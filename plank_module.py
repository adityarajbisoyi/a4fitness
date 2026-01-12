import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import time
import calories_module

def run_plank():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    
    start_time = 0
    total_time = 0
    is_planking = False
    
    feedback = "Fix Form"
    last_feedback = ""

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # Check for straight line: Shoulder(11), Hip(23), Ankle(27)
            angle = detector.findAngle(img, 11, 23, 27)
            
            # Logic: Plank is roughly 170-180 degrees straight body
            if 170 < angle < 190:
                if not is_planking:
                    start_time = time.time()
                    is_planking = True
                    feedback = "Hold It"
                    utils.speak("Hold It")
                
                # Update time
                current_time = time.time()
                session_time = current_time - start_time
                
            else:
                if is_planking:
                    total_time += (time.time() - start_time)
                    is_planking = False
                    start_time = 0
                    feedback = "Fix Form"
                    utils.speak("Fix Form")
                
                session_time = 0

            # Draw Feedback and Timer
            display_time = total_time + session_time if is_planking else total_time
            
            # Draw Timer Box
            cv2.rectangle(img, (0, 0), (250, 80), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f"{int(display_time)}s", (20, 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)

            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow('Plank Timer', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    # Add final session time if quit while planking
    if is_planking:
        total_time += (time.time() - start_time)

    cap.release()
    cv2.destroyAllWindows()
    # Saving time in "reps" column for simplicity, or we could handle differently
    database.save_session("Plank (Secs)", int(total_time), calories_module.calculate_calories("Plank (Secs)", int(total_time)))
