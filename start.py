"""
A4 Fitness - Startup Script
This script checks dependencies and launches the main application.
"""

import sys
import subprocess

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'cv2': 'opencv-python',
        'customtkinter': 'customtkinter',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'pyttsx3': 'pyttsx3',
        'matplotlib': 'matplotlib',
        'PIL': 'Pillow',
        'bleak': 'bleak',
        'speech_recognition': 'SpeechRecognition'
    }
    
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    return missing

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            return True
        return False
    except Exception:
        return False

def main():
    print("=" * 60)
    print("🏋️  AI FITNESS TRACKER - Startup Check")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print("❌ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print()
        print("💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        return 1
    
    print("✅ All dependencies installed")
    print()
    
    # Check camera
    print("📷 Checking camera...")
    if check_camera():
        print("✅ Camera detected")
    else:
        print("⚠️  No camera detected - Some features may not work")
    
    print()
    print("=" * 60)
    print("🚀 Launching AI Fitness Tracker...")
    print("=" * 60)
    print()
    
    # Launch the main application
    try:
        import app
        app.ctk.set_appearance_mode("Dark")
        application = app.FitnessApp()
        application.protocol("WM_DELETE_WINDOW", application.on_closing)
        application.after(100, application.check_language)
        application.mainloop()
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
