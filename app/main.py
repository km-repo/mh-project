import os, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.preprocessing import normalize
from fastapi.middleware.cors import CORSMiddleware

INDEX_PATH = os.getenv("INDEX_PATH", "data/faiss_index.idx")
META_PATH = os.getenv("META_PATH", "data/metadata.json")
MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")

app = FastAPI(title="MH Assist Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str
    k: int = 5  # top k results

@app.on_event("startup")
def load_resources():
    global index, metadata, model
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    model = SentenceTransformer(MODEL_NAME)

@app.get("/health")
def health():
    return {"status": "ok", "index_size": index.ntotal}

@app.post("/search")
def search(q: Query):
    if not q.query:
        raise HTTPException(status_code=400, detail="query is empty")
    vec = model.encode([q.query], convert_to_numpy=True)
    vec = normalize(vec, axis=1).astype('float32')
    D, I = index.search(vec, q.k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        m = metadata[idx]
        results.append({
            "score": float(score),
            "context": m["context"],
            "response": m["response"]
        })
    return {"query": q.query, "results": results}