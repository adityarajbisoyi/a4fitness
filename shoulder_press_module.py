import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module

def run_shoulder_press():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0  # 0 = down (start), 1 = up
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
            # Elbow Angle: Shoulder(12) - Elbow(14) - Wrist(16)
            angle = detector.findAngle(img, 12, 14, 16)
            
            # 50-90 degrees = Down position
            # 160-180 degrees = Up position (extended)
            
            per = np.interp(angle, (90, 160), (0, 100))
            bar = np.interp(angle, (90, 160), (380, 50))

            # Logic
            if angle > 160: # Fully extended up
                if direction == 0:
                    count += 0.5
                    direction = 1
                    feedback = "Down"
                else:
                    feedback = "Bring Down"

            if angle < 90: # Brought down
                if direction == 1:
                    count += 0.5
                    direction = 0
                    feedback = "Up"
                else:
                    feedback = "Push Up"

            # Voice Feedback
            if feedback != last_feedback:
                if feedback in ["Up", "Down"]:
                    utils.speak(feedback)
                elif feedback == "Fix Form" and last_feedback != "Fix Form":
                    utils.speak("Fix Form")
                last_feedback = feedback

            # Draw Bar
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            # Draw Counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

            # Draw Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow('Shoulder Press Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Shoulder Press", int(count), calories_module.calculate_calories("Shoulder Press", int(count)))
