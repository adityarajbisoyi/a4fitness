# AI-Powered Voice Coach System

## Overview
This document describes the AI-powered voice chat system integrated into the A4Fitness application. The system replaces the rule-based voice commands with an intelligent AI coach powered by Google's Gemini AI.

## Features

### 🤖 Intelligent Conversation
- Natural language understanding using Gemini AI
- Context-aware responses based on current workout state
- Conversational personality that motivates and guides users

### 🎯 Smart Exercise Control
- AI decides when to start, stop, or change exercises
- Monitors user progress and suggests rest breaks
- Adapts to user's energy level and performance

### 🗣️ Voice Interaction
- Continuous listening with Google Speech Recognition
- Natural text-to-speech responses via ElevenLabs
- Non-blocking audio for seamless interaction

### 📊 Real-time Feedback
- Tracks rep counts and form quality
- Provides motivational messages during workouts
- Responds to form issues with coaching tips

## Architecture

### Core Components

1. **AIVoiceCoach** (`ai_voice_coach.py`)
   - Main class handling voice interaction
   - Integrates speech recognition, AI processing, and TTS
   - Manages conversation history and workout state

2. **App Integration** (`app.py`)
   - Replaces old `VoiceController` with `AIVoiceCoach`
   - Processes AI commands through `process_ai_command()`
   - Passes AI coach instance to exercise modules

3. **Exercise Modules** (e.g., `main_module.py`)
   - Updated to receive AI coach instance
   - Notify AI coach of rep counts and form feedback
   - Enable real-time coaching during exercises

### Data Flow

```
User Speech → Speech Recognition → Gemini AI → Decision Engine → App Actions
                                        ↓
                                   AI Response → ElevenLabs TTS → User Hears
```

## How It Works

### 1. Initialization
When the app starts:
- AI Voice Coach initializes with Gemini API
- Microphone adjusts for ambient noise
- System greets user and starts listening

### 2. Voice Processing
When user speaks:
1. Speech Recognition captures audio
2. Converts speech to text
3. Builds context with current workout state
4. Sends to Gemini AI for processing

### 3. AI Decision Making
Gemini AI:
- Understands user intent
- Considers current workout context
- Decides appropriate action
- Generates natural response

### 4. Action Execution
Based on AI decision:
- Start/stop/change exercises
- Navigate app screens
- Trigger rest breaks
- End workout sessions

### 5. Real-time Coaching
During exercise:
- AI receives rep count updates
- Monitors form feedback
- Provides encouragement
- Suggests breaks or exercise changes

## AI Capabilities

### Exercise Commands
- "Start pushups" → Starts pushup exercise
- "Let's do some squats" → Starts squat exercise
- "I'm tired, stop" → Stops current exercise
- "Switch to jumping jacks" → Changes exercise

### Navigation Commands
- "Show me my history" → Navigates to history
- "How are my analytics?" → Opens analytics
- "Go home" → Returns to home screen

### Intelligent Decisions
- After 15-20 reps: "Great work! Ready for a new exercise?"
- User says "I'm exhausted": "Let's take a 30-second break"
- Form issues detected: "Watch your form! Focus on quality"

## Configuration

### Environment Variables
Required in `.env` file:
```env
GEMINI_LLM_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### AI Model Settings
- **Model**: `gemini-1.5-flash` (fast, efficient)
- **Conversation History**: Last 20 exchanges
- **Response Format**: JSON with speech and action

### Voice Settings
- **Energy Threshold**: 300 (adjustable)
- **Pause Threshold**: 1.0 seconds
- **Phrase Time Limit**: 10 seconds

## Available Actions

### Exercise Actions
```json
{
  "action": "start_exercise",
  "parameters": {"exercise": "pushups"}
}
```

Supported exercises:
- pushups
- squats
- jumping_jacks
- bicep_curls
- lunges
- shoulder_press
- plank
- high_knees
- crunches
- auto_detect

### Control Actions
```json
{
  "action": "stop_exercise",
  "parameters": {}
}
```

```json
{
  "action": "change_exercise",
  "parameters": {"exercise": "squats"}
}
```

```json
{
  "action": "rest_break",
  "parameters": {"duration": 30}
}
```

### Navigation Actions
```json
{
  "action": "navigate",
  "parameters": {"destination": "history"}
}
```

Destinations: home, history, analytics, tools

## Integration Guide

### Adding AI Coach to New Exercises

1. **Update exercise function signature:**
```python
def run_your_exercise(ai_coach=None):
    # Your exercise code
```

2. **Create counter with AI coach:**
```python
counter = YourCounter(ai_coach=ai_coach)
```

3. **Notify AI of rep updates:**
```python
if self.ai_coach and int(self.count) != self.last_rep_update:
    self.last_rep_update = int(self.count)
    self.ai_coach.update_rep_count(int(self.count))
```

4. **Send form feedback:**
```python
if self.ai_coach and self.feedback:
    self.ai_coach.notify_exercise_feedback(self.feedback)
```

5. **Update app.py exercise starter:**
```python
def start_your_exercise(self):
    tutorial_module.show_tutorial(self, "Your Exercise")
    import your_module
    self.run_exercise_thread(lambda: your_module.run_your_exercise(ai_coach=self.ai_coach))
```

## Testing

### Quick Test
Run the test script to verify setup:
```bash
python test_ai_voice_coach.py
```

This checks:
- ✅ API keys present
- ✅ Required packages installed
- ✅ Gemini AI responding
- ✅ ElevenLabs TTS working
- ✅ Microphone accessible

### Manual Testing
1. Start the app: `python app.py`
2. Wait for "AI Coach: Active" status
3. Say: "Hey, start pushups"
4. Verify exercise starts
5. Say: "Stop" or "I'm tired"
6. Verify AI responds and stops

## Troubleshooting

### Common Issues

**Problem**: "AI Coach: Unavailable"
- Check API keys in `.env` file
- Verify `google-generativeai` installed
- Check internet connection

**Problem**: No voice recognition
- Check microphone permissions
- Test microphone in other apps
- Adjust energy_threshold if needed

**Problem**: AI not responding
- Check Gemini API quota/limits
- Verify API key is valid
- Check console for error messages

**Problem**: TTS not working
- Verify ElevenLabs API key
- Check audio output device
- Test with `test_ai_voice_coach.py`

### Debug Mode
Enable verbose logging by adding to `ai_voice_coach.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### Response Time
- Gemini 1.5 Flash: ~1-2 seconds
- Speech Recognition: ~0.5 seconds
- TTS Generation: ~1 second
- Total latency: ~2-3 seconds

### Resource Usage
- RAM: ~200MB for AI models
- CPU: Moderate during voice processing
- Network: ~1KB per AI request

### Best Practices
- Keep conversation history limited (20 exchanges)
- Use non-blocking speech queue
- Process audio in background thread
- Cache common responses (future enhancement)

## Future Enhancements

### Planned Features
- [ ] Emotion detection integration
- [ ] Personalized coaching based on user history
- [ ] Multi-language support
- [ ] Offline mode with cached responses
- [ ] Voice biometrics for user identification
- [ ] Workout plan generation
- [ ] Social features (voice-controlled sharing)

### Advanced AI Features
- [ ] Predictive fatigue detection
- [ ] Adaptive workout difficulty
- [ ] Injury prevention suggestions
- [ ] Nutrition advice integration
- [ ] Sleep pattern correlation

## Security Considerations

### API Key Protection
- Store keys in `.env` file (not in code)
- Add `.env` to `.gitignore`
- Never commit API keys to repository
- Rotate keys periodically

### Data Privacy
- Voice data sent to Google (Speech Recognition)
- Text sent to Gemini API for processing
- Consider privacy policy for users
- Option to disable AI coach if desired

### Rate Limiting
- Gemini API: 60 requests/minute (free tier)
- ElevenLabs: Varies by plan
- Implement rate limiting if needed

## License
This AI Voice Coach system is part of the A4Fitness application.

## Support
For issues or questions:
1. Check troubleshooting section
2. Review error logs
3. Test with `test_ai_voice_coach.py`
4. Contact development team

## Credits
- **AI Model**: Google Gemini 1.5 Flash
- **Text-to-Speech**: ElevenLabs
- **Speech Recognition**: Google Speech Recognition
- **Integration**: A4Fitness Team
