import pyttsx3
import threading

import database

TRANSLATIONS = {
    "en": {
        "Up": "Up",
        "Down": "Down",
        "Fix Form": "Fix Form",
        "Hold It": "Hold It",
        "Welcome": "Welcome",
        "Curl Up": "Curl Up",
        "Lunge Down": "Lunge Down",
        "Push Up": "Push Up",
        "Bring Down": "Bring Down",
        "Crunch Up": "Crunch Up",
        "Ready": "Ready",
        "Left": "Left",
        "Right": "Right",
        "Start": "Start"
    },
    "hi": {
        "Up": "Upar",
        "Down": "Niche",
        "Fix Form": "Form Sahi Karein",
        "Hold It": "Rukein Rahein",
        "Welcome": "Swagat Hai",
        "Curl Up": "Upar Curl Karein",
        "Lunge Down": "Niche Lunge Karein",
        "Push Up": "Upar Push Karein",
        "Bring Down": "Niche Layein",
        "Crunch Up": "Upar Aayein",
        "Ready": "Taiyaar",
        "Left": "Baayein",
        "Right": "Daayein",
        "Start": "Shuru"
    }
}

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.lock = threading.Lock()

    def get_voice_id(self, lang):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            name = voice.name.lower()
            if lang == "hi":
                # specific checks for common Indian voices
                if "ravi" in name or "kalpana" in name or "hindi" in name or "india" in name:
                    return voice.id
            else:
                # Default to English (US/UK)
                if "david" in name or "zira" in name or "english" in name:
                    return voice.id
        return None

    def speak(self, key):
        lang = database.get_setting("language", "en")
        text = TRANSLATIONS.get(lang, {}).get(key, key)
        
        # Determine voice based on language
        voice_id = self.get_voice_id(lang)

        def _speak():
            with self.lock:
                try:
                    if voice_id:
                        self.engine.setProperty('voice', voice_id)
                    self.engine.say(text)
                    self.engine.runAndWait()
                except RuntimeError:
                    pass 

        # Run in separate thread to avoid blocking the video loop
        t = threading.Thread(target=_speak)
        t.start()

voice_assistant = VoiceAssistant()

def speak(text):
    voice_assistant.speak(text)
