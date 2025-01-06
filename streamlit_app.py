import streamlit as st
import openai
from pathlib import Path

# 1) Set your API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_Key"]

# 2) Streamlit title
st.title("OpenAI Text-to-Speech Demo (Legacy)")

# 3) Button to generate TTS
if st.button("Generate Speech"):
    # 4) Call the TTS endpoint
    response = openai.Audio.speech.create(
        model="tts-1",
        voice="nova",
        input="Today is a wonderful day but very cold in Helsinki, Finland!",
    )

    # 5) Immediately play the MP3 in Streamlit
    st.audio(response.content, format="audio/mp3")

    # 6) Optionally write the MP3 to a file and let the user download
    tts_file_path = Path(__file__).parent / "output.mp3"
    with open(tts_file_path, "wb") as f:
        f.write(response.content)

    with open(tts_file_path, "rb") as f:
        st.download_button(
            label="Download MP3",
            data=f,
            file_name="openai-tts-output.mp3"
        )
