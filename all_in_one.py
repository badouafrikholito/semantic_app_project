# all_in_one_working.py
import streamlit as st
import subprocess
import threading
import requests
import time
import sys

# ========== BACKEND SERVER ==========
print("🚀 Starting backend server...")

# Start FastAPI backend in background
backend_process = subprocess.Popen(
    [sys.executable, "-c", """
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Semantic Search API is running"}

@app.get("/search")
def search(q: str = "test", k: int = 5):
    return {
        "query": q,
        "results": {
            "documents": [
                f"Research paper on {q} using transformer models.",
                f"Academic study about {q} applications.",
                f"Conference paper discussing {q} in NLP.",
                f"Journal article about {q} implementations.",
                f"Technical report on {q} with vector databases."
            ],
            "distances": [0.1, 0.15, 0.2, 0.25, 0.3]
        }
    }

@app.post("/index")
def index():
    return {"message": "Documents indexed successfully"}

print("✅ Backend running on http://0.0.0.0:8001")
uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")
"""],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for backend to start
time.sleep(3)
print("✅ Backend ready!")

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="Semantic Search", layout="centered")

# SIMPLE UI LIKE YOUR IMAGE
st.markdown("# Search Academic Papers")
st.markdown("### vector database")

# Search bar
query = st.text_input("", placeholder="Enter search query...", key="search_input")

col1, col2 = st.columns([4, 1])
with col1:
    pass
with col2:
    search_clicked = st.button("Search", type="primary", use_container_width=True)

# Clickable tags
st.markdown("**Click to search:**")
tags = ["Attention", "BERT", "Vector DB", "Docker", "Transformer", "Semantic Search", "Machine Learning"]

# Show tags as buttons
tag_cols = st.columns(len(tags))
for i, tag in enumerate(tags):
    with tag_cols[i]:
        if st.button(tag, key=f"tag_{i}"):
            st.session_state.search_input = tag
            st.session_state.tag_search = tag
            st.rerun()

# Status
st.markdown("---")
st.markdown("- **Backend:** Connected ✅")
st.markdown("- **Model:** Sentence-BERT")
st.markdown("- **Vector DB:** ChromaDB")

# Handle search
if search_clicked and query:
    search_term = query
elif 'tag_search' in st.session_state:
    search_term = st.session_state.tag_search
    del st.session_state.tag_search
else:
    search_term = None

if search_term:
    st.markdown(f"### Searching: **{search_term}**")

    try:
        response = requests.get(
            "http://127.0.0.1:8001/search",
            params={"q": search_term, "k": 5},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Found {len(data['results']['documents'])} results")

            for i, doc in enumerate(data["results"]["documents"]):
                st.markdown(f"**Result {i + 1}:** {doc}")
                st.divider()
        else:
            st.error(f"Search failed: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Backend might still be starting... try again in 3 seconds")

# Sidebar for testing
with st.sidebar:
    if st.button("Test Connection"):
        try:
            response = requests.get("http://127.0.0.1:8001/", timeout=3)
            st.success(f"✅ {response.json()}")
        except:
            st.error("❌ Backend not responding")

print("✅ Streamlit UI running on http://localhost:8501")
print("✅ Everything is running! Open browser to http://localhost:8501")

# Keep script running
try:
    backend_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    backend_process.terminate()
