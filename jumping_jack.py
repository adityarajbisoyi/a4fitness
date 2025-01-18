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
threshold=100
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
    threading.Thread(target= _speak).start()
count_hai = 0
a = 0
while cap.isOpened():
    if form == 0 and time.time() -start_time >= timeout:
        print('u are stoped')
    if a == 0:
        speak("welcome to the squat training ")
        a = 1
    if count_hai<int(count):
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
    if len(lmList) !=0:
        r_hip_angle = detector.findAngle(img, 23, 24, 26)
        l_hip_angle = detector.findAngle(img, 24, 23, 25)
        hp_angel = detector.findAngle(img, 11, 23, 25)
        hp_angle2 = detector.findAngle(img, 12, 24, 26)
        lfoot_level = lmList[27][2]
        rfoot_level = lmList[28][2]
        bar =np.interp(r_hip_angle, (90, 110), (0, 100))
        per = np.interp(r_hip_angle, (90, 110), (350,50))


        if r_hip_angle>90 and l_hip_angle>90 and hp_angle2 <175 and hp_angel <175:
            feedback = "correct position"
            form = 1
            print("form  = 1")

            if form == 1 and r_hip_angle >110 and l_hip_angle>110 and direction == 0 and hp_angle2 <150 and hp_angel <150:
                feedback = "squeeze"
                print("sq")
                count +=0.5
                direction = 1

            if form == 1 and r_hip_angle < 100 and l_hip_angle <100 and direction == 1 and hp_angle2 >150 and hp_angel >150:
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
