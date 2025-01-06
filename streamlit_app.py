import streamlit as st
import openai
from pathlib import Path

# 1) Set the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 2) Create the client object
client = openai.OpenAI()  # (only works for openai<1.0.0 TTS)

# 3) Title
st.title("OpenAI Text-to-Speech Demo (Legacy)")

# 4) Button
if st.button("Generate Speech"):
    # 5) TTS request
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input="Today is a wonderful day but very cold in Helsinki, Finland!",
    )

    # 6) Immediately play the MP3
    st.audio(response.content, format="audio/mp3")

    # 7) Save to file and offer download
    tts_file_path = Path(__file__).parent / "output.mp3"
    with open(tts_file_path, "wb") as f:
        f.write(response.content)
    with open(tts_file_path, "rb") as f:
        st.download_button("Download MP3", f, file_name="openai-tts-output.mp3")
