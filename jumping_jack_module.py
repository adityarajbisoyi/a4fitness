import cv2
import numpy as np
import PoseModule as pm
import utils
import time
import database
import calories_module

def run_jumping_jack():
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
    
    detector = pm.poseDetector()
    count = 0
    direction = 0  # 0 = arms down, 1 = arms up
    feedback = "Stand Ready"
    last_feedback = ""
    start_time = time.time()
    
    # Flag for welcome message
    welcome_said = False
    last_count = 0

    while cap.isOpened():
        if not welcome_said:
            utils.speak("Welcome to jumping jack training")
            welcome_said = True

        if int(count) > last_count:
            utils.speak(str(int(count)))
            last_count = int(count)

        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # Get key landmarks
            # 11 = Left Shoulder, 12 = Right Shoulder
            # 15 = Left Wrist, 16 = Right Wrist
            # 23 = Left Hip, 24 = Right Hip
            # 27 = Left Ankle, 28 = Right Ankle
            
            left_shoulder_y = lmList[11][2]
            right_shoulder_y = lmList[12][2]
            left_wrist_y = lmList[15][2]
            right_wrist_y = lmList[16][2]
            
            left_hip_x = lmList[23][1]
            right_hip_x = lmList[24][1]
            left_ankle_x = lmList[27][1]
            right_ankle_x = lmList[28][1]
            
            # Calculate average shoulder and wrist heights
            avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
            avg_wrist_y = (left_wrist_y + right_wrist_y) / 2
            
            # Calculate leg spread (distance between ankles)
            leg_spread = abs(left_ankle_x - right_ankle_x)
            hip_width = abs(left_hip_x - right_hip_x)
            
            # Hands are UP when wrists are above shoulders
            hands_up = (left_wrist_y < left_shoulder_y - 30) and (right_wrist_y < right_shoulder_y - 30)
            
            # Legs are SPREAD when ankles are wider apart than hips
            legs_spread = leg_spread > (hip_width * 1.5)
            
            # Jumping Jack Logic
            # Position 1: Arms up, legs spread
            if hands_up and legs_spread:
                feedback = "Arms Up! ⬆️"
                if direction == 0:
                    count += 0.5
                    direction = 1
                    
            # Position 2: Arms down, legs together
            elif not hands_up and not legs_spread:
                feedback = "Arms Down ⬇️"
                if direction == 1:
                    count += 0.5
                    direction = 0
            else:
                # Partial movement
                if hands_up:
                    feedback = "Spread Legs"
                elif legs_spread:
                    feedback = "Raise Arms"
                else:
                    feedback = "Start Movement"
            
            # Draw visual indicators
            # Show hand position indicator
            hand_color = (0, 255, 0) if hands_up else (0, 0, 255)
            cv2.circle(img, (lmList[15][1], lmList[15][2]), 15, hand_color, cv2.FILLED)  # Left wrist
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 15, hand_color, cv2.FILLED)  # Right wrist
            
            # Show leg position indicator
            leg_color = (0, 255, 0) if legs_spread else (0, 0, 255)
            cv2.circle(img, (lmList[27][1], lmList[27][2]), 15, leg_color, cv2.FILLED)  # Left ankle
            cv2.circle(img, (lmList[28][1], lmList[28][2]), 15, leg_color, cv2.FILLED)  # Right ankle
            
            # Counter display
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Feedback display
            cv2.rectangle(img, (450, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (460, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                        (0, 255, 0), 2)
            
            # Status indicators
            cv2.putText(img, f"Hands: {'UP' if hands_up else 'DOWN'}", (10, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 1.5, hand_color, 2)
            cv2.putText(img, f"Legs: {'SPREAD' if legs_spread else 'TOGETHER'}", (10, 60), 
                       cv2.FONT_HERSHEY_PLAIN, 1.5, leg_color, 2)

        cv2.imshow('Jumping Jack Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Jumping Jacks", int(count), calories_module.calculate_calories("Jumping Jacks", int(count)))
