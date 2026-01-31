"""
AI-Powered Voice Coach Module
Uses Gemini AI for intelligent conversation and exercise coaching
Integrates with ElevenLabs for text-to-speech
"""

import os
import json
import threading
import time
import queue
from datetime import datetime
import speech_recognition as sr
from dotenv import load_dotenv
import google.generativeai as genai
from tts_elevenlabs import speak

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_LLM_API_KEY"))

class AIVoiceCoach:
    """
    AI Voice Coach that listens, understands context, and provides guidance
    """
    
    def __init__(self, app_callback):
        """
        Initialize the AI Voice Coach
        
        Args:
            app_callback: Function to call with commands like {'action': 'start_exercise', 'exercise': 'pushups'}
        """
        self.app_callback = app_callback
        
        # Speech Recognition Setup
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
        self.microphone = sr.Microphone()
        
        # Gemini AI Setup
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.conversation_history = []
        
        # State Management
        self.is_listening = False
        self.stop_listening_func = None
        self.current_exercise = None
        self.exercise_start_time = None
        self.rep_count = 0
        self.session_data = {}
        self.stop_exercise_flag = False
        
        # Audio queue for non-blocking speech
        self.speech_queue = queue.Queue()
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        # Available exercises
        self.exercises = [
            "pushups", "squats", "jumping_jacks", "bicep_curls", 
            "lunges", "shoulder_press", "plank", "high_knees", 
            "crunches", "auto_detect"
        ]
        
        # System prompt for Gemini
        self.system_context = self._build_system_prompt()
        
        print("🤖 AI Voice Coach initialized!")
    
    def _build_system_prompt(self):
        """Build the system prompt that defines the AI coach's personality and capabilities"""
        return """You are an enthusiastic AI Fitness Coach named "Coach AI" integrated into a fitness tracking app.

YOUR CAPABILITIES:
- Start/stop exercises: pushups, squats, jumping_jacks, bicep_curls, lunges, shoulder_press, plank, high_knees, crunches, auto_detect
- Track reps and provide real-time feedback during workouts
- Motivate users with encouraging messages
- Decide when a user should rest, switch exercises, or stop
- Answer fitness questions
- Navigate the app (home, history, analytics, tools)

YOUR PERSONALITY:
- Enthusiastic and motivating
- Professional but friendly
- Safety-conscious
- Adaptive to user's energy level and emotions

RESPONSE FORMAT:
When you need to perform an action, respond with JSON in this format:
{
    "speech": "What you say to the user",
    "action": "command_name",
    "parameters": {"key": "value"}
}

AVAILABLE ACTIONS:
- start_exercise: {"exercise": "exercise_name"}
- stop_exercise: {}
- change_exercise: {"exercise": "new_exercise_name"}
- navigate: {"destination": "home|history|analytics|tools"}
- rest_break: {"duration": 30}
- end_session: {}

DECISION MAKING:
- If user sounds tired or requests a break, suggest rest or stop
- After 15-20 reps of an exercise, suggest switching or resting
- If user expresses discomfort or pain, immediately suggest stopping
- Be proactive in guiding the workout flow

Keep responses conversational and under 50 words unless explaining something complex."""

    def start_listening(self):
        """Start listening for voice commands"""
        if self.is_listening:
            return
        
        print("🎙️ AI Coach: Adjusting for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.is_listening = True
            self.stop_listening_func = self.recognizer.listen_in_background(
                self.microphone,
                self._process_audio,
                phrase_time_limit=10
            )
            
            # Greet the user
            greeting = "Hey! I'm your AI fitness coach. I'm here to guide your workout. What would you like to do today?"
            self._speak_async(greeting)
            print(f"🤖 AI Coach: {greeting}")
            
        except Exception as e:
            print(f"❌ Failed to start AI Coach: {e}")
            self.is_listening = False
    
    def stop(self):
        """Stop listening"""
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
        self.is_listening = False
        print("🤖 AI Coach: Stopped listening")
    
    def _process_audio(self, recognizer, audio):
        """Process audio from microphone"""
        try:
            # Recognize speech
            text = recognizer.recognize_google(audio).lower()
            print(f"🎙️ User said: '{text}'")
            
            # Get AI response
            threading.Thread(target=self._handle_user_input, args=(text,), daemon=True).start()
            
        except sr.UnknownValueError:
            # Could not understand - this is normal
            pass
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
        except Exception as e:
            print(f"❌ Error processing audio: {e}")
    
    def _handle_user_input(self, user_text):
        """Handle user input with AI"""
        try:
            # Build context for AI
            context = self._build_context_message(user_text)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "parts": [context]
            })
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Get AI response
            chat = self.model.start_chat(history=self.conversation_history)
            response = chat.send_message(context)
            ai_response = response.text
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "model",
                "parts": [ai_response]
            })
            
            # Process the response
            self._process_ai_response(ai_response)
            
        except Exception as e:
            print(f"❌ Error handling user input: {e}")
            self._speak_async("Sorry, I had trouble processing that. Can you repeat?")
    
    def _build_context_message(self, user_text):
        """Build context message for AI with current state"""
        context = f"{self.system_context}\n\nCURRENT STATE:\n"
        
        if self.current_exercise:
            elapsed = int(time.time() - self.exercise_start_time)
            context += f"- Currently doing: {self.current_exercise}\n"
            context += f"- Reps completed: {self.rep_count}\n"
            context += f"- Time elapsed: {elapsed} seconds\n"
        else:
            context += "- No active exercise\n"
        
        context += f"\nUSER SAID: {user_text}\n\n"
        context += "Respond naturally and take appropriate action if needed."
        
        return context
    
    def _process_ai_response(self, ai_response):
        """Process AI response and execute actions"""
        try:
            # Try to parse as JSON first
            if "{" in ai_response and "}" in ai_response:
                # Extract JSON from response
                json_start = ai_response.index("{")
                json_end = ai_response.rindex("}") + 1
                json_str = ai_response[json_start:json_end]
                response_data = json.loads(json_str)
                
                speech = response_data.get("speech", "")
                action = response_data.get("action")
                parameters = response_data.get("parameters", {})
                
                # Speak the response
                if speech:
                    print(f"🤖 AI Coach: {speech}")
                    self._speak_async(speech)
                
                # Execute action
                if action:
                    self._execute_action(action, parameters)
            else:
                # Plain text response
                print(f"🤖 AI Coach: {ai_response}")
                self._speak_async(ai_response)
                
        except Exception as e:
            # If parsing fails, just speak the response
            print(f"🤖 AI Coach: {ai_response}")
            self._speak_async(ai_response)
    
    def _execute_action(self, action, parameters):
        """Execute actions determined by AI"""
        try:
            if action == "start_exercise":
                exercise = parameters.get("exercise")
                if exercise in self.exercises:
                    self.stop_exercise_flag = False
                    self.current_exercise = exercise
                    self.exercise_start_time = time.time()
                    self.rep_count = 0
                    print(f"▶️ AI Coach: Starting {exercise}")
                    self.app_callback({
                        "action": "start_exercise",
                        "exercise": exercise
                    })
            
            elif action == "stop_exercise":
                self.stop_exercise_flag = True
                self.current_exercise = None
                self.exercise_start_time = None
                self.rep_count = 0
                print("🛑 AI Coach: Stopping exercise...")
                self.app_callback({
                    "action": "stop_exercise"
                })
            
            elif action == "change_exercise":
                new_exercise = parameters.get("exercise")
                if new_exercise in self.exercises:
                    self.stop_exercise_flag = True  # Stop current
                    time.sleep(0.5)  # Brief pause
                    self.stop_exercise_flag = False  # Ready for new
                    self.current_exercise = new_exercise
                    self.exercise_start_time = time.time()
                    self.rep_count = 0
                    print(f"🔄 AI Coach: Changing to {new_exercise}")
                    self.app_callback({
                        "action": "change_exercise",
                        "exercise": new_exercise
                    })
            
            elif action == "navigate":
                destination = parameters.get("destination")
                self.app_callback({
                    "action": "navigate",
                    "destination": destination
                })
            
            elif action == "rest_break":
                duration = parameters.get("duration", 30)
                self.app_callback({
                    "action": "rest_break",
                    "duration": duration
                })
            
            elif action == "end_session":
                self.current_exercise = None
                self.app_callback({
                    "action": "end_session"
                })
                
        except Exception as e:
            print(f"❌ Error executing action: {e}")
    
    def update_rep_count(self, count):
        """Update rep count from exercise module"""
        old_count = self.rep_count
        self.rep_count = count
        print(f"🔢 AI Coach: Rep count updated to {count}")
        
        # AI can provide encouragement based on progress
        if count > 0 and count % 5 == 0 and count != old_count:
            encouragement = [
                "Great work! Keep it up!",
                "You're doing amazing!",
                "Strong form! Keep going!",
                "Excellent! You've got this!",
                "Perfect! Keep that energy!"
            ]
            import random
            msg = random.choice(encouragement)
            self._speak_async(msg)
    
    def notify_exercise_feedback(self, feedback):
        """Receive feedback from exercise modules (e.g., 'Fix Form', 'Good', etc.)"""
        # AI can respond to form issues
        if "fix" in feedback.lower() or "bad" in feedback.lower():
            if hasattr(self, '_last_form_warning'):
                if time.time() - self._last_form_warning < 10:
                    return  # Don't spam warnings
            
            self._last_form_warning = time.time()
            self._speak_async("Watch your form! Focus on quality over speed.")
    
    def _speak_async(self, text):
        """Queue text for speech (non-blocking)"""
        self.speech_queue.put(text)
    
    def _speech_worker(self):
        """Worker thread that processes speech queue"""
        while True:
            try:
                text = self.speech_queue.get()
                if text:
                    speak(text)
                self.speech_queue.task_done()
            except Exception as e:
                print(f"❌ Speech error: {e}")
                time.sleep(0.5)
