import re
import os, json, argparse
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.preprocessing import normalize


def normalize_whitespace(s: str) -> str:
    if not isinstance(s, str):
        return ""
    # Normalize line endings
    s = re.sub(r'\r\n?|\n', '\n', s)
    # Remove spaces around newlines
    s = re.sub(r'[ \t]*\n[ \t]*', '\n', s)
    # Collapse multiple spaces into one
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def build(csv_path, index_path, meta_path, model_name="all-MiniLM-L6-v2", batch_size=128):
    df = pd.read_csv(csv_path)
    
    # Drop duplicates (based on both context + response)
    # normalize newlines
    before = len(df)
    df["Context"] = df["Context"].apply(normalize_whitespace)
    df["Response"] = df["Response"].apply(normalize_whitespace)
    df = df.drop_duplicates(subset=['Context', 'Response']).reset_index(drop=True)
    after = len(df)
    print(f"Removed {before - after} duplicate rows (kept {after}).")

    # extract contexts and responses
    texts = df['Context'].astype(str).tolist()
    responses = df['Response'].astype(str).tolist()
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True)
    
    # normalize for cosine similarity with IndexFlatIP
    embeddings = normalize(embeddings, axis=1, norm='l2').astype('float32')
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)

    #save index and metadata
    faiss.write_index(index, index_path)
    metadata = [{"id": i, "context": texts[i], "response": responses[i]} for i in range(len(texts))]
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("Built index:", index.ntotal, "vectors")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="../data/train.csv")
    p.add_argument("--index", default="../data/faiss_index.idx")
    p.add_argument("--meta", default="../data/metadata.json")
    args = p.parse_args()
    build(args.csv, args.index, args.meta)