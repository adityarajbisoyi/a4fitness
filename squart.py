import cv2
import numpy as np
import time
import PoseModule as pm
import database
import calories_module

def run_squat():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not access camera!")
        return
    
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    threshold=100
    feedback = "Fix Form"
    arr = []
    shoulder_level = 0
    
    while cap.isOpened():
        ret, img = cap.read()  # 640 x 480
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        # Determine dimensions of video - Help with creation of box in Line 43
        width = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        # print(width, height)

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:

            hip = detector.findAngle(img, 11, 23, 25)
            knee = detector.findAngle(img, 23, 25, 27)
            # Percentage of success of pushup
            per = np.interp(knee, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(knee, (90, 160), (380, 50))

            # Check to ensure right form before starting the program
            if knee>160 and hip>160:
                shoulder_level = lmList[11][2]
                form = 1
                if not len(arr):
                    arr.append(shoulder_level)
                else:
                    current_level = lmList[11][2]
                    difference = abs(arr[0]-current_level)
            # Check for full range of motion for the pushup
            if form == 1:

                if per > 85:

                    if knee > 140 and hip > 140:
                        feedback = "Down"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"
                        # form = 0


                if per < 15:
                    if not len(arr):
                        arr.append(shoulder_level)
                    else:
                        current_level = lmList[11][2]
                        difference = abs(arr[0] - current_level)

                    if knee < 90 and hip < 120 and (difference>threshold):
                        feedback = "Up"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"
                        # form = 0

           


            # Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

            # Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        else:
            if len(arr):
                arr.pop()
        cv2.imshow('Squat counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Squats", int(count), calories_module.calculate_calories("Squats", int(count)))
