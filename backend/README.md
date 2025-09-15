# 🧠 Mental Health Semantic Search - Backend

This is the FastAPI + FAISS backend for the semantic search app that helps mental health professionals retrieve possible responses to patient queries.

---

## 🚀 Features
- Ingests a CSV dataset (`context`, `response`)
- Generates embeddings with [SentenceTransformers](https://www.sbert.net/)
- Stores embeddings in [FAISS](https://faiss.ai) for semantic search
- Exposes a REST API endpoint via [FastAPI](https://fastapi.tiangolo.com/)

---

## 📂 Project Structure
- **`app/main.py`** → Entry point for the FastAPI backend.  
- **`data/index.faiss`** → The FAISS vector index generated from training data.  
- **`data/metadata.json`** → Metadata mapping between embeddings and original records.  
- **`data/train.csv`** → Source dataset containing `context` (patient query) and `response` (professional reply).  
- **`scripts/build_index.py`** → Script to process the CSV and build the FAISS index.  
- **`models/`** → Folder for pre-downloaded [SentenceTransformers](https://www.sbert.net/) models used to generate embeddings.  
