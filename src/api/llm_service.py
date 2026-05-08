"""
LLM Service Layer — Fixed (removed unsupported metadata parameter)
"""

import os
import time
from openai import OpenAI
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import RateLimitError, APITimeoutError
from dotenv import load_dotenv

load_dotenv()

from src.utils.config import settings

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "legal-chatbot")

LANGSMITH_ENABLED = bool(os.environ.get("LANGCHAIN_API_KEY", "").startswith("lsv2"))


class LegalChatbotService:

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_id = settings.MODEL_ID
        logger.info(f"LegalChatbotService initialized with model: {self.model_id}")
        if LANGSMITH_ENABLED:
            logger.info(f"LangSmith tracing ENABLED — project: {os.environ['LANGCHAIN_PROJECT']}")
        else:
            logger.warning("LangSmith tracing DISABLED — add LANGCHAIN_API_KEY to .env")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError)),
        reraise=True
    )
    def get_legal_answer(
        self,
        question: str,
        temperature: float = 0.3,
        max_tokens: int = 500,
        session_id: str = None
    ) -> dict:
        start_time = time.time()
        logger.info(f"Querying model: {question[:60]}...")

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": settings.SYSTEM_MESSAGE
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        end_time = time.time()
        response_time_ms = round((end_time - start_time) * 1000, 2)
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        model_used = response.model

        logger.info(f"Response in {response_time_ms}ms | Tokens: {tokens_used}")

        return {
            "answer": answer,
            "model_used": model_used,
            "tokens_used": tokens_used,
            "response_time_ms": response_time_ms
        }

    def get_model_info(self) -> dict:
        model_id = self.model_id
        is_fine_tuned = model_id.startswith("ft:")
        return {
            "model_id": model_id,
            "base_model": "gpt-4o-mini-2024-07-18",
            "fine_tuned": is_fine_tuned,
            "domain": "legal",
            "capabilities": [
                "Contract law questions",
                "NDA and confidentiality",
                "Employment law",
                "Intellectual property",
                "Liability and indemnity",
                "General legal literacy"
            ]
        }


chatbot_service = LegalChatbotService()
