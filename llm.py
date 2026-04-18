import requests

def detect_intent(text):
    """
    Takes user text
    Returns intent (create_file / write_code / summarize / chat)
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

    response = requests.post(
        "http://localhost:11434/api/generate",  
        json={
            "model": "llama3",    
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    intent = result["response"].strip()

    return intent

def generate_code(prompt):
    """
    Generates code using Ollama
    """

    full_prompt = f"""
    Generate code for the following request:
    {prompt}

    Only return code. No explanation.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def extract_filename(text):
    """
    Extract filename from user text
    """

    prompt = f"""
    Extract the filename from this text:
    {text}

    If no filename, return 'output.txt'
    Only return filename.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


def summarize_llm(text):
    prompt = f"""
    Summarize this text:
    {text}

    Keep it short and clear.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()