# A4Fitness - AI-Powered Fitness Tracker

## 🎯 Features

### 🤖 AI Voice Coach (NEW!)
- **Intelligent Conversation**: Natural language interaction powered by Google Gemini AI
- **Smart Exercise Control**: AI decides when to start, stop, or change exercises
- **Real-time Coaching**: Motivational feedback and form correction during workouts
- **Context-Aware**: Understands your fatigue, progress, and goals
- **Voice Commands**: Just talk naturally - "Start pushups", "I'm tired", "Switch to squats"

### 🏋️ Exercise Tracking
- Full-screen pose detection with MediaPipe
- Multiple exercises: Pushups, Squats, Jumping Jacks, Bicep Curls, Lunges, Shoulder Press, Plank, High Knees, Crunches
- Auto-detect mode for flexible workouts
- Real-time rep counting and form analysis
- Calorie tracking

### 📊 Progress Analytics
- Session history with timestamps
- Progress graphs and analytics
- Achievement badges and gamification
- XP and level system
- Daily quest challenges

### 🎙️ Voice Features
- AI-powered voice coach with ElevenLabs TTS
- Natural conversation flow
- Motivational encouragement
- Form feedback

### 🩺 Health Profile
- Injury tracking and exercise restrictions
- Personalized recommendations
- Safety-conscious workout planning

### 🛠️ Utility Tools
- BMI Calculator
- PDF Report Export
- Water Reminder
- Rest Timer
- Bluetooth device connectivity

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam
- Microphone (for AI Voice Coach)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd a4fitness
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API Keys**

Create a `.env` file in the project root:
```env
GEMINI_LLM_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Get your API keys:
- **Gemini API**: https://makersuite.google.com/app/apikey
- **ElevenLabs API**: https://elevenlabs.io/

4. **Run setup for AI Voice Coach**
```bash
# Windows
setup_ai_coach.bat

# Mac/Linux
chmod +x setup_ai_coach.sh
./setup_ai_coach.sh
```

5. **Test the AI Voice Coach**
```bash
python test_ai_voice_coach.py
```

6. **Launch the app**
```bash
python app.py
```

## 🎮 How to Use

### With AI Voice Coach

1. **Start the app** - The AI Coach will greet you
2. **Talk naturally**: 
   - "Hey, let's do some pushups"
   - "I want to exercise"
   - "Start squats"
3. **During workout**:
   - AI provides real-time feedback
   - Counts your reps
   - Gives form corrections
   - Offers encouragement
4. **When tired**: 
   - "I'm tired"
   - "Take a break"
   - "Stop"
5. **Change exercises**:
   - "Switch to jumping jacks"
   - "Let's do something else"

### Without Voice

1. Click on exercise cards in the home screen
2. Follow on-screen tutorial
3. Perform exercise in front of camera
4. Press 'Q' to quit and save session

## 🧠 AI Voice Coach Features

### Natural Commands
- ✅ "Start pushups" → Begins exercise
- ✅ "How many reps have I done?" → AI tells you
- ✅ "I'm tired, stop" → Ends session
- ✅ "Switch to squats" → Changes exercise
- ✅ "Show my progress" → Navigates to analytics

### Intelligent Decisions
- Suggests breaks after intense sets
- Recommends exercise variety
- Adapts to your energy level
- Provides safety reminders

### Motivational Coaching
- "Great work! Keep it up!"
- "You're doing amazing!"
- "Watch your form! Focus on quality."
- "Perfect! Keep that energy!"

## 📋 Available Exercises

1. **Pushups** - Upper body strength
2. **Squats** - Lower body and core
3. **Jumping Jacks** - Cardio
4. **Bicep Curls** - Arm strength (requires weights)
5. **Lunges** - Leg strength and balance
6. **Shoulder Press** - Shoulder and arm strength
7. **Plank** - Core stability (time-based)
8. **High Knees** - Cardio and leg strength
9. **Crunches** - Abdominal strength
10. **Auto Detect** - AI detects your exercise

## 🔧 Configuration

### Voice Settings
Edit `ai_voice_coach.py`:
```python
self.recognizer.energy_threshold = 300  # Microphone sensitivity
self.recognizer.pause_threshold = 1.0   # Silence detection
```

### AI Model
Default: `gemini-1.5-flash` (fast and efficient)

For more detailed responses:
```python
self.model = genai.GenerativeModel('gemini-1.5-pro')
```

## 📖 Documentation

- [AI Voice Coach Guide](AI_VOICE_COACH_GUIDE.md) - Comprehensive documentation
- [Integration Guide](AI_VOICE_COACH_GUIDE.md#integration-guide) - Add AI to custom exercises
- [Troubleshooting](AI_VOICE_COACH_GUIDE.md#troubleshooting) - Common issues and fixes

## 🐛 Troubleshooting

### AI Coach Not Starting
1. Check API keys in `.env` file
2. Verify internet connection
3. Run `python test_ai_voice_coach.py`

### Voice Not Recognized
1. Check microphone permissions
2. Test microphone in other apps
3. Reduce background noise

### Camera Not Opening
1. Close other apps using camera
2. Check camera permissions
3. Try different camera index

## 🔐 Security & Privacy

- API keys stored in `.env` (not committed)
- Voice data processed by Google Speech Recognition
- Text processed by Gemini AI
- No voice/video data stored permanently
- All processing respects user privacy

## 🛠️ Tech Stack

- **UI**: CustomTkinter
- **Computer Vision**: OpenCV + MediaPipe
- **AI**: Google Gemini 1.5 Flash
- **Speech Recognition**: Google Speech Recognition
- **Text-to-Speech**: ElevenLabs
- **Data Visualization**: Matplotlib
- **Database**: SQLite (via database.py)

## 📊 System Requirements

- **OS**: Windows 10/11, macOS 10.14+, Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: 720p or higher
- **Microphone**: Any working microphone
- **Internet**: Required for AI features

## 🎨 Features in Development

- [ ] Emotion detection integration
- [ ] Personalized workout plans
- [ ] Multi-language support
- [ ] Social features
- [ ] Mobile app companion
- [ ] Advanced analytics with AI insights

## 📝 License

This project is part of the A4Fitness application.

## 🤝 Contributing

Contributions welcome! Please read the contribution guidelines first.

## 📧 Support

For issues or questions:
1. Check the [troubleshooting guide](AI_VOICE_COACH_GUIDE.md#troubleshooting)
2. Review error logs
3. Test with `test_ai_voice_coach.py`

## 🌟 Credits

- **AI**: Google Gemini
- **TTS**: ElevenLabs
- **Pose Detection**: MediaPipe
- **Development**: A4Fitness Team

---

**Note**: Previous rule-based voice commands have been replaced with intelligent AI Voice Coach for a more natural and adaptive experience.
