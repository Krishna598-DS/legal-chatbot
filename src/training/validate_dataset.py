"""
Day 2: Dataset Validation Script
Before uploading to OpenAI for fine-tuning, validate:
1. Format correctness (every line is valid JSON with correct structure)
2. Token counts (each example must be under 4096 tokens)
3. Cost estimation (so you know how much fine-tuning will cost)
4. Quality checks (minimum lengths, role presence)

This is what a professional ML engineer does before burning compute budget.
"""

import json
import os
from pathlib import Path
from loguru import logger

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available, skipping token counts")


def count_tokens(messages: list, model: str = "gpt-4o-mini") -> int:
    """Count tokens in a list of messages using tiktoken."""
    if not TIKTOKEN_AVAILABLE:
        return 0
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    total = 0
    for message in messages:
        # 4 tokens overhead per message
        total += 4
        for key, value in message.items():
            total += len(encoding.encode(str(value)))
    total += 2  # Reply prime tokens
    return total


def validate_example(example: dict, idx: int) -> list:
    """
    Validate a single training example.
    Returns a list of error strings (empty = valid).
    """
    errors = []
    
    # Check top-level structure
    if "messages" not in example:
        errors.append(f"Example {idx}: Missing 'messages' key")
        return errors
    
    messages = example["messages"]
    
    if not isinstance(messages, list):
        errors.append(f"Example {idx}: 'messages' must be a list")
        return errors
    
    if len(messages) < 2:
        errors.append(f"Example {idx}: Must have at least 2 messages")
        return errors
    
    # Check roles
    roles = [m.get("role") for m in messages]
    
    if "user" not in roles:
        errors.append(f"Example {idx}: Must have at least one 'user' message")
    
    if "assistant" not in roles:
        errors.append(f"Example {idx}: Must have at least one 'assistant' message")
    
    # Check each message has content
    for i, msg in enumerate(messages):
        if "role" not in msg:
            errors.append(f"Example {idx}, message {i}: Missing 'role'")
        if "content" not in msg:
            errors.append(f"Example {idx}, message {i}: Missing 'content'")
        elif not msg["content"].strip():
            errors.append(f"Example {idx}, message {i}: Empty 'content'")
        
        # Check role is valid
        if msg.get("role") not in ["system", "user", "assistant"]:
            errors.append(f"Example {idx}, message {i}: Invalid role '{msg.get('role')}'")
    
    # Check token count
    if TIKTOKEN_AVAILABLE:
        token_count = count_tokens(messages)
        if token_count > 4096:
            errors.append(f"Example {idx}: {token_count} tokens exceeds 4096 limit")
    
    return errors


def validate_file(filepath: str) -> dict:
    """
    Validate an entire JSONL file.
    Returns a dict with validation results.
    """
    results = {
        "filepath": filepath,
        "total_examples": 0,
        "valid_examples": 0,
        "errors": [],
        "token_counts": [],
        "estimated_training_cost": 0.0
    }
    
    if not Path(filepath).exists():
        results["errors"].append(f"File not found: {filepath}")
        return results
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            
            results["total_examples"] += 1
            
            # Try to parse JSON
            try:
                example = json.loads(line)
            except json.JSONDecodeError as e:
                results["errors"].append(f"Line {idx+1}: Invalid JSON - {e}")
                continue
            
            # Validate structure
            errors = validate_example(example, idx+1)
            if errors:
                results["errors"].extend(errors)
            else:
                results["valid_examples"] += 1
            
            # Count tokens for cost estimation
            if TIKTOKEN_AVAILABLE and "messages" in example:
                tokens = count_tokens(example["messages"])
                results["token_counts"].append(tokens)
    
    # Estimate fine-tuning cost
    # OpenAI charges $0.008 per 1K tokens for gpt-4o-mini fine-tuning (training)
    if results["token_counts"]:
        total_tokens = sum(results["token_counts"])
        # Training runs for ~3 epochs by default
        results["estimated_training_cost"] = (total_tokens * 3 / 1000) * 0.008
        results["avg_tokens_per_example"] = total_tokens / len(results["token_counts"])
        results["max_tokens"] = max(results["token_counts"])
        results["min_tokens"] = min(results["token_counts"])
    
    return results


def print_validation_report(results: dict):
    """Print a formatted validation report."""
    logger.info("=" * 60)
    logger.info(f"VALIDATION REPORT: {results['filepath']}")
    logger.info("=" * 60)
    logger.info(f"Total examples:  {results['total_examples']}")
    logger.info(f"Valid examples:  {results['valid_examples']}")
    logger.info(f"Invalid examples: {results['total_examples'] - results['valid_examples']}")
    
    if results.get("token_counts"):
        logger.info(f"Avg tokens/example: {results.get('avg_tokens_per_example', 0):.0f}")
        logger.info(f"Max tokens: {results.get('max_tokens', 0)}")
        logger.info(f"Min tokens: {results.get('min_tokens', 0)}")
        logger.info(f"Estimated training cost: ${results['estimated_training_cost']:.4f}")
    
    if results["errors"]:
        logger.error(f"\nERRORS FOUND ({len(results['errors'])}):")
        for error in results["errors"]:
            logger.error(f"  - {error}")
    else:
        logger.success("No errors found! Dataset is ready for fine-tuning.")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    files_to_validate = [
        "data/fine_tune/legal_qa_train.jsonl",
        "data/fine_tune/legal_qa_val.jsonl"
    ]
    
    all_valid = True
    for filepath in files_to_validate:
        results = validate_file(filepath)
        print_validation_report(results)
        if results["errors"]:
            all_valid = False
    
    if all_valid:
        logger.success("\nAll files passed validation. Ready to proceed to Day 3!")
    else:
        logger.error("\nFix errors before proceeding to fine-tuning.")
