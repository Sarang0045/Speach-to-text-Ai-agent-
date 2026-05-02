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
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "4"))

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT_SECONDS", "12"))

INTENTS = {"create_file", "write_code", "summarize", "chat"}


def _call_local_ollama(prompt):
    """Try to get response from local Ollama instance."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=OLLAMA_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("response", "").strip()
    if not text:
        raise ValueError("Empty response from Ollama")
    return text


def _call_cloud_llm(prompt):
    """Call cloud LLM via OpenRouter."""
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY not set")

    response = requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {LLM_API_KEY}"},
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 220,
        },
        timeout=LLM_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"]["content"].strip()
    if not text:
        raise ValueError("Empty response from cloud LLM")
    return text


def call_llm(prompt: str) -> str:
    """Call LLM: try local Ollama first, fallback to cloud."""
    try:
        result = _call_local_ollama(prompt)
        logger.info("Using local Ollama")
        return result
    except Exception as e:
        logger.warning(f"Local Ollama failed, trying cloud: {e}")

    try:
        result = _call_cloud_llm(prompt)
        logger.info("Using cloud LLM")
        return result
    except Exception as e:
        logger.error(f"Both LLM sources failed: {e}")
        return "LLM unavailable"


def detect_intent(text: str) -> str:
    """Detect user intent from text."""
    prompt = f"Classify this request into one category: create_file, write_code, summarize, or chat. Request: '{text}'. Reply with just the category name."
    response = call_llm(prompt)
    intent = response.lower().strip()
    return intent if intent in INTENTS else "chat"


def generate_code(prompt: str) -> str:
    """Generate code from prompt."""
    code_prompt = f"Generate Python code for: {prompt}. Return only the code without explanation."
    return call_llm(code_prompt)


def extract_filename(text: str) -> str:
    """Extract filename from text."""
    filename_prompt = f"Extract a short filename from this: '{text}'. Reply with just the filename (no path). If unclear, suggest 'output.txt'."
    name = call_llm(filename_prompt).strip()
    if "." not in name:
        name = f"{name}.txt"
    return name or "output.txt"


def summarize_llm(text: str) -> str:
    """Summarize text using LLM."""
    summary_prompt = f"Summarize this briefly in 2-3 sentences: {text[:500]}"
    return call_llm(summary_prompt)