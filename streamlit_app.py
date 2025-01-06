import streamlit as st
import openai
import queue
import io
import wave

# -----------------------------------------------------------------------------
# 1. Set up your OpenAI credentials
# -----------------------------------------------------------------------------
# Use your OpenAI API key. Replace "YOUR_OPENAI_API_KEY" with your key.
client = OpenAI(api_key=st.secrets['OPENAI_API_Key'])

#-----------
#1.5 debugging
#------------
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def text_to_speech(text: str, voice: str = "onyx", model: str = "tts-1") -> bytes:
    try:
        # Call OpenAI TTS API
        logger.debug("Making TTS API call with text: %s", text)
        response = openai.Audio.create(
            text=text,
            voice=voice,
            model=model,
            response_format="pcm"
        )
        pcm_audio = response["audio_content"]
        wav_audio = pcm_to_wav(pcm_audio, sample_rate=24000)
        return wav_audio

    except AttributeError as e:
        logger.error("AttributeError: %s", e)
        st.error(f"Error generating TTS audio: {e}")
        return None
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        st.error(f"An unexpected error occurred: {e}")
        return None

# -----------------------------------------------------------------------------
# 2. Text-to-Speech Function: Use OpenAI's Streaming TTS API
# -----------------------------------------------------------------------------
def text_to_speech(text: str, voice: str = "onyx", model: str = "tts-1") -> bytes:
    """
    Convert text to speech using OpenAI's streaming TTS API and return WAV audio bytes.
    """
    try:
        # Initialize a queue to hold audio chunks
        audio_queue = queue.Queue()

        # Call the OpenAI TTS API with streaming response
        with openai.Audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="pcm",  # Return raw PCM data
        ) as response:
            # Process streaming audio chunks
            for audio_chunk in response.iter_bytes(1024):
                audio_queue.put(audio_chunk)

        # Combine all audio chunks into a single PCM byte stream
        pcm_audio = b"".join(list(audio_queue.queue))

        # Convert PCM audio to WAV for browser playback
        wav_audio = pcm_to_wav(pcm_audio, sample_rate=24000)
        return wav_audio

    except Exception as e:
        st.error(f"Error generating TTS audio: {e}")
        return None

# -----------------------------------------------------------------------------
# 3. PCM to WAV Conversion
# -----------------------------------------------------------------------------
def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000) -> bytes:
    """
    Convert raw PCM bytes into a WAV file in memory.
    """
    with io.BytesIO() as wav_io:
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(1)          # mono
            wav_file.setsampwidth(2)          # 16-bit audio
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_data)
        return wav_io.getvalue()

# -----------------------------------------------------------------------------
# 4. Generate Text Function
# -----------------------------------------------------------------------------
def generate_paragraph_on_penguins() -> str:
    """
    Generate a paragraph about penguins using OpenAI ChatCompletion API.
    """
    try:
        # Call OpenAI ChatCompletion API to generate text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[{"role": "user", "content": "Give me one paragraph on penguins"}],
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the response text
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        st.error(f"Error generating text: {e}")
        return ""

# -----------------------------------------------------------------------------
# 5. Streamlit UI
# -----------------------------------------------------------------------------
def main():
    st.title("OpenAI Text-to-Speech Demo")

    # Text input from the user
    user_text = st.text_area(
        "Enter the text to synthesize",
        value="Penguins are fascinating creatures that inhabit cold climates...",
    )

    # Voice selection
    voice_name = st.selectbox(
        "Select a voice",
        options=["Onyx", "Echo", "Alloy", "Fable", "Nova", "Shimmer"],  # Replace with actual available voices
        index=0
    )

    # Model selection (optional)
    model_name = st.radio(
        "Select model type",
        options=["tts-1", "tts-1-hd"],
        index=0,
        help="Choose 'tts-1' for real-time performance or 'tts-1-hd' for higher-quality audio."
    )

    if st.button("Generate Audio"):
        with st.spinner("Generating text..."):
            # Generate text if not manually provided
            paragraph = user_text or generate_paragraph_on_penguins()

        st.markdown("### Generated Text")
        st.write(paragraph)

        with st.spinner("Converting text to speech..."):
            audio_bytes = text_to_speech(paragraph, voice=voice_name, model=model_name)

        if audio_bytes:
            st.markdown("### Listen to the TTS Audio")
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.error("Failed to generate audio. Check the logs.")

if __name__ == "__main__":
    main()
