# 🏋️ AI Fitness Tracker

**The Ultimate Smart Workout Companion powered by Computer Vision & Artificial Intelligence.**

![Fitness AI](assets/logo.png)

This application uses your webcam to analyze your exercise form in real-time, count reps, and provide AI coaching feedback. It features a modern GUI, gamification (XP, Levels), and hands-free voice control.

---

## 🌟 Key Features

### 🧠 Advanced AI & Computer Vision
*   **🤖 Auto-Exercise Recognition (Auto Mode)**: Automatically detects if you are doing Squats, Pushups, or Jumping Jacks without pressing any buttons.
*   **⚡ Velocity Training**: Tracks your rep speed (e.g., "0.8s ⚡ Power Rep!") to optimize hypertrophy vs strength.
*   **⚖️ Auto Weight Detection**: Uses computer vision to detect dumbbell weight by color (Red=5kg, Blue=10kg).
*   **AI Coach**: Real-time form analysis giving feedback like "Go Lower", "Straighten Back".
*   **Face Emotion Detection** 😃/😫: Detects if you are happy or straining during a workout.
*   **Voice Command Control** 🎙️: Completely hands-free navigation.

### 🎮 Gamification
*   **📜 Daily Quests**: 3 random challenges every day (e.g., "Do 20 Pushups") to earn Bonus XP.
*   **Level System**: Earn XP for every rep. Level up from Bronze to Diamond.
*   **Achievements**: Unlock badges like "Early Bird", "Squat King", "Iron Man".
*   **Streaks**: Maintain a daily workout streak.

### 📊 Exercises & Tools
*   💪 **Pushups** (Chest/Triceps)
*   🦵 **Squats** (Legs/Glutes)
*   🏃 **Jumping Jacks** (Cardio)
*   💪 **Bicep Curls** (Arms)
*   🏋️ **Shoulder Press** (Delts)
*   🚶 **Lunges** (Legs)
*   🧘 **Plank** (Core Stability)
*   🦵 **High Knees** (Cardio)
*   🍫 **Crunches** (Abs)

### 🩺 Health & Utilities
*   **Injury Modifiers (Health Profile)**: Select your injuries (e.g., Knee, Shoulder) and the AI automatically disables risky exercises.
*   **Analytics Dashboard**: Visual graphs of your reps and calories.
*   **BMI Calculator**: Track your body metrics.
*   **PDF Export**: Download session reports.

---

## 💻 Installation

### Prerequisites
*   Python 3.10 or higher
*   Webcam

### Steps
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/adityarajbisoyi/a4fitness.git
    cd a4fitness
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 How to Run

### Main Application (Recommended)
Run the full GUI application with all features:

```bash
python app.py
```

Or use the startup script with dependency checks:

```bash
python start.py
```

### Demo Scripts
- **Simple Pushup Counter**: `python main.py` (Basic demo, no GUI)
- **Auto Mode**: Click "🤖 Auto Detect" in the app to let the AI guess your workout
- **Weight Scanner**: Run `python weight_detect_module.py` to calibrate weights

---

## 🔧 Troubleshooting

### Camera Issues
- **Error: "Could not access camera"**
  - Make sure your webcam is connected
  - Close other applications using the camera (Zoom, Teams, etc.)
  - Try running with administrator privileges
  - Check camera permissions in Windows Settings

### Missing Dependencies
- Run `pip install -r requirements.txt` to install all packages
- If Bluetooth features don't work, install: `pip install bleak`

### Application Won't Start
- Make sure you're running `python app.py` NOT `python main.py`
- Check that Python 3.10+ is installed: `python --version`
- Verify all dependencies are installed

---

## 🎙️ Voice Commands

You can control the app hands-free! Try saying:

| Command | Action |
| :--- | :--- |
| **"Start Pushups"** | Launches Pushup Module |
| **"Start Squats"** | Launches Squat Module |
| **"Start Auto Mode"** | Launches Auto Recognition |
| **"Go Home"** | Returns to Main Menu |
| **"Show History"** | Opens History Tab |
| **"Stop"** | Stops current activity |

---

## 📂 Project Structure

*   `app.py`: Main GUI application (CustomTkinter).
*   `auto_detect_module.py`: Logic for Automatic Exercise Recognition.
*   `weight_detect_module.py`: HSV Color masking for dumbells.
*   `gamification_module.py`: Quests, XP, and Badges logic.
*   `PoseModule.py`: Core logic for MediaPipe Pose estimation.
*   `ai_coach_module.py`: Logic for scoring form, velocity, and mechanics.
*   `face_emotion_module.py`: Face Mesh logic for emotion detection.
*   `voice_control_module.py`: Background thread for speech recognition.
*   `database.py`: SQLite database management.

---

## 👨‍💻 Developer
**Aditya Raj Bisoyi**

---
*Built with Python, OpenCV, MediaPipe, and CustomTkinter.*
