import whisper

# Lazy loading model to avoid memory crash on deployment
_model = None

def get_model():
    global _model
    if _model is None:
        # Use smaller model for cloud (Render free tier)
        _model = whisper.load_model("tiny")
    return _model

def transcribe(audio_path):
    try:
        model = get_model()
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error: {str(e)}"