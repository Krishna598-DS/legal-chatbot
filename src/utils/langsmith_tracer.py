"""
Day 6: LangSmith Tracing
Wraps every OpenAI call with LangSmith tracing.
Every call is recorded with:
- Full input (system message + user question)
- Full output (model answer)
- Latency (how long it took)
- Token usage (how much it cost)
- Custom metadata (session ID, environment, model version)

In production, this is how you debug bad responses,
monitor costs, and evaluate model quality over time.
"""

import os
from functools import wraps
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# LangSmith is configured via environment variables
# These must be set before importing langsmith
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "legal-chatbot")

def is_langsmith_configured() -> bool:
    """Check if LangSmith credentials are available."""
    return bool(LANGCHAIN_API_KEY and LANGCHAIN_API_KEY != "your_langsmith_key_here")


def get_tracer_status() -> dict:
    """Return LangSmith configuration status."""
    configured = is_langsmith_configured()
    return {
        "enabled": configured,
        "project": LANGCHAIN_PROJECT if configured else None,
        "tracing_v2": LANGCHAIN_TRACING_V2
    }
