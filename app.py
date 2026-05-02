import streamlit as st
from stt import transcribe
from llm import detect_intent, generate_code, summarize_llm, extract_filename
from tools import create_file, write_code
from streamlit_mic_recorder import mic_recorder

st.title("🎤 Voice-Controlled AI Agent")

# ---------------- 🎤 MIC RECORDING ----------------
st.subheader("🎤 Record Your Voice")

audio_data = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    key="recorder"
)

# Show recorded audio (optional)
if audio_data is not None:
    st.audio(audio_data["bytes"])


# ---------------- 📁 FILE UPLOAD ----------------
audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])


# ---------------- 🎯 HANDLE BOTH INPUTS ----------------
temp_file_path = None

if audio_file is not None:
    file_extension = audio_file.name.split(".")[-1]
    temp_file_path = f"temp.{file_extension}"

    with open(temp_file_path, "wb") as f:
        f.write(audio_file.read())

elif audio_data is not None:
    temp_file_path = "recorded.wav"

    with open(temp_file_path, "wb") as f:
        f.write(audio_data["bytes"])


# ---------------- 🚀 RUN PIPELINE ----------------
if temp_file_path is not None:

    # STEP 1: STT
    st.subheader("📝 Transcription")
    text = transcribe(temp_file_path)
    st.write(text)

    # STEP 2: Intent
    st.subheader("🧠 Detected Intent")
    intent = detect_intent(text)
    st.write(intent)

    # STEP 3: Action Plan
    st.subheader("⚙️ Action Plan")

    filename = None
    code = None
    result = None

    # -------- PREPARE --------
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

    # -------- CONFIRMATION --------
    if intent in ["create_file", "write_code"]:
        if st.button("✅ Confirm Action"):

            try:
                if intent == "create_file":
                    result = create_file(filename)

                elif intent == "write_code":
                    result = write_code(filename, code)

                st.success(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # -------- FINAL OUTPUT --------
    st.subheader("✅ Final Output")

    if result:
        st.write(result)