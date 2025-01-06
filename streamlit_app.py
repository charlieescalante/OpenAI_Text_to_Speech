import streamlit as st
import openai
import io
import wave
import re

# -----------------------------------------------------------------------------
# 1. Set up your OpenAI credentials
# -----------------------------------------------------------------------------
# Option A: Use an environment variable (recommended).
#    import os
#    openai.api_key = os.getenv("OPENAI_API_KEY")
#
# Option B: Use Streamlit secrets (if deploying on Streamlit Cloud).
#    openai.api_key = st.secrets["OPENAI_API_KEY"]
#
# For local testing, you can just do:
#    openai.api_key = "sk-..."

# Uncomment one of these to set your key:
# openai.api_key = st.secrets["OPENAI_API_KEY"]
# OR:
# openai.api_key = "YOUR_OPENAI_KEY_HERE"

# -----------------------------------------------------------------------------
# 2. Helper function: Convert raw PCM bytes into a WAV file in memory.
# -----------------------------------------------------------------------------
def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000) -> bytes:
    """
    Takes raw 16-bit PCM data and returns a WAV file as bytes.
    """
    with io.BytesIO() as wav_io:
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(1)          # mono
            wav_file.setsampwidth(2)          # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_data)
        return wav_io.getvalue()

# -----------------------------------------------------------------------------
# 3. Helper function: Call OpenAI to get Text (ChatCompletion) or TTS
# -----------------------------------------------------------------------------
def generate_paragraph_on_penguins() -> str:
    """
    Ask OpenAI's completion endpoint for a paragraph on penguins.
    Feel free to modify the prompt or parameters as you like.
    """
    # Example using ChatCompletion API with GPT-3.5 or GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[{"role": "user", "content": "Give me one paragraph on penguins"}],
        max_tokens=150,
        temperature=0.7,
    )
    # Extract text
    text_response = response["choices"][0]["message"]["content"]
    return text_response.strip()

def text_to_speech(text: str) -> bytes:
    """
    Convert text to speech using OpenAI's TTS (if you have access to that API).
    If OpenAI's TTS endpoint is not available in your account, you'll need
    a different TTS provider or a library like ElevenLabs, Azure, etc.

    This function returns raw PCM bytes from the TTS.
    Then we'll convert it to WAV for web playback.
    """
    # Pseudocode for OpenAI TTS (the official library does not yet have a stable TTS endpoint).
    #
    # If you have a custom TTS endpoint, it might look like this:
    #
    # response = openai.Audio.synthesize(
    #     text=text,
    #     voice="onyx",          # Example voice name
    #     response_format="pcm", # We want raw PCM
    #     model="tts-1"          # Example model name
    # )
    #
    # raw_pcm_data = response.audio_content  # Hypothetical attribute
    #
    # For demonstration, we'll just return empty bytes or a dummy beep.
    # Remove this stub and replace it with your actual TTS call:
    
    # ----- DUMMY Implementation (Replace with real TTS code) -----
    # Just generate 1 second of silence in 16-bit PCM at 24kHz:
    import struct
    sample_rate = 24000
    duration_sec = 1
    num_samples = sample_rate * duration_sec
    silent_pcm = b"".join([struct.pack("<h", 0) for _ in range(num_samples)])
    # -------------------------------------------------------------
    
    # If you have actual TTS, you'd do something like:
    # raw_pcm_data = real_api_call_that_returns_pcm(text)
    raw_pcm_data = silent_pcm

    # Convert PCM to WAV
    wav_bytes = pcm_to_wav(raw_pcm_data, sample_rate=24000)
    return wav_bytes

# -----------------------------------------------------------------------------
# 4. The Streamlit UI
# -----------------------------------------------------------------------------
def main():
    st.title("OpenAI TTS Demo")

    # A button to generate text about penguins
    if st.button("Generate Text about Penguins"):
        with st.spinner("Generating text..."):
            paragraph = generate_paragraph_on_penguins()
        
        # Display the text
        st.markdown("### Generated Text")
        st.write(paragraph)

        # Convert that paragraph to speech
        with st.spinner("Converting text to speech..."):
            wav_file_bytes = text_to_speech(paragraph)

        # Display an audio player in the browser
        st.markdown("### Listen to the TTS Audio")
        st.audio(wav_file_bytes, format="audio/wav")

if __name__ == "__main__":
    main()
