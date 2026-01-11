import speech_recognition as sr
import threading
import time

class VoiceController:
    def __init__(self, callback):
        self.recognizer = sr.Recognizer()
        # Adjust recognition sensitivity
        self.recognizer.energy_threshold = 300  # Lower = more sensitive
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Seconds of silence to consider end of phrase
        
        self.microphone = sr.Microphone()
        self.callback = callback
        self.is_listening = False
        self.stop_listening = None
        self.last_recognition_time = 0

    def start_listening(self):
        if self.is_listening:
            return

        print("Voice Control: Starting listener...")
        print("Voice Control: Adjusting for ambient noise (please wait)...")
        
        try:
            self.is_listening = True
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("Voice Control: Ready! Say commands like 'start pushups'")
            print(f"Voice Control: Energy threshold: {self.recognizer.energy_threshold}")

            # Start background listening
            self.stop_listening = self.recognizer.listen_in_background(
                self.microphone, 
                self._process_audio,
                phrase_time_limit=5
            )
        except Exception as e:
            print(f"Voice Control Error: Failed to start - {e}")
            print("Voice Control: Continuing without voice control...")
            self.is_listening = False

    def stop(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        self.is_listening = False
        print("Voice Control: Stopped.")

    def _process_audio(self, recognizer, audio):
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio).lower()
            
            # Prevent duplicate commands within 2 seconds
            current_time = time.time()
            if current_time - self.last_recognition_time < 2:
                return
            
            print(f"Voice Control: Heard '{text}'")
            
            # Map simplified commands
            command = self._map_command(text)
            if command:
                print(f"Voice Control: Executing '{command}'")
                self.last_recognition_time = current_time
                self.callback(command)
            else:
                print(f"Voice Control: No matching command for '{text}'")
                
        except sr.UnknownValueError:
            # Could not understand audio - this is normal, don't spam console
            pass
        except sr.RequestError as e:
            print(f"Voice Control Error: Google API error - {e}")
            print("Voice Control: Check internet connection")
        except Exception as e:
            print(f"Voice Control Error: {e}")

    def _map_command(self, text):
        """Maps spoken text to internal command strings"""
        
        # Dictionary of trigger phrases: command_key
        triggers = {
            "start pushups": "pushups",
            "start push up": "pushups",
            "pushups": "pushups",
            "start squats": "squats",
            "start squat": "squats",
            "squats": "squats",
            "start jumping jacks": "jumping_jacks",
            "jumping jacks": "jumping_jacks",
            "start bicep curls": "bicep_curls",
            "bicep curls": "bicep_curls",
            "start lunges": "lunges",
            "lunges": "lunges",
            "start shoulder press": "shoulder_press",
            "shoulder press": "shoulder_press",
            "start plank": "plank",
            "plank": "plank",
            "start high knees": "high_knees",
            "high knees": "high_knees",
            "start crunches": "crunches",
            "crunches": "crunches",
            "go home": "home",
            "home": "home",
            "show history": "history",
            "history": "history",
            "show analytics": "analytics",
            "analytics": "analytics",
            "open tools": "tools",
            "tools": "tools",
            "stop": "stop",
            "quit": "quit"
        }
        
        for phrase, cmd in triggers.items():
            if phrase in text:
                return cmd
        return None
