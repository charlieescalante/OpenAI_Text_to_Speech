import streamlit as st
from pathlib import Path
from openai import OpenAI

# 1. Create the client
client = OpenAI()

# 1) Set the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_Key"]

# 2. Title
st.title("OpenAI Text-to-Speech Demo (Legacy)")

# 3. A button to generate TTS
if st.button("Generate Speech"):
    # 4. Make the TTS request
    response = client.audio.speech.create(
        model="tts-1",  
        voice="nova",  
        input="Today is a wonderful day but very cold in Helsinki, Finland!"
    )
    
    # 5. The response includes audio in response.content
    #    We can play it directly in Streamlit:
    st.audio(response.content, format="audio/mp3")

    # 6. Optionally, you could allow a download:
    #    (a) write the content to a local file
    tts_file_path = Path(__file__).parent / "output.mp3"
    with open(tts_file_path, "wb") as f:
        f.write(response.content)
    #    (b) provide a download link
    with open(tts_file_path, "rb") as f:
        st.download_button("Download MP3", f, file_name="openai-tts-output.mp3")
