import speech_recognition as sr
import threading
import time

class VoiceController:
    def __init__(self, callback):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = callback
        self.is_listening = False
        self.stop_listening = None

    def start_listening(self):
        if self.is_listening:
            return

        print("Voice Control: Starting listener...")
        self.is_listening = True
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        # Start background listening
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self._process_audio)

    def stop(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.is_listening = False
        print("Voice Control: Stopped.")

    def _process_audio(self, recognizer, audio):
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio).lower()
            print(f"Voice Control: Heard '{text}'")
            
            # Map simplified commands
            command = self._map_command(text)
            if command:
                print(f"Voice Control: Executing '{command}'")
                self.callback(command)
                
        except sr.UnknownValueError:
            pass # Could not understand audio
        except sr.RequestError as e:
            print(f"Voice Control Error: {e}")

    def _map_command(self, text):
        """Maps spoken text to internal command strings"""
        
        # Dictionary of trigger phrases: command_key
        triggers = {
            "start pushups": "pushups",
            "start push up": "pushups",
            "start squats": "squats",
            "start squat": "squats",
            "start jumping jacks": "jumping_jacks",
            "start bicep curls": "bicep_curls",
            "start lunges": "lunges",
            "start shoulder press": "shoulder_press",
            "start plank": "plank",
            "start high knees": "high_knees",
            "start crunches": "crunches",
            "go home": "home",
            "show history": "history",
            "show analytics": "analytics",
            "open tools": "tools",
            "stop": "stop",
            "quit": "quit"
        }
        
        for phrase, cmd in triggers.items():
            if phrase in text:
                return cmd
        return None
