
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_module(name):
    try:
        print(f"Checking {name}...", end=" ")
        __import__(name)
        print("PASS ✅")
        return True
    except Exception as e:
        print(f"FAIL ❌ ({e})")
        return False

def run_tests():
    print("=== AI FITNESS TRACKER HEALTH CHECK ===\n")
    
    # 1. Check Dependencies
    print("--- Dependency Check ---")
    dependencies = ["cv2", "mediapipe", "numpy", "customtkinter", "PIL", "matplotlib", "speech_recognition", "pyaudio"]
    for dep in dependencies:
        check_module(dep)
        
    print("\n--- Internal Module Check ---")
    custom_modules = ["database", "utils", "gamification_module", "tutorial_module", 
                      "utility_modules", "ai_coach_module", "face_emotion_module", 
                      "voice_control_module", "auto_detect_module", "weight_detect_module"]
    for mod in custom_modules:
        check_module(mod)

    # 2. Logic Verification
    print("\n--- Logic Verification ---")
    
    # Database (Quests)
    try:
        import database
        print("Database & Quests...", end=" ")
        database.init_db()
        quests = database.get_active_quests()
        if isinstance(quests, list):
            print("PASS ✅")
        else:
             print("FAIL ❌ (Quests return type mismatch)")
    except Exception as e:
        print(f"Database FAIL ❌: {e}")

    # AI Coach (Velocity)
    try:
        import ai_coach_module
        print("AI Coach velocity...", end=" ")
        coach = ai_coach_module.AICoach()
        if hasattr(coach, 'last_rep_duration'):
             print("PASS ✅")
        else:
             print("FAIL ❌ (Missing velocity attributes)")
    except Exception as e:
        print(f"AI Coach FAIL ❌: {e}")
        
    # Weight Detector
    try:
        import weight_detect_module
        print("Weight Detector...", end=" ")
        wd = weight_detect_module.WeightDetector()
        if "Red (5kg)" in wd.colors:
            print("PASS ✅")
        else:
            print("FAIL ❌ (Color map invalid)")
    except Exception as e:
        print(f"Weight Detect FAIL ❌: {e}")

    # Utilities
    try:
        import utility_modules
        print("BMI Calculation...", end=" ")
        # Warning: calculate_bmi might be static
        bmi = utility_modules.UtilityManager.calculate_bmi(70, 1.75)
        if 22.8 < bmi < 22.9:
            print("PASS ✅")
        else:
            print(f"FAIL ❌ (Expected ~22.85, got {bmi})")
    except Exception as e:
        print(f"Utilities FAIL ❌: {e}")
        
    print("\n=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    run_tests()
