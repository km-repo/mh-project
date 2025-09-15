# 🧠 Mental Health Semantic Search App

This project provides a semantic search tool to assist mental health professionals during patient conversations.  
It allows professionals to input a patient’s query and retrieve the most relevant responses from a dataset of expert replies.

---

## ✨ Features
- **Semantic Search**: Uses [SentenceTransformers](https://www.sbert.net/) to embed text.
- **Vector Indexing**: Stores embeddings in [FAISS](https://faiss.ai) for efficient similarity search.
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) with a REST API for querying responses.
- **Frontend**: [React](https://react.dev/) app for user interaction.
