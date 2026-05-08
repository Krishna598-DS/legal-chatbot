# Base image — official Python 3.11 slim variant
# 'slim' means no unnecessary OS packages = smaller image = faster deploys
# This is the same Python version you developed with — guaranteed compatibility
FROM python:3.11-slim

# Set working directory inside the container
# All subsequent commands run from here
WORKDIR /app

# Copy requirements first — before copying code
# Why? Docker caches each step. If requirements.txt didn't change,
# Docker reuses the cached pip install layer even if your code changed.
# This makes rebuilds 10x faster during development.
COPY requirements.txt .

# Install dependencies
# --no-cache-dir: don't cache pip downloads inside the image (saves space)
# --upgrade pip: always use latest pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/
COPY models/ ./models/

# Create necessary directories
RUN mkdir -p data/fine_tune logs mlflow_runs

# Environment variables with defaults
# These get overridden by docker-compose or -e flags at runtime
ENV APP_ENV=production
ENV LOG_LEVEL=INFO
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# PYTHONUNBUFFERED=1 means Python prints logs immediately
# without buffering — critical for seeing logs in Docker

# Expose the port FastAPI runs on
# This is documentation — tells Docker which port the app uses
EXPOSE 8000

# Health check — Docker will ping this every 30s
# If it fails 3 times, Docker marks the container as unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start command — runs when container starts
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
