# AI Fitness Tracker

A computer vision-based fitness tracking application that monitors your form and counts repetitions for various exercises using OpenCV and MediaPipe.

## Features

- **Pushup Counter**: Tracks pushups with form correction feedback (Up/Down/Fix Form).
- **Squat Counter**: Monitors squat depth and counts repetitions.
- **Jumping Jacks**: Tracks jumping jack movements.
- **Real-time Feedback**: Visual feedback on the video feed including rep counts and form status.

## Prerequisites

- Python 3.10 (recommended for MediaPipe compatibility)
- Webcam

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

```bash
pip install opencv-python mediapipe==0.10.5 numpy
```
*Note: MediaPipe version `0.10.5` is recommended to ensure compatibility with the provided code.*

## Usage

### Main Application (Pushups)
To start the main pushup counter:

```bash
python main.py
```

### Other Exercises
You can run specific exercise trackers by executing their respective scripts:

- **Squats**: `python squart.py`
- **Jumping Jacks**: `python jumping_jack.py`
- **Cardio**: `python cardio.py`

## Controls
- Press `q` to quit the application window.

## Structure
- `PoseModule.py`: Core module containing the `poseDetector` class for landmark detection.
- `main.py`: Main entry point (Pushup counter).
- `improved.py`: An alternative or improved version of the tracker.
- `squart.py`: Squat tracking implementation.
- `jumping_jack.py`: Jumping jack tracking implementation.
