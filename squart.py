import cv2
import numpy as np
import PoseModule as pm
import database
import calories_module

class SquatCounter:
    """Reusable squat counting logic for both standalone and auto-detect modes"""
    def __init__(self):
        self.count = 0
        self.direction = 0
        self.form = 0
        self.threshold = 100
        self.arr = []
        self.shoulder_level = 0
        self.feedback = "Fix Form"
    
    def process_frame(self, lmList, detector):
        """Process pose and return count increment"""
        if len(lmList) == 0:
            if len(self.arr):
                self.arr.pop()
            return 0, self.feedback
        
        # Temporarily set the detector's lmList for findAngle to work
        detector.lmList = lmList
        
        hip = detector.findAngle(None, 11, 23, 25, draw=False)
        knee = detector.findAngle(None, 23, 25, 27, draw=False)
        per = np.interp(knee, (90, 160), (0, 100))
        
        # Check to ensure right form before starting
        if knee > 160 and hip > 160:
            self.shoulder_level = lmList[11][2]
            self.form = 1
            if not len(self.arr):
                self.arr.append(self.shoulder_level)
            else:
                current_level = lmList[11][2]
                difference = abs(self.arr[0] - current_level)
        
        count_increment = 0
        
        if self.form == 1:
            if per > 85:
                if knee > 140 and hip > 140:
                    self.feedback = "Down"
                    if self.direction == 0:
                        count_increment = 0.5
                        self.count += 0.5
                        self.direction = 1
                else:
                    self.feedback = "Fix Form"
            
            if per < 15:
                if not len(self.arr):
                    self.arr.append(self.shoulder_level)
                else:
                    current_level = lmList[11][2]
                    difference = abs(self.arr[0] - current_level)
                
                if knee < 90 and hip < 120 and (difference > self.threshold):
                    self.feedback = "Up"
                    if self.direction == 1:
                        count_increment = 0.5
                        self.count += 0.5
                        self.direction = 0
                else:
                    self.feedback = "Fix Form"
        
        return count_increment, self.feedback

def run_squat():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not access camera!")
        return
    
    detector = pm.poseDetector()
    counter = SquatCounter()
    
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
        
        # Use the counter class
        count_increment, feedback = counter.process_frame(lmList, detector)
        
        if len(lmList) != 0:
            knee = detector.findAngle(img, 23, 25, 27)
            per = np.interp(knee, (90, 160), (0, 100))
            bar = np.interp(knee, (90, 160), (380, 50))

            # Draw Bar
            if counter.form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

            # Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(counter.count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        
        cv2.imshow('Squat counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Squats", int(counter.count), calories_module.calculate_calories("Squats", int(counter.count)))