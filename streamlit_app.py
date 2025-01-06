import streamlit as st
from gtts import gTTS
from io import BytesIO
from pathlib import Path
from openai import OpenAI

client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!",
)
response.stream_to_file(speech_file_path)


st.title("Simple Text to Speech Converter")

text_input = st.text_area("Enter text to convert to speech", height=150)

st.sidebar.title("Upload your file")
uploaded_file=st.sidebar.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
  file_text = uploaded_file.read().decode("utf-8")

  st.subheader("text from Uploaded file")
  st.text(file_text)

  text_input += "\n\n" + file_text

language = st.selectbox("Select language",["en","fr","ru","hi","es"])

if st.button("Generate my speech"):
  if text_input:
    tts = gTTS(text_input, lang=language)

    audio_stream = BytesIO()

    tts.write_to_fp(audio_stream)

    st.audio(audio_stream)
  else:
    st.warning("Please enter some text or upload from device.")
