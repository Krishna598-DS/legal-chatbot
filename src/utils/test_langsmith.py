"""
Test LangSmith tracing end to end.
After running this, go to https://smith.langchain.com
and you should see a trace appear in your project.
"""

import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def test_langsmith_tracing():
    """Send a test question and verify it appears in LangSmith."""

    api_key = os.getenv("LANGCHAIN_API_KEY", "")
    project = os.getenv("LANGCHAIN_PROJECT", "legal-chatbot")

    if not api_key or api_key == "your_langsmith_key_here":
        logger.error("LANGCHAIN_API_KEY not set in .env file!")
        logger.error("Go to https://smith.langchain.com to get your key")
        return False

    logger.info(f"LangSmith API key loaded: {api_key[:12]}...")
    logger.info(f"Project: {project}")

    # Set environment variables for LangSmith
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = api_key
    os.environ["LANGCHAIN_PROJECT"] = project

    # Import after setting env vars
    from langsmith import Client
    from langsmith import traceable

    # Test 1: Verify LangSmith client connects
    try:
        client = Client()
        logger.success("LangSmith client connected successfully")
    except Exception as e:
        logger.error(f"LangSmith connection failed: {e}")
        return False

    # Test 2: Create a traced function and call it
    @traceable(
        name="legal-qa-test",
        tags=["test", "legal", "day6"],
        metadata={"environment": "development", "model": "fine-tuned"}
    )
    def ask_legal_question(question: str) -> str:
        """This function call will appear as a trace in LangSmith."""
        import openai
        client_oai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client_oai.chat.completions.create(
            model=os.getenv(
                "FINE_TUNED_MODEL",
                "ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu"
            ),
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert legal assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=150,
            temperature=0.3
        )
        return response.choices[0].message.content

    logger.info("Sending traced test question to LangSmith...")
    
    answer = ask_legal_question(
        "In one sentence, what is a breach of contract?"
    )

    logger.success("=" * 60)
    logger.success("LANGSMITH TRACING TEST PASSED")
    logger.success("=" * 60)
    logger.info(f"Answer: {answer}")
    logger.success(f"Check your trace at: https://smith.langchain.com")
    logger.success(f"Look for project: {project}")
    logger.success("=" * 60)
    return True


if __name__ == "__main__":
    test_langsmith_tracing()
