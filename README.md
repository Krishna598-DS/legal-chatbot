# ⚖️ Legal AI Chatbot — Full MLOps Pipeline

[![Live API](https://img.shields.io/badge/API-Live-green)](https://legal-chatbot-a1fb.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://docker.com)

A production-grade legal domain chatbot built with a complete MLOps pipeline. Fine-tuned GPT-4o-mini on 60 legal Q&A examples, served via FastAPI, traced with LangSmith, tracked with MLflow, containerized with Docker, and deployed on Render.

## 🔗 Live Demo
**API:** https://legal-chatbot-a1fb.onrender.com  
**Swagger UI:** https://legal-chatbot-a1fb.onrender.com/docs

## 🏗️ Architecture

Legal Dataset (60 examples)
↓
OpenAI Fine-tuning API
↓
ft:gpt-4o-mini (legal-chatbot)
↓
FastAPI + Uvicorn (REST API)
↓                    ↓
LangSmith (tracing)    MLflow (experiments)
↓
Streamlit (Chat UI)
↓
Docker Compose
↓
Render (Cloud Deployment)

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Model | OpenAI Fine-tuning API | Domain adaptation |
| API | FastAPI + Uvicorn | REST API server |
| Validation | Pydantic | Request/response validation |
| Tracing | LangSmith | LLM observability |
| Tracking | MLflow | Experiment tracking |
| UI | Streamlit | Chat interface |
| Container | Docker + Compose | Containerization |
| Deployment | Render | Cloud hosting |
| Resilience | Tenacity | Retry logic |

## 📊 Training Results

| Metric | Value |
|---|---|
| Base Model | gpt-4o-mini-2024-07-18 |
| Training Examples | 54 |
| Validation Examples | 6 |
| Initial Loss | 1.86 |
| Final Training Loss | 0.28 |
| Final Validation Loss | 0.87 |
| Loss Reduction | 84.95% |
| Training Steps | 162 |
| Training Cost | ~$0.38 |

## 📁 Project Structure

legal-chatbot/
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Pydantic request/response models
│   │   └── llm_service.py   # LLM service layer
│   ├── training/
│   │   ├── create_dataset.py    # Dataset creation
│   │   ├── validate_dataset.py  # Pre-training validation
│   │   ├── finetune_manager.py  # Fine-tuning lifecycle
│   │   └── mlflow_tracker.py    # Experiment logging
│   ├── ui/
│   │   └── app.py           # Streamlit chat interface
│   └── utils/
│       ├── config.py         # Central configuration
│       └── langsmith_tracer.py # Tracing setup
├── data/fine_tune/           # JSONL training data
├── models/                   # Model configuration
├── Dockerfile                # FastAPI container
├── docker/Dockerfile.streamlit
├── docker-compose.yml        # Multi-container orchestration
├── render.yaml               # Render deployment config
└── requirements.txt


## 🚀 Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/Krishna598-DS/legal-chatbot
cd legal-chatbot
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add your API keys to .env
cp .env.example .env  # Edit with your keys

# Start API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Start UI (new terminal)
streamlit run src/ui/app.py --server.port 8501
```

### Docker
```bash
docker compose up --build
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /model/info | Model information |
| POST | /chat | Ask a legal question |
| POST | /chat/stream | Streaming response |
| GET | /docs | Swagger UI |

## 🎯 Legal Domains Covered

- Contract Law (breach, formation, clauses)
- NDA & Confidentiality Agreements
- Employment Law (wrongful termination, discrimination)
- Intellectual Property (copyright, patent, trademark)
- Liability & Indemnity
- General Legal Literacy

## ⚠️ Disclaimer

This chatbot is for informational purposes only. Always consult a licensed attorney for legal advice specific to your situation.
