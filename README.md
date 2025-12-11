# Semantic Search — Final Project (Hybrid: PyCharm + Docker)

## Overview
This project implements a semantic search application using:
- Sentence-BERT (all-MiniLM-L6-v2) for embeddings
- ChromaDB vector store (local embedded mode for development; REST server for Docker)
- FastAPI backend
- Streamlit UI
- Docker + docker-compose for full containerized deployment

## Folder structure
(see project root)

## Quickstart — PyCharm / Local (recommended for development)
1. Create a venv and install dependencies:pip install -r requirements.txt
2. 2. Ensure `app/config.py` has:
```py
MODE = "local"
start backend; python run_local.py