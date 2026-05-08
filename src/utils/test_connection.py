"""
OpenAI API connection test.
This is the first thing you run on any new machine to verify your setup works.
In production, this logic becomes a health-check endpoint in FastAPI.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

# Load environment variables from .env file
load_dotenv()

def test_openai_connection():
    """
    Test that we can:
    1. Load the API key from .env
    2. Create an OpenAI client
    3. Send a real API request and get a response
    """
    
    # Step 1: Verify the key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        logger.error("OPENAI_API_KEY not set in .env file!")
        raise ValueError("Please set your OPENAI_API_KEY in the .env file")
    
    logger.info(f"API key loaded: {api_key[:8]}...{api_key[-4:]} (masked for security)")
    
    # Step 2: Create the client
    # The client automatically reads OPENAI_API_KEY from environment
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client created successfully")
    
    # Step 3: Send a test message
    logger.info("Sending test message to GPT-4o-mini...")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",          # Cheapest capable model, ~$0.0001 per test
        messages=[
            {
                "role": "system",
                "content": "You are a legal assistant specializing in contract law."
            },
            {
                "role": "user", 
                "content": "In one sentence, what is the purpose of an NDA?"
            }
        ],
        max_tokens=100,               # Limit response length = limit cost
        temperature=0.3               # Lower = more consistent/factual responses
    )
    
    # Step 4: Extract and display the response
    reply = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    model_used = response.model
    
    logger.success("=" * 60)
    logger.success("CONNECTION TEST PASSED")
    logger.success("=" * 60)
    logger.info(f"Model: {model_used}")
    logger.info(f"Tokens used: {tokens_used} (roughly ${tokens_used * 0.00000015:.6f})")
    logger.info(f"Response: {reply}")
    logger.success("=" * 60)
    
    return {
        "status": "success",
        "model": model_used,
        "tokens_used": tokens_used,
        "response": reply
    }


if __name__ == "__main__":
    test_openai_connection()
