"""
Test script for AI Voice Coach
"""

import sys
import io
from dotenv import load_dotenv
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# Verify API keys
gemini_key = os.getenv("GEMINI_LLM_API_KEY")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

print("🔍 Checking API Keys...")
print(f"Gemini API Key: {'✅ Found' if gemini_key else '❌ Missing'}")
print(f"ElevenLabs API Key: {'✅ Found' if elevenlabs_key else '❌ Missing'}")

if not gemini_key or not elevenlabs_key:
    print("\n❌ Missing API keys in .env file!")
    exit(1)

print("\n🧪 Testing imports...")
try:
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    import google.generativeai as genai
    print("✅ google-generativeai imported (Note: Package is deprecated but still functional)")
except ImportError:
    print("❌ google-generativeai not installed. Run: pip install google-generativeai")
    exit(1)

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs.play import play
    print("✅ elevenlabs imported")
except ImportError as e:
    print(f"❌ elevenlabs not installed: {e}")
    exit(1)

try:
    import speech_recognition as sr
    print("✅ speech_recognition imported")
except ImportError:
    print("❌ speech_recognition not installed")
    exit(1)

print("\n🤖 Testing Gemini AI...")
try:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'Hello, I am your AI fitness coach!' in a motivating way.")
    print(f"✅ Gemini Response: {response.text}")
except Exception as e:
    print(f"❌ Gemini Error: {e}")
    exit(1)

print("\n🔊 Testing ElevenLabs TTS...")
try:
    print("Speaking: 'AI Voice Coach Test'")
    elevenlabs_client = ElevenLabs(api_key=elevenlabs_key)
    audio = elevenlabs_client.text_to_speech.convert(
        text="AI Voice Coach Test",
        voice_id="SAz9YHcvj6GT2YYXdXww",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)
    print("✅ ElevenLabs TTS working")
except Exception as e:
    print(f"❌ ElevenLabs Error: {e}")

print("\n🎤 Testing Microphone...")
try:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone working")
except Exception as e:
    print(f"❌ Microphone Error: {e}")

print("\n✅ All tests passed! AI Voice Coach is ready to use.")
print("\nTo start the app with AI Voice Coach:")
print("  python app.py")
