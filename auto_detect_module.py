
import cv2
import numpy as np
import PoseModule as pm
import utils
import time
import math
import ai_coach_module

class AutoDetector:
    def __init__(self):
        self.detector = pm.poseDetector()
        self.state = "Scanning"  # Scanning, Squats, Pushups, JumpingJacks
        self.state_counter = 0
        self.confirmation_threshold = 20 # Frames to confirm a state change

    def get_bbox(self, lm_list, img_shape):
        """Returns bounding box of the body"""
        if not lm_list:
            return None
        h, w, c = img_shape
        x_min, y_min = w, h
        x_max, y_max = 0, 0
        
        for lm in lm_list:
            x, y = lm[1], lm[2]
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            
        return x_min, y_min, x_max, y_max

    def detect_state(self, lm_list, img_shape):
        if not lm_list:
            return "Scanning"

        bbox = self.get_bbox(lm_list, img_shape)
        if not bbox:
            return "Scanning"
            
        x_min, y_min, x_max, y_max = bbox
        bbox_h = y_max - y_min
        bbox_w = x_max - x_min
        
        aspect_ratio = bbox_h / bbox_w if bbox_w > 0 else 0

        # Heuristics
        # 1. Horizontal (Pushup/Plank) vs Vertical (Squat/Jumping)
        if aspect_ratio < 0.8: # Horizontal
            return "Pushups"
        else: # Vertical
            # Check Hands for Jumping Jacks (Hands above shoulders)
            # 11=L.Shoulder, 12=R.Shoulder, 15=L.Wrist, 16=R.Wrist
            l_shoulder_y = lm_list[11][2]
            r_shoulder_y = lm_list[12][2]
            l_wrist_y = lm_list[15][2]
            r_wrist_y = lm_list[16][2]
            
            # If wrists are significantly above shoulders
            if l_wrist_y < l_shoulder_y and r_wrist_y < r_shoulder_y:
                return "Jumping Jacks"
                
            # Default Vertical
            return "Squats"

def run_auto_mode():
    # Try to open camera with error handling
    cap = None
    for camera_index in [0, 1, 2]:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            print(f"✅ Camera opened successfully on index {camera_index}")
            break
        cap.release()
    
    if not cap or not cap.isOpened():
        print("❌ ERROR: Could not access camera!")
        print("Please check:")
        print("  1. Camera is connected")
        print("  2. No other application is using the camera")
        print("  3. Camera permissions are granted")
        return
    
    auto_detector = AutoDetector()
    detector = pm.poseDetector()
    coach = ai_coach_module.AICoach()
    
    # Import exercise counter classes
    from squart import SquatCounter
    from jumping_jack_module import JumpingJackCounter
    from main_module import PushupCounter
    
    # Initialize counters
    squat_counter = SquatCounter()
    jump_counter = JumpingJackCounter()
    pushup_counter = PushupCounter()
    
    # Track totals for display
    counters = {
        "Squats": 0,
        "Pushups": 0,
        "Jumping Jacks": 0
    }
    
    current_exercise = "Scanning"
    display_exercise = "Scanning..."
    
    # Smooth state switching
    pending_state = "Scanning"
    pending_counter = 0

    utils.speak("Auto detect mode. Perform any exercise and switch between them freely.")

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Continuously detect exercise type
            detected = auto_detector.detect_state(lmList, (h, w, c))
            
            # State Machine Confirmation for switching
            if detected == pending_state:
                pending_counter += 1
            else:
                pending_state = detected
                pending_counter = 0
                
            if pending_counter > 15: # approx 0.5 sec stability to switch
                if current_exercise != pending_state:
                    current_exercise = pending_state
                    display_exercise = f"Auto: {current_exercise}"
                    if current_exercise != "Scanning":
                        utils.speak(f"Switched to {current_exercise}")

            # --- DELEGATE TO EXERCISE MODULES ---
            
            # SQUATS - Use SquatCounter class
            if current_exercise == "Squats":
                count_inc, feedback = squat_counter.process_frame(lmList, detector)
                counters["Squats"] = int(squat_counter.count)
                
                # AI Coach Analysis
                score, ai_feedback = coach.evaluate_squat(lmList)
                cv2.putText(img, f"Score: {int(score)}%", (w-200, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(img, feedback, (w-250, 140), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

            # JUMPING JACKS - Use JumpingJackCounter class
            elif current_exercise == "Jumping Jacks":
                count_inc, feedback = jump_counter.process_frame(lmList)
                counters["Jumping Jacks"] = int(jump_counter.count)
                            
            # PUSHUPS - Use PushupCounter class
            elif current_exercise == "Pushups":
                count_inc, feedback = pushup_counter.process_frame(lmList, detector)
                counters["Pushups"] = int(pushup_counter.count)
                
                # AI Coach Analysis
                score, ai_feedback = coach.evaluate_pushup(lmList)
                cv2.putText(img, f"Score: {int(score)}%", (w-200, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # DRAW UI
        # Top Banner
        cv2.rectangle(img, (0, 0), (w, 80), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, display_exercise, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Stats Panel - All exercise counts
        y_offset = 120
        for ex, count in counters.items():
            color = (0, 255, 0) if ex == current_exercise else (150, 150, 150)
            cv2.putText(img, f"{ex}: {count}", (20, y_offset), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            y_offset += 40
            
        # Show pending detection
        if pending_state != current_exercise and pending_state != "Scanning":
            cv2.putText(img, f"Detecting: {pending_state}...", (20, h-40), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 200, 0), 2)

        cv2.imshow('Auto-Detection Mode', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Save session with total counts
    import database
    import calories_module
    total_reps = sum(count for count in counters.values())
    if total_reps > 0:
        total_calories = sum(calories_module.calculate_calories(ex, count) for ex, count in counters.items() if count > 0)
        database.save_session("Auto-Detect Mixed", total_reps, total_calories)
