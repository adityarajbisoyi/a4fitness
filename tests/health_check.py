
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
                      "utility_modules", "ai_coach_module", "face_emotion_module", "voice_control_module"]
    for mod in custom_modules:
        check_module(mod)

    # 2. Logic Verification
    print("\n--- Logic Verification ---")
    
    # Database
    try:
        import database
        print("Database Connection...", end=" ")
        database.init_db()
        print("PASS ✅")
    except Exception as e:
        print(f"Database FAIL ❌: {e}")

    # AI Coach
    try:
        import ai_coach_module
        print("AI Coach Logic...", end=" ")
        coach = ai_coach_module.AICoach()
        # Mock simple landmarks (just 33 empty points)
        lm_list = [[i, 0, 0] for i in range(33)] 
        score, feedback = coach.evaluate_squat(lm_list)
        if score >= 0:
            print("PASS ✅")
        else:
             print("FAIL ❌ (Invalid Score)")
    except Exception as e:
        print(f"AI Coach FAIL ❌: {e}")

    # Utilities
    try:
        import utility_modules
        print("BMI Calculation...", end=" ")
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
