import threading
import time
import cv2
import numpy as np
import PoseModule as pm
import pyttsx3

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
threshold = 100
feedback = "Fix Form"
rf = []
# lf = 0
start_time = time.time()
timeout = 10


def speak(text):
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=_speak).start()


can_start = False

count_hai = 0
a = 0
while cap.isOpened():

    if a == 0:
        speak("Welcome to the Cardio training ")
        a = 1
    if count_hai < int(count):
        x = str(int(count))
        speak(x)
        count_hai = count
    ret, img = cap.read()  # 640 x 480
    img = cv2.flip(img, 1)
    # Determine dimensions of video - Help with creation of box in Line 43
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    # if not can_start:
    #     speak("You Can Start")
    #     can_start = True
    if len(lmList) != 0:
        r_hip_angle = detector.findAngle(img, 11, 23, 25)
        l_hip_angle = detector.findAngle(img, 12, 24, 26)
        l_elbow = detector.findAngle(img, 11, 13, 15)
        r_elbow = detector.findAngle(img, 12, 14, 16)
        l_shoulder_angle = detector.findAngle(img, 23, 11, 13)
        r_shoulder_angle = detector.findAngle(img, 24, 12, 14)
        l_knee = detector.findAngle(img, 23, 25, 27)
        r_knee = detector.findAngle(img, 24, 26, 28)

        bar = np.interp(r_hip_angle, (90, 110), (0, 100))
        per = np.interp(r_hip_angle, (90, 110), (350, 50))

        if r_hip_angle > 160 and l_hip_angle > 160 and direction == 0 and r_shoulder_angle < 40 and l_shoulder_angle < 40 and l_knee>165 and r_knee>165:
            feedback = "squeeze"
            print("sq")
            count += 0.5
            direction = 1

        if r_hip_angle < 160 and l_hip_angle < 160 and direction == 1 and r_shoulder_angle > 120 and l_shoulder_angle > 120 and l_knee>165 and r_knee>165:
            feedback = "stretch"
            print("str")
            count += 0.5
            direction = 0
        # Draw Bar

        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            # cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
            #             (255, 0, 0), 2)

        # Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        # Feedback
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    cv2.imshow('Pushup counter', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
