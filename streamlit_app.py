import streamlit as st
import openai
from openai import OpenAI
from io import BytesIO

# Set your API key. 
# If you're using Streamlit's Secrets Manager, do something like:
# openai.api_key = st.secrets["OPENAI_API_Key"]
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

def main():
    st.title("OpenAI TTS Simple Demo")
    text_input = st.text_input("Enter text to read out loud", value="Hello, world!")

    if st.button("Read with OpenAI TTS"):
        if text_input.strip():
            # 1. Create client
            client = OpenAI(api_key=openai.api_key)

            # 2. Request TTS generation
            response = client.audio.speech.create(
                model="tts-1",   # or the appropriate TTS model
                voice="alloy",   # change to another voice if you'd like
                input=text_input
            )

            # 3. Build an in-memory MP3 from the response
            audio_data = BytesIO()
            for chunk in response.iter_raw():  # yields bytes in chunks
                audio_data.write(chunk)
            audio_data.seek(0)

            # 4. Play the audio in the app
            st.audio(audio_data, format="audio/mp3")
        else:
            st.warning("Please enter some text first.")

if __name__ == "__main__":
    main()
