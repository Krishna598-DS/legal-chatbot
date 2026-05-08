"""
Day 5: FastAPI Main Application
This is the entry point for the API server.

FastAPI automatically:
- Validates all request bodies against Pydantic models
- Returns 422 errors for invalid input
- Generates /docs (Swagger UI) and /redoc documentation
- Handles async requests concurrently
"""

import time
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger

from src.api.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ModelInfoResponse,
    ErrorResponse
)
from src.api.llm_service import chatbot_service
from src.utils.config import settings


# ============================================================
# LIFESPAN — runs on startup and shutdown
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.
    This is where you'd load ML models, connect to databases, etc.
    """
    logger.info("=" * 50)
    logger.info("Legal Chatbot API Starting Up")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Model: {settings.MODEL_ID}")
    logger.info("=" * 50)
    
    # Validate settings on startup
    settings.validate()
    
    yield  # API is now running and accepting requests
    
    # Shutdown
    logger.info("Legal Chatbot API Shutting Down")


# ============================================================
# APP CREATION
# ============================================================
app = FastAPI(
    title="Legal Chatbot API",
    description="""
    A fine-tuned legal domain chatbot API.
    
    ## Features
    - Powered by a fine-tuned GPT-4o-mini model
    - Covers contract law, employment law, IP, and more
    - Production-grade with retry logic and error handling
    
    ## Important
    Responses are for informational purposes only.
    Always consult a licensed attorney for legal advice.
    """,
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# MIDDLEWARE
# ============================================================
# CORS — allows browsers to call this API from any origin
# In production, replace "*" with your specific frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware — logs every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware runs on EVERY request before it reaches your route.
    This logs method, path, and response time for every call.
    Essential for debugging and performance monitoring.
    """
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(
        f"{request.method} {request.url.path} "
        f"-> {response.status_code} ({duration}ms)"
    )
    return response


# ============================================================
# ROUTES
# ============================================================

@app.get("/", include_in_schema=False)
async def root():
    """Redirect hint for root URL."""
    return {
        "message": "Legal Chatbot API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Health check endpoint.
    Load balancers and Kubernetes ping this every 30 seconds.
    If it returns non-200, the container is restarted automatically.
    This is called a liveness probe in production.
    """
    return HealthResponse(
        status="healthy",
        environment=settings.APP_ENV,
        model_id=settings.MODEL_ID
    )


@app.get(
    "/model/info",
    response_model=ModelInfoResponse,
    tags=["Model"],
    summary="Get information about the loaded model"
)
async def model_info():
    """Returns details about the fine-tuned model being served."""
    info = chatbot_service.get_model_info()
    return ModelInfoResponse(**info)


@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Ask a legal question",
    responses={
        200: {"description": "Successful response"},
        422: {"description": "Validation error — check request format"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"}
    }
)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    
    Send a legal question and receive a professional legal answer
    from the fine-tuned model.
    
    - **question**: Your legal question (3-2000 characters)
    - **temperature**: Response randomness (0.0-2.0, default 0.3)
    - **max_tokens**: Maximum response length (50-2000, default 500)
    """
    try:
        result = chatbot_service.get_legal_answer(
            question=request.question,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return ChatResponse(
            answer=result["answer"],
            model_used=result["model_used"],
            tokens_used=result["tokens_used"],
            response_time_ms=result["response_time_ms"],
            session_id=request.session_id
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )


@app.post(
    "/chat/stream",
    tags=["Chat"],
    summary="Stream a legal answer token by token"
)
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint.
    Instead of waiting for the full response, tokens stream
    back to the client as they are generated.
    This makes the UI feel much faster — users see text appearing
    immediately rather than waiting 3-5 seconds for the full answer.
    This is how ChatGPT's UI works.
    """
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate():
        try:
            stream = client.chat.completions.create(
                model=settings.MODEL_ID,
                messages=[
                    {"role": "system", "content": settings.SYSTEM_MESSAGE},
                    {"role": "user", "content": request.question}
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True    # This is what enables streaming
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"\n[Error: {str(e)}]"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
