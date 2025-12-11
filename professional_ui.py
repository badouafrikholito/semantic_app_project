# professional_ui.py - UPDATED FOR REAL BACKEND
import streamlit as st
import requests
import time

# Backend URL - FIXED
BACKEND_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="Academic Paper Search",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .tag-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .result-card {
        background: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔍 Search Academic Papers</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">vector database</div>', unsafe_allow_html=True)

# Check backend status
try:
    response = requests.get(f"{BACKEND_URL}/", timeout=3)
    backend_data = response.json()
    backend_status = "✅ Connected"
    docs_count = backend_data.get('documents', 0)
except:
    backend_status = "❌ Not connected"
    docs_count = 0

# Status bar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Backend Status", backend_status)
with col2:
    st.metric("Papers in DB", docs_count)
with col3:
    st.metric("Search Mode", "Real" if docs_count > 0 else "Test")

st.divider()

# Search Section
st.markdown("### 🔎 Search Papers")

# Search input with pre-fill
if st.session_state.search_query:
    default_query = st.session_state.search_query
else:
    default_query = ""

query = st.text_input(
    "",
    value=default_query,
    placeholder="Enter search query (e.g., 'transformer attention')",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    k = st.slider("Number of results", 1, 10, 5)
with col2:
    st.write("")  # Spacer
    search_clicked = st.button("🔍 SEARCH", type="primary", use_container_width=True)

# Clickable tags
st.markdown("### 🏷️ Popular Topics")

tags = ["Attention", "BERT", "Vector DB", "Docker", "Transformer", "Semantic Search", "Machine Learning"]

# Create tag buttons
tag_cols = st.columns(len(tags))
for i, tag in enumerate(tags):
    with tag_cols[i]:
        if st.button(tag, key=f"tag_{i}", use_container_width=True):
            st.session_state.search_query = tag
            st.session_state.search_triggered = True
            st.rerun()

# Handle search
if search_clicked and query:
    st.session_state.search_query = query
    st.session_state.search_triggered = True

if st.session_state.search_triggered:
    search_term = st.session_state.search_query

    with st.spinner(f"🔍 Searching for '{search_term}'..."):
        try:
            response = requests.get(
                f"{BACKEND_URL}/search",
                params={"q": search_term, "k": k},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.search_results = data

                if "error" in data:
                    st.error(f"Error: {data['error']}")
                elif "message" in data:
                    st.warning(data['message'])
                else:
                    st.success(
                        f"✅ Found {data.get('results_found', len(data.get('results', {}).get('documents', [])))} results")

                    # Show if in test mode
                    if data.get('mode') == 'test':
                        st.info("ℹ️ Running in test mode - Index documents for real semantic search")
            else:
                st.error(f"Search failed: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend!")
            st.info("Make sure backend is running:")
            st.code("python real_backend.py")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.session_state.search_triggered = False

# Display results
if st.session_state.search_results:
    data = st.session_state.search_results

    st.markdown(f"### 📊 Results for: **'{data.get('query', '')}'**")

    if "results" in data and data["results"].get("documents"):
        results = data["results"]
        documents = results["documents"]
        similarities = results.get("similarities", [])

        for i, (doc, sim) in enumerate(zip(documents, similarities)):
            with st.container():
                st.markdown(f'<div class="result-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"#### 📄 Paper {i + 1}")
                    st.write(doc)
                with col2:
                    if i < len(similarities):
                        st.metric("Similarity", f"{sim}%")

                st.markdown('</div>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    # Index button
    if st.button("📥 Index Documents", use_container_width=True, type="secondary"):
        with st.spinner("Indexing academic papers..."):
            try:
                response = requests.post(f"{BACKEND_URL}/index")
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"Indexing failed: {result.get('error', 'Unknown error')}")
                else:
                    st.error(f"Failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Test connection
    if st.button("🔌 Test Connection", use_container_width=True):
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=3)
            st.success("✅ Backend connected!")
            st.json(response.json())
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

    st.divider()
    st.markdown(f"**Backend:** {BACKEND_URL}")
    st.markdown("**Model:** Sentence-BERT")
    st.markdown("**Vector DB:** ChromaDB")

# Footer
st.divider()
st.caption("🎯 Real Semantic Search System | Sentence-BERT + ChromaDB")