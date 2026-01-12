import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module

def run_high_knees():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    feedback = "Start"
    
    # State tracking
    # 0 = Both feet down
    # 1 = Left Knee Up
    # 2 = Right Knee Up
    state = 0 
    last_state = 0

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # Check knee height vs hip height
            # Left: Hip(23), Knee(25)
            # Right: Hip(24), Knee(26)
            
            l_hip_y = lmList[23][2]
            l_knee_y = lmList[25][2]
            
            r_hip_y = lmList[24][2]
            r_knee_y = lmList[26][2]
            
            # Threshold: Knee should be above hip (y value smaller)
            # Add some buffer
            
            is_left_up = l_knee_y < l_hip_y
            is_right_up = r_knee_y < r_hip_y
            
            if is_left_up and state != 1:
                state = 1
                count += 0.5
                feedback = "Left"
            
            elif is_right_up and state != 2:
                state = 2
                count += 0.5
                feedback = "Right"
            
            elif not is_left_up and not is_right_up:
                state = 0

            # Draw Counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

            # Draw Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow('High Knees Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("High Knees", int(count), calories_module.calculate_calories("High Knees", int(count)))
