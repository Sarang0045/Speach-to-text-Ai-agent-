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
- LLM_BASE_URL
- LLM_API_KEY
- LLM_MODEL
- LLM_TEMPERATURE
- LLM_MAX_TOKENS
- LLM_TIMEOUT_SECONDS

Default cloud model:

- meta-llama/llama-3-8b-instruct (temperature: 0.2, max_tokens: 220)

## Run

```bash
streamlit run app.py
```

The app runs by default at http://localhost:8501

## Hybrid LLM Behavior

The central function in llm.py is `call_llm(prompt: str) -> str`.

It implements a simple local-first strategy:

1. Attempts to call local Ollama with 4-second timeout.
2. If local fails (connection error, timeout, invalid response), catches exception.
3. Falls back to cloud LLM via OpenRouter using meta-llama/llama-3-8b-instruct.
4. Logs which provider was used.
5. Returns "LLM unavailable" if both providers fail.

Public API functions using `call_llm()`:

- `detect_intent(text)` - Classifies user request into: create_file, write_code, summarize, or chat
- `generate_code(prompt)` - Generates Python code from natural language
- `extract_filename(text)` - Extracts or suggests a filename
- `summarize_llm(text)` - Summarizes text

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

- Check Ollama is running: `ollama serve`
- Verify OLLAMA_URL and model name in .env
- Increase OLLAMA_TIMEOUT_SECONDS if network is slow

### Cloud fallback not working

- Verify LLM_API_KEY is set in .env
- Verify LLM_BASE_URL is correct (https://openrouter.ai/api/v1)
- Verify LLM_MODEL is valid (meta-llama/llama-3-8b-instruct)
- Check network access to OpenRouter endpoint
- Inspect logs for specific error messages

### Import errors in editor

- Ensure VS Code is using venv/bin/python as interpreter
- Reinstall dependencies: `pip install -r requirements.txt`

## Security Notes

- Never commit .env.
- Keep API keys only in environment variables.
- Use .env.example as the shared template.

## License

MIT
