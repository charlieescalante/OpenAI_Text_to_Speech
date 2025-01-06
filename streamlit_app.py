import streamlit as st
from pathlib import Path
from openai import OpenAI
from io import BytesIO
client = OpenAI(api_key=openai.api_key)

speech_file_path = "steve_jobs_generated.mp3"
response = client.audio.speech.create(
    # model="tts-1",
    model="tts-1",
    # voice="alloy",
    voice = "echo",
    # voice = "fable",
    # voice = "onyx",
    # voice = "nova"
    # voice = "shimmer",
    input="Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma - which is what"
)

response.stream_to_file(speech_file_path)
