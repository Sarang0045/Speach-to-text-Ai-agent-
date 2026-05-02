import logging
import os

import requests

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv is not None:
    load_dotenv()


logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
LOCAL_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "4"))

OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
OPENROUTER_FALLBACK_MODEL = os.getenv("OPENROUTER_FALLBACK_MODEL", "openrouter/auto")
OPENROUTER_TIMEOUT_SECONDS = float(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "20"))


def _extract_openrouter_text_completion(data):
    """Safely extract text from OpenRouter completions-style responses."""
    choices = data.get("choices") if isinstance(data, dict) else None
    if not isinstance(choices, list) or not choices:
        raise ValueError("OpenRouter completions response missing 'choices'.")

    first_choice = choices[0] if isinstance(choices[0], dict) else None
    if not isinstance(first_choice, dict):
        raise ValueError("OpenRouter completions response has invalid first choice.")

    text = first_choice.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()

    raise ValueError("OpenRouter completions response text is empty or invalid.")


def _extract_openrouter_content(data):
    """Safely extract text content from OpenRouter chat completion response."""
    choices = data.get("choices") if isinstance(data, dict) else None
    if not isinstance(choices, list) or not choices:
        raise ValueError("OpenRouter response missing 'choices'.")

    first_choice = choices[0] if isinstance(choices[0], dict) else None
    if not isinstance(first_choice, dict):
        raise ValueError("OpenRouter response has invalid first choice.")

    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise ValueError("OpenRouter response missing 'message'.")

    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content.strip()

    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict):
                text_part = part.get("text")
                if isinstance(text_part, str) and text_part.strip():
                    text_parts.append(text_part.strip())
        if text_parts:
            return "\n".join(text_parts)

    raise ValueError("OpenRouter response content is empty or invalid.")


def _call_local_ollama(prompt):
    """Call local Ollama model and return text or raise an exception."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=LOCAL_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    data = response.json()
    text = data.get("response") if isinstance(data, dict) else None
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Ollama response missing valid 'response' text.")

    return text.strip()


def _call_openrouter_chat(prompt, model):
    """Call OpenRouter chat-completions endpoint and return text."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=OPENROUTER_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    data = response.json()
    return _extract_openrouter_content(data)


def _chat_to_completions_url(url):
    """Map /chat/completions endpoint to /completions endpoint."""
    return url.replace("/chat/completions", "/completions")


def _call_openrouter_completions(prompt, model):
    """Call OpenRouter completions endpoint and return text."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        _chat_to_completions_url(OPENROUTER_URL),
        headers=headers,
        json={
            "model": model,
            "prompt": prompt,
        },
        timeout=OPENROUTER_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    data = response.json()
    return _extract_openrouter_text_completion(data)


def _call_openrouter(prompt):
    """Call OpenRouter with compatibility retries on model/endpoint issues."""
    try:
        return _call_openrouter_chat(prompt, OPENROUTER_MODEL)
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code != 404:
            raise
        logger.warning(
            "OpenRouter model '%s' unavailable; retrying with fallback model.",
            OPENROUTER_MODEL,
        )

    try:
        return _call_openrouter_chat(prompt, OPENROUTER_FALLBACK_MODEL)
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code != 404:
            raise
        logger.warning("OpenRouter chat retry failed with 404; trying completions endpoint.")

    return _call_openrouter_completions(prompt, OPENROUTER_FALLBACK_MODEL)


def _keyword_intent_fallback(text):
    """Deterministic intent fallback for cases where LLM output is unavailable/noisy."""
    text_lower = (text or "").lower()

    if any(token in text_lower for token in ["summarize", "summary", "tl;dr"]):
        return "summarize"

    if any(
        token in text_lower
        for token in [
            "write code",
            "code",
            "program",
            "function",
            "algorithm",
            "binary search",
            "java",
            "python",
            "c++",
            "javascript",
        ]
    ):
        return "write_code"

    if any(token in text_lower for token in ["create file", "make file", "new file"]):
        return "create_file"

    return "chat"


def call_llm(prompt: str) -> str:
    """Call local Ollama first, then fallback to OpenRouter if local fails."""
    if not isinstance(prompt, str) or not prompt.strip():
        return "LLM error: Prompt must be a non-empty string."

    try:
        result = _call_local_ollama(prompt)
        logger.info("LLM provider used: local")
        return result
    except (requests.exceptions.RequestException, ValueError) as local_error:
        logger.warning("Local LLM failed, falling back to cloud: %s", local_error)

    try:
        result = _call_openrouter(prompt)
        logger.info("LLM provider used: cloud")
        return result
    except (requests.exceptions.RequestException, ValueError, RuntimeError) as cloud_error:
        logger.error("Cloud fallback failed: %s", cloud_error)
        return (
            "LLM unavailable right now: local model failed and cloud fallback is not reachable. "
            "Please try again in a moment."
        )


def detect_intent(text):
    """
    Takes user text.
    Returns one of: create_file / write_code / summarize / chat.
    """
    prompt = f"""
    You are an AI intent classifier.

    Classify the user request into ONE of these:
    - create_file
    - write_code
    - summarize
    - chat

    ONLY return the category name. No explanation.

    User input:
    {text}
    """

    raw_intent = call_llm(prompt).strip().lower()
    valid_intents = {"create_file", "write_code", "summarize", "chat"}

    if raw_intent in valid_intents:
        return raw_intent

    for intent in valid_intents:
        if intent in raw_intent:
            return intent

    return _keyword_intent_fallback(text)


def generate_code(prompt):
    """Generate code from user request using hybrid LLM routing."""
    full_prompt = f"""
    Generate code for the following request:
    {prompt}

    Only return code. No explanation.
    """
    return call_llm(full_prompt)


def extract_filename(text):
    """Extract filename from user text."""
    prompt = f"""
    Extract the filename from this text:
    {text}

    If no filename, return 'output.txt'
    Only return filename.
    """
    result = call_llm(prompt).strip()
    return result if result else "output.txt"


def summarize_llm(text):
    """Summarize text using hybrid LLM routing."""
    prompt = f"""
    Summarize this text:
    {text}

    Keep it short and clear.
    """
    return call_llm(prompt)