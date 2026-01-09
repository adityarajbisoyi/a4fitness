import cv2
import numpy as np
import PoseModule as pm
import utils
import time
import database
import calories_module

def run_jumping_jack():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "Fix Form"
    last_feedback = ""
    start_time = time.time()
    
    # Flag for welcome message
    welcome_said = False
    last_count = 0

    while cap.isOpened():
        # Clean shutdown if 'q' pressed check at end of loop
        
        if not welcome_said:
            utils.speak("Welcome to jumping jack training")
            welcome_said = True

        if int(count) > last_count:
            utils.speak(str(int(count)))
            last_count = int(count)

        ret, img = cap.read()  # 640 x 480
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            r_hip_angle = detector.findAngle(img, 23, 24, 26)
            l_hip_angle = detector.findAngle(img, 24, 23, 25)
            hp_angel = detector.findAngle(img, 11, 23, 25)
            hp_angle2 = detector.findAngle(img, 12, 24, 26)
            
            # Using original logic for angles
            if r_hip_angle > 90 and l_hip_angle > 90 and hp_angle2 < 175 and hp_angel < 175:
                feedback = "Correct Position"
                form = 1
                
                if form == 1 and r_hip_angle > 110 and l_hip_angle > 110 and direction == 0 and hp_angle2 < 150 and hp_angel < 150:
                    feedback = "Squeeze"
                    count += 0.5
                    direction = 1

                if form == 1 and r_hip_angle < 100 and l_hip_angle < 100 and direction == 1 and hp_angle2 > 150 and hp_angel > 150:
                    feedback = "Stretch"
                    count += 0.5
                    direction = 0
            
            # Voice Feedback for form (optional, keeping minimal as per original but safer)
            # Original code printed "sq" "str" and feedback
            
            # Pushup counter (Jumping Jack counter really)
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)

        cv2.imshow('Jumping Jack counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Jumping Jacks", int(count), calories_module.calculate_calories("Jumping Jacks", int(count)))
