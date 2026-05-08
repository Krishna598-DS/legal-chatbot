"""
Central configuration module.
All settings loaded from .env file.
Never hardcode values — always read from environment.
This is how production systems manage configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Load .env file
load_dotenv()


class Settings:
    """
    Single source of truth for all app configuration.
    Using a class instead of scattered os.getenv() calls
    makes the code testable and maintainable.
    """

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Model — reads from the saved fine_tuned_model.json
    # Falls back to gpt-4o-mini if fine-tuned model not found
    @property
    def MODEL_ID(self) -> str:
        model_config = Path("models/fine_tuned_model.json")
        if model_config.exists():
            import json
            with open(model_config) as f:
                data = json.load(f)
                model = data.get("fine_tuned_model")
                if model:
                    return model
        # Fallback
        return "gpt-4o-mini-2024-07-18"

    # API settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # LLM inference settings
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.3
    
    # System message baked into every request
    SYSTEM_MESSAGE: str = """You are an expert legal assistant with deep knowledge \
of contract law, employment law, intellectual property, and corporate law. \
You provide clear, accurate, and professional legal information. \
Always clarify that your responses are for informational purposes \
and recommend consulting a licensed attorney for specific legal advice."""

    def validate(self):
        """Check all required settings are present at startup."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in .env")
        logger.info(f"Environment: {self.APP_ENV}")
        logger.info(f"Model: {self.MODEL_ID}")
        logger.info(f"Log level: {self.LOG_LEVEL}")


# Single instance used everywhere
settings = Settings()
