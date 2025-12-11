import sys
import os

# ===== PATH FIX =====
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_file_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, current_file_dir)

# ===== CREATE ALL NEEDED CLASSES =====
# Correct way to create classes
ModelCard = type('ModelCard', (), {})
CommitOperationAdd = type('CommitOperationAdd', (), {})
CommitOperationDelete = type('CommitOperationDelete', (), {})
CommitOperation = type('CommitOperation', (), {})
HfApi = type('HfApi', (), {})
ModelInfo = type('ModelInfo', (), {'id': 'mock', 'sha': 'mock'})  # FIXED: Use () not {}
RepoFile = type('RepoFile', (), {})


# Create the main mock
class EverythingMock:
    # Version and constants
    __version__ = '0.19.4'
    __name__ = 'huggingface_hub'
    ENDPOINT = 'https://huggingface.co'
    HF_HUB_DISABLE_TELEMETRY = False
    _CACHED_NO_EXIST = object()

    # ALL imports
    ModelCard = ModelCard
    CommitOperationAdd = CommitOperationAdd
    CommitOperationDelete = CommitOperationDelete
    CommitOperation = CommitOperation
    HfApi = HfApi
    ModelInfo = ModelInfo
    RepoFile = RepoFile

    # Functions
    @staticmethod
    def get_full_repo_name(*args, **kwargs):
        return 'mock/repo'

    @staticmethod
    def hf_hub_download(*args, **kwargs):
        os.makedirs('./models', exist_ok=True)
        return './models/model.bin'

    @staticmethod
    def cached_download(*args, **kwargs):
        return './models/model.bin'

    @staticmethod
    def snapshot_download(*args, **kwargs):
        return './models/'

    @staticmethod
    def model_info(*args, **kwargs):
        return ModelInfo()

    @staticmethod
    def list_repo_files(*args, **kwargs):
        return []

    # Submodules
    class utils:
        @staticmethod
        def are_progress_bars_disabled():
            return False

        @staticmethod
        def get_session(*args, **kwargs):
            return type('Session', (), {})()

    class constants:
        ENDPOINT = 'https://huggingface.co'
        HF_HUB_DISABLE_TELEMETRY = False


# Register everything
everything = EverythingMock()
sys.modules['huggingface_hub'] = everything
sys.modules['huggingface_hub.utils'] = everything.utils
sys.modules['huggingface_hub.constants'] = everything.constants

print("[FIX] HuggingFace hub mock created")

# ===== CHROMADB =====
os.environ['CHROMA_DB_IMPLEMENTATION'] = 'duckdb+parquet'
os.makedirs('./models', exist_ok=True)

# ===== IMPORT YOUR APP =====
try:
    print("Testing imports...")
    from sentence_transformers import SentenceTransformer

    print("✓ sentence-transformers OK")

    from fastapi import FastAPI
    from app.search import SemanticSearch
    from app.config import MODE

    app = FastAPI(title="Semantic Search API")
    search_engine = SemanticSearch(mode=MODE)


    @app.get("/")
    def root():
        return {"app": "Semantic Search", "status": "running"}


    @app.get("/health")
    def health():
        return {"status": "healthy"}


    @app.get("/search")
    def search(q: str, k: int = 5):
        return search_engine.search(q, k)


    @app.post("/index")
    def index_docs():
        search_engine.index_documents()
        return {"status": "indexed"}


    print("✅ Your app loaded successfully")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()

    # Fallback
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    def home():
        return {"app": "Semantic", "status": "fallback"}

# ===== RUN =====
if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("🚀 Server: http://localhost:8000")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
