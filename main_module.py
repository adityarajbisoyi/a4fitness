import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module
import ai_coach_module
import face_emotion_module

class PushupCounter:
    """Reusable pushup counting logic for both standalone and auto-detect modes"""
    def __init__(self):
        self.count = 0
        self.direction = 0
        self.form = 0
        self.feedback = "Fix Form"
    
    def process_frame(self, lmList, detector):
        """Process pose and return count increment"""
        if len(lmList) == 0:
            return 0, self.feedback
        
        # Temporarily set the detector's lmList for findAngle to work
        detector.lmList = lmList
        
        elbow = detector.findAngle(None, 11, 13, 15, draw=False)
        shoulder = detector.findAngle(None, 13, 11, 23, draw=False)
        hip = detector.findAngle(None, 11, 23, 25, draw=False)
        
        per = np.interp(elbow, (90, 160), (0, 100))
        
        # Check to ensure right form before starting
        if elbow > 160 and shoulder > 40 and hip > 160:
            self.form = 1
        
        count_increment = 0
        
        if self.form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    self.feedback = "Up"
                    if self.direction == 0:
                        count_increment = 0.5
                        self.count += 0.5
                        self.direction = 1
                else:
                    self.feedback = "Fix Form"
            
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    self.feedback = "Down"
                    if self.direction == 1:
                        count_increment = 0.5
                        self.count += 0.5
                        self.direction = 0
                else:
                    self.feedback = "Fix Form"
        
        return count_increment, self.feedback

def run_pushup():
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
    coach = ai_coach_module.AICoach()
    emotion_detector = face_emotion_module.EmotionDetector()
    counter = PushupCounter()
    score = 0
    last_feedback = ""

    while cap.isOpened():
        ret, img = cap.read()  # 640 x 480
        if not ret:
            break
            
        img =  cv2.flip(img,1)
        # Determine dimensions of video - Help with creation of box in Line 43
        width = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        # print(width, height)

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        # Use the counter class
        count_increment, feedback = counter.process_frame(lmList, detector)
        
        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            
            # Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))
            
            # Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))
            
            # AI Coach Analysis
            score, detailed_feedback = coach.evaluate_pushup(lmList)
            if detailed_feedback:
                 feedback = detailed_feedback

            # Voice Feedback Logic
            if feedback != last_feedback:
                if feedback in ["Up", "Down"]:
                    utils.speak(feedback)
                elif feedback == "Fix Form" and last_feedback != "Fix Form":
                    utils.speak("Fix Form")
                last_feedback = feedback

            print(counter.count)

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

            # Rep Quality Score Display
            cv2.rectangle(img, (0, 0), (250, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, f"Form Score: {int(score)}%", (10, 30), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255) if score < 70 else (0, 255, 0), 2)

        # Face Emotion Detection (always try, even if no pose detected)
        try:
            emotion, img = emotion_detector.detect_emotion(img, draw=True)
            
            # Display emotion prominently at top
            cv2.rectangle(img, (250, 0), (500, 40), (50, 50, 50), cv2.FILLED)
            cv2.putText(img, f"Mood: {emotion}", (260, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
            
            # Motivational Voice check
            if len(lmList) != 0 and emotion == "Strain 😫" and per > 50: # Straining during rep
                 # This would be where we add specific motivational voice lines
                 pass
        except Exception as e:
            # Silently handle emotion detection errors
            cv2.putText(img, "Emotion: N/A", (260, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 1, (128, 128, 128), 1)


        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Pushups", int(counter.count), calories_module.calculate_calories("Pushups", int(counter.count)))
