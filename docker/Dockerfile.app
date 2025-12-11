# Dockerfile for backend service (FastAPI)
FROM python:3.10-slim

WORKDIR /workspace

# Copy project files
COPY . /workspace

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8001

# When running in docker compose, app/config.py should be adjusted to MODE="docker"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]