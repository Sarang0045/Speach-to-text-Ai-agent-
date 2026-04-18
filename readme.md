# 🎤 Voice-Controlled AI Agent

A powerful voice-activated AI agent application that converts speech to text, understands user intent, and performs automated actions like creating files and generating code. Built with Streamlit, Whisper, and Ollama.

## 🌟 Features

- **Speech-to-Text Transcription**: Convert audio files (WAV, MP3, M4A) to text using OpenAI's Whisper model
- **Intent Detection**: Intelligent intent classification using Ollama's Llama3 model
  - `create_file`: Create new files
  - `write_code`: Generate code snippets
  - `summarize`: Summarize text
  - `chat`: General conversation (future implementation)
- **Automated Code Generation**: Generate Python code based on voice commands
- **File Management**: Create and write files to the output directory
- **User-Friendly Interface**: Interactive web interface powered by Streamlit

## 🏗️ Architecture

The system works in 4 main steps:

```
Audio File Upload
    ↓
Step 1: Speech-to-Text (Transcription)
    ↓
Step 2: Intent Detection (Understanding user intent)
    ↓
Step 3: Action Preparation (Generate code or plan action)
    ↓
Step 4: Execution & Confirmation (Create files or write code)
```

## 📋 Project Structure

```
STT-AI-AGENT/
├── app.py              # Main Streamlit application
├── stt.py              # Speech-to-text transcription module (Whisper)
├── llm.py              # LLM functions for intent detection and code generation
├── tools.py            # File creation and manipulation utilities
├── utils.py            # Utility functions (currently empty)
├── test_llm.py         # Tests for LLM functions
├── test_tools.py       # Tests for file tools
├── requirements.txt    # Project dependencies
├── readme.md           # Project documentation
└── output/             # Output directory for generated files
```

## 🛠️ Technologies Used

- **Streamlit**: Web framework for building the UI
- **OpenAI Whisper**: Speech-to-text model for audio transcription
- **Ollama**: Local LLM framework running Llama3
- **Python 3.8+**: Core programming language
- **Requests**: HTTP client for API calls to Ollama

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running with Llama3 model loaded
- Virtual environment management (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**

```bash
cd STT-AI-AGENT
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Ensure Ollama is running**

```bash
ollama serve
# In another terminal: ollama pull llama3
```

## ⚙️ Configuration

### Ollama API Endpoint

The application connects to Ollama at `http://localhost:11434/api/generate`. Make sure Ollama is running on this address before starting the app.

### Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- M4A (.m4a)

### Output Directory

Generated files are saved to the `output/` directory. The directory is created automatically if it doesn't exist.

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

This will open the application in your default browser at `http://localhost:8501`

### Basic Workflow

1. **Upload Audio**: Click "Upload Audio File" and select your audio file
2. **View Transcription**: The app transcribes your speech to text
3. **Check Intent**: The AI detects what action you want (create file, write code, etc.)
4. **Review Action**: Preview the action that will be performed
5. **Confirm & Execute**: Click "Confirm Action" to execute the action

### Example Voice Commands

- **Create File**: "Create a file named my_document.txt"
- **Write Code**: "Write Python code for a hello world program and save it as hello.py"
- **Summarize**: "Summarize the following text: [your text here]"
- **Chat**: "Hello, how are you?" (feature coming soon)

## 📝 Module Documentation

### stt.py

Handles speech-to-text conversion using OpenAI's Whisper model.

**Function**: `transcribe(audio_path)`

- Input: Path to audio file
- Output: Transcribed text or error message

### llm.py

Contains all LLM-related functions for intent detection and code generation.

**Functions**:

- `detect_intent(text)`: Classifies user intent
- `generate_code(prompt)`: Generates Python code based on prompt
- `extract_filename(text)`: Extracts filename from user text
- `summarize_llm(text)`: Summarizes input text

### tools.py

Provides file management utilities.

**Functions**:

- `create_file(filename)`: Creates an empty file in output/
- `write_code(filename, code)`: Writes code to a file in output/
- `summarize(text)`: Simple text summarization (basic version)

### app.py

Main Streamlit application containing the UI and orchestration logic.

## 🧪 Testing

Run the included test files to verify functionality:

```bash
# Test LLM functions
python test_llm.py

# Test file tools
python test_tools.py
```

## 🔄 Workflow Example

**Voice Input**: "Create a Python file that prints hello world and name it greet.py"

1. **Transcription**: Converts audio to text
2. **Intent Detection**: Identifies as "write_code"
3. **Filename Extraction**: Extracts "greet.py"
4. **Code Generation**: Generates Python code
5. **User Confirmation**: Shows preview
6. **Execution**: Creates file in output/greet.py
7. **Result**: File created successfully ✅

## 📈 Future Improvements

- [ ] Support for additional intents (chat, data analysis, etc.)
- [ ] Enhanced error handling and recovery
- [ ] File editing capabilities (modify existing files)
- [ ] Support for multiple programming languages
- [ ] Conversation history tracking
- [ ] Voice output/Text-to-Speech response
- [ ] Database integration for storing generated files
- [ ] Advanced code generation with multiple file support
- [ ] Performance optimization and caching
- [ ] Unit tests expansion and CI/CD pipeline

## ⚠️ Troubleshooting

### Ollama Connection Error

- Ensure Ollama is running: `ollama serve`
- Check if Llama3 is installed: `ollama pull llama3`

### Audio Upload Issues

- Verify audio file format is WAV, MP3, or M4A
- Check file size isn't too large
- Ensure microphone/audio source is working properly

### Generated Files Not Appearing

- Check that the `output/` directory exists
- Verify write permissions in the project directory
- Look for error messages in the Streamlit console

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a voice-controlled AI agent project demonstrating:

- Speech recognition capabilities
- Natural language understanding
- Automated task execution
- File generation and management

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review test files for usage examples
3. Verify all dependencies are installed correctly
4. Ensure Ollama and required models are properly configured

---

**Happy voice commanding! 🎙️**
# Speach-to-text-Ai-agent-
