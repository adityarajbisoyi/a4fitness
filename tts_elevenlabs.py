from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def speak(text):
    audio = elevenlabs.text_to_speech.convert(
        text=f'{text}',
        voice_id="SAz9YHcvj6GT2YYXdXww",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)
speak("hello There")
