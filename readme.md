# Voice-Controlled AI Agent

A Streamlit-based voice AI agent that transcribes audio, detects intent, generates code, and writes files.

This project now uses a hybrid LLM architecture:

- Primary: local Ollama model
- Fallback: OpenRouter cloud model when local fails

## Features

- Speech-to-text transcription with OpenAI Whisper
- Hybrid LLM routing with automatic fallback
  - Tries local Ollama first
  - Falls back to OpenRouter on timeout, connection errors, or invalid local response
- Intent classification
  - create_file
  - write_code
  - summarize
  - chat
- Code generation from natural language
- File creation and write tools in output directory
- Streamlit UI with upload and microphone input

## Architecture

```text
Audio Input (Upload/Mic)
        -> Whisper Transcription
        -> Intent Detection (Hybrid LLM)
        -> Action Planning
        -> User Confirmation
        -> File Creation/Code Write/Summary
```

## Project Structure

```text
STT-AI-AGENT/
    app.py
    stt.py
    llm.py
    tools.py
    utils.py
    requirements.txt
    .env
    .env.example
    .gitignore
    readme.md
    output/
```

## Tech Stack

- Python 3.8+
- Streamlit
- OpenAI Whisper
- Ollama
- OpenRouter
- requests
- python-dotenv

## Installation

1. Move into the project directory.

```bash
cd STT-AI-AGENT
```

2. Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Start Ollama and pull the model.

```bash
ollama serve
# in another terminal
ollama pull llama3
```

## Environment Configuration

1. Create your local environment file from the example.

```bash
cp .env.example .env
```

2. Set your OpenRouter API key in .env.

Required variables:

- OLLAMA_URL
- OLLAMA_MODEL
- OLLAMA_TIMEOUT_SECONDS
- OPENROUTER_API_KEY
- OPENROUTER_URL
- OPENROUTER_MODEL
- OPENROUTER_TIMEOUT_SECONDS

Default fallback model:

- mistralai/mistral-7b-instruct

## Run

```bash
streamlit run app.py
```

The app runs by default at http://localhost:8501

## Hybrid LLM Behavior

The central function in llm.py is call_llm(prompt: str) -> str.

It does the following:

1. Calls local Ollama with a short timeout.
2. If local fails, calls OpenRouter.
3. Logs which provider was used.
4. Returns a safe fallback message if both fail.

Functions using call_llm:

- detect_intent(text)
- generate_code(prompt)
- extract_filename(text)
- summarize_llm(text)

## Usage Flow

1. Upload audio or record from the microphone.
2. Transcribe audio to text.
3. Detect intent with hybrid LLM routing.
4. Review generated action.
5. Confirm and execute.

## Testing

If tests are available in your workspace:

```bash
python test_llm.py
python test_tools.py
```

## Troubleshooting

### Local model not responding

- Check Ollama is running.
- Verify OLLAMA_URL and model name in .env.
- Increase OLLAMA_TIMEOUT_SECONDS if needed.

### Cloud fallback not working

- Verify OPENROUTER_API_KEY is set.
- Verify OPENROUTER_MODEL is valid.
- Check network access to OpenRouter endpoint.

### Import errors in editor

- Ensure VS Code is using venv/bin/python as interpreter.
- Reinstall dependencies with pip install -r requirements.txt.

## Security Notes

- Never commit .env.
- Keep API keys only in environment variables.
- Use .env.example as the shared template.

## License

MIT
