import streamlit as st
from llm import detect_intent, extract_filename, generate_code, summarize_llm
from stt import transcribe
from streamlit_mic_recorder import mic_recorder
from tools import create_file, write_code


def _save_temp_audio(path, data):
    with open(path, "wb") as file_obj:
        file_obj.write(data)
    return path

st.title("🎤 Voice-Controlled AI Agent")
st.subheader("🎤 Record Your Voice")

audio_data = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    key="recorder"
)
if audio_data is not None:
    st.audio(audio_data["bytes"])

audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])

temp_file_path = None

if audio_file is not None:
    extension = audio_file.name.split(".")[-1]
    temp_file_path = _save_temp_audio(f"temp.{extension}", audio_file.read())
elif audio_data is not None:
    temp_file_path = _save_temp_audio("recorded.wav", audio_data["bytes"])

if temp_file_path is not None:
    st.subheader("📝 Transcription")
    text = transcribe(temp_file_path)
    st.write(text)

    if text.startswith("Error:"):
        st.stop()

    st.subheader("🧠 Detected Intent")
    intent = detect_intent(text)
    st.write(intent)

    st.subheader("⚙️ Action Plan")

    filename = None
    code = None
    result = None

    if intent == "create_file":
        filename = extract_filename(text)
        st.write(f"📁 File to be created: {filename}")

    elif intent == "write_code":
        filename = extract_filename(text)
        code = generate_code(text)

        st.write(f"📁 File: {filename}")
        st.subheader("💻 Generated Code")
        st.code(code, language="python")

    elif intent == "summarize":
        result = summarize_llm(text)
        st.write(result)

    else:
        result = "Chat response (not implemented yet)"
        st.write(result)

    if intent in {"create_file", "write_code"} and st.button("✅ Confirm Action"):
        try:
            if intent == "create_file":
                result = create_file(filename)
            else:
                result = write_code(filename, code)
            st.success(result)
        except Exception as exc:
            st.error(f"Error: {exc}")

    st.subheader("✅ Final Output")

    if result:
        st.write(result)