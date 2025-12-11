"""
Run this file in PyCharm or terminal to start the FastAPI backend in local mode.

Before running, make sure:
- app/config.py has MODE = "local"
- you've installed requirements

Run:
    python run_local.py
"""
import uvicorn

if __name__ == "__main__":
    # This runs the FastAPI app defined in app.main
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)