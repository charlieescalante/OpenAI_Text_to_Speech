import streamlit as st
from openai import OpenAI
from io import BytesIO

# Set your OpenAI API key
openai.api_key = st.secrets['OPENAI_API_Key']

st.title("Simple Text to Speech Converter (OpenAI)")

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

# Button to trigger speech generation
if st.button("Generate my speech"):
    if text_input.strip():
        # Call OpenAI TTS
        response = openai.Audio.speech.create(
            model="tts-1",       # Example model name
            voice="alloy",       # Example voice name
            input=text_input
        )

        # Write the TTS result to an in-memory buffer
        audio_stream = BytesIO()
        response.stream_to_file(audio_stream)

        # Reset to the beginning of the buffer so Streamlit can read it
        audio_stream.seek(0)

        # Play the audio in Streamlit
        st.audio(audio_stream, format="audio/mp3")
    else:
        st.warning("Please enter some text or upload from device.")
