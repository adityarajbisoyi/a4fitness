import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module

def run_bicep_curl():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0  # 0 = down, 1 = up
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
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            
            # Map angle to percentage (approximate range for curl)
            per = np.interp(angle, (30, 160), (100, 0))
            bar = np.interp(angle, (30, 160), (50, 380))

            # Logic
            if angle > 160:
                if direction == 1:
                    count += 0.5
                    direction = 0
                    feedback = "Down"
                else:
                    feedback = "Curl Up" # Ready to curl

            if angle < 30:
                if direction == 0:
                    count += 0.5
                    direction = 1
                    feedback = "Up"
                else:
                    feedback = "Down" # Ready to go down

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

        cv2.imshow('Bicep Curl Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Bicep Curls", int(count), calories_module.calculate_calories("Bicep Curls", int(count)))
