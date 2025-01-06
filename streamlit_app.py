import streamlit as st
import openai
from openai import OpenAI
from gtts import gTTS
from io import BytesIO

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_Key"]

st.title("Simple Text to Speech Converter")

# Text area for user input
text_input = st.text_area("Enter text to convert to speech", height=150)

st.sidebar.title("Upload your file")
uploaded_file = st.sidebar.file_uploader("Choose a .txt file", type="txt")

# If a file is uploaded, read its content and append to text_input
if uploaded_file is not None:
    file_text = uploaded_file.read().decode("utf-8")
    st.subheader("Text from uploaded file")
    st.text(file_text)
    text_input += "\n\n" + file_text

# Let the user pick which TTS engine to use
tts_service = st.selectbox("Select TTS Service", ["OpenAI TTS", "Google TTS"])

# Only show language choices if using Google TTS
if tts_service == "Google TTS":
    language = st.selectbox("Select language", ["en", "fr", "ru", "hi", "es"])

# Button to generate speech
if st.button("Generate my speech"):
    if not text_input.strip():
        st.warning("Please enter some text or upload from device.")
    else:
        if tts_service == "OpenAI TTS":
            # Use new OpenAI client-based approach
            client = OpenAI(api_key=openai.api_key)
            # Make the request to the TTS endpoint
            response = client.audio.speech.create(
                model="tts-1",    # Example model name
                voice="alloy",    # Example voice name
                input=text_input,
            )

            # Stream TTS output to an in-memory buffer
            audio_stream = BytesIO()
            response.stream_to_file(audio_stream)
            audio_stream.seek(0)

            st.audio(audio_stream, format="audio/mp3")
        else:
            # Fallback or alternative: Google TTS
            tts = gTTS(text_input, lang=language)
            audio_stream = BytesIO()
            tts.write_to_fp(audio_stream)
            audio_stream.seek(0)

            st.audio(audio_stream)
