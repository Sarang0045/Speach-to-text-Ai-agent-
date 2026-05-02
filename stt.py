import whisper
import os

# Lazy loading model to avoid memory crash on deployment
_model = None

def get_model():
    global _model
    if _model is None:
        # Use persistent temp directory to avoid repeated downloads
        model_dir = "/tmp/whisper"
        os.makedirs(model_dir, exist_ok=True)

        # Use smaller model for cloud (Render free tier)
        _model = whisper.load_model("tiny", download_root=model_dir)
    return _model

def transcribe(audio_path):
    try:
        model = get_model()
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error: {str(e)}"