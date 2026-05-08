"""
Pydantic models for API request and response validation.
FastAPI uses these to:
1. Validate incoming request data (wrong types = automatic 422 error)
2. Generate OpenAPI/Swagger documentation automatically
3. Serialize response data to JSON

This is one of the biggest reasons to use FastAPI over Flask.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============================================================
# REQUEST MODELS (what the client sends TO the API)
# ============================================================

class ChatRequest(BaseModel):
    """
    The request body for POST /chat
    Field() lets us add validation rules and documentation.
    """
    question: str = Field(
        ...,                          # ... means required (no default)
        min_length=3,
        max_length=2000,
        description="The legal question to ask the chatbot",
        example="What is the difference between void and voidable contracts?"
    )
    temperature: Optional[float] = Field(
        default=0.3,
        ge=0.0,                       # ge = greater than or equal to
        le=2.0,                       # le = less than or equal to
        description="Response randomness. 0=deterministic, 2=creative"
    )
    max_tokens: Optional[int] = Field(
        default=500,
        ge=50,
        le=2000,
        description="Maximum tokens in the response"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session ID for conversation tracking"
    )

    class Config:
        # Example shown in Swagger UI
        json_schema_extra = {
            "example": {
                "question": "What is an NDA and when should I use one?",
                "temperature": 0.3,
                "max_tokens": 500
            }
        }


# ============================================================
# RESPONSE MODELS (what the API sends BACK to the client)
# ============================================================

class ChatResponse(BaseModel):
    """Response body for POST /chat"""
    answer: str = Field(description="The legal assistant's response")
    model_used: str = Field(description="The model ID that generated this response")
    tokens_used: int = Field(description="Total tokens consumed (for cost tracking)")
    response_time_ms: float = Field(description="How long the API took to respond")
    session_id: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Response body for GET /health"""
    status: str
    environment: str
    model_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelInfoResponse(BaseModel):
    """Response body for GET /model/info"""
    model_id: str
    base_model: str
    fine_tuned: bool
    domain: str
    capabilities: list[str]


class ErrorResponse(BaseModel):
    """Standard error response shape"""
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
