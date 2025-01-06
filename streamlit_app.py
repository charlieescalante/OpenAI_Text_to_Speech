import streamlit as st
from pathlib import Path
from openai import OpenAI  # We only have the "OpenAI" class here

# 1) Create the client, passing in your secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_Key"])

# 2) Title
st.title("OpenAI Text-to-Speech Demo (Legacy)")

# 3) A button to generate TTS
if st.button("Generate Speech"):
    # 4) Make the TTS request
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input="Today is a wonderful day but very cold in Helsinki, Finland!",
    )

    # 5) Immediately play the MP3 in Streamlit
    st.audio(response.content, format="audio/mp3")

    # 6) Optionally, write to a file and provide a download link
    tts_file_path = Path(__file__).parent / "output.mp3"
    with open(tts_file_path, "wb") as f:
        f.write(response.content)
    with open(tts_file_path, "rb") as f:
        st.download_button("Download MP3", f, file_name="openai-tts-output.mp3")
