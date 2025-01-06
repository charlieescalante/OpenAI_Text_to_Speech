import streamlit as st
import openai
import io

# 1) Set the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_Key"]

# 2) Title of the app
st.title("OpenAI Text-to-Speech Demo")

# 3) Button to run text-to-speech
if st.button("Generate Steve Jobs MP3"):
    # 4) Call the OpenAI TTS endpoint
    response = openai.Audio.speech.create(
        model="tts-1",          # "tts-1" is currently in limited or early access
        voice="echo",
        input="Your time is limited, so don't waste it living someone else's life. "
              "Don't be trapped by dogma - which is living with the results of other people's thinking."
    )

    # 5) Stream the MP3 in memory
    mp3_data = io.BytesIO(response.content)
    
    # 6) Play the generated audio in Streamlit
    st.audio(mp3_data, format="audio/mp3")

    # 7) Optionally, save to a local file
    with open("steve_jobs_generated.mp3", "wb") as f:
        f.write(response.content)

    st.success("MP3 generated and played above!")
