import streamlit as st
from stt import transcribe
from llm import detect_intent, generate_code, summarize_llm, extract_filename
from tools import create_file, write_code

st.title("🎤 Voice-Controlled AI Agent")

# Upload audio
audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])

if audio_file is not None:

    # Save file with correct extension
    file_extension = audio_file.name.split(".")[-1]
    temp_file_path = f"temp.{file_extension}"

    with open(temp_file_path, "wb") as f:
        f.write(audio_file.read())

    # ---------------- STEP 1: STT ----------------
    st.subheader("📝 Transcription")
    text = transcribe(temp_file_path)
    st.write(text)

    # ---------------- STEP 2: INTENT ----------------
    st.subheader("🧠 Detected Intent")
    intent = detect_intent(text)
    st.write(intent)

    # ---------------- STEP 3: ACTION ----------------
    st.subheader("⚙️ Action Plan")

    filename = None
    code = None
    result = None

    # -------- PREPARE ACTION --------

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

    # -------- CONFIRMATION + EXECUTION --------

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

    # ---------------- FINAL OUTPUT ----------------
    st.subheader("✅ Final Output")

    if result:
        st.write(result)