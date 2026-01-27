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
    def __init__(self, ai_coach=None):
        self.count = 0
        self.direction = 0
        self.form = 0
        self.feedback = "Fix Form"
        self.ai_coach = ai_coach
        self.last_rep_update = 0
    
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
                        # Notify AI Coach
                        if self.ai_coach and int(self.count) != self.last_rep_update:
                            self.last_rep_update = int(self.count)
                            self.ai_coach.update_rep_count(int(self.count))
                else:
                    self.feedback = "Fix Form"
            
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    self.feedback = "Down"
                    if self.direction == 1:
                        count_increment = 0.5
                        self.count += 0.5
                        self.direction = 0
                        # Notify AI Coach
                        if self.ai_coach and int(self.count) != self.last_rep_update:
                            self.last_rep_update = int(self.count)
                            self.ai_coach.update_rep_count(int(self.count))
                else:
                    self.feedback = "Fix Form"
        
        # Notify AI Coach about form issues
        if self.ai_coach and self.feedback:
            self.ai_coach.notify_exercise_feedback(self.feedback)
        
        return count_increment, self.feedback

def run_pushup(ai_coach=None):
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
    counter = PushupCounter(ai_coach=ai_coach)
    score = 0
    last_feedback = ""
    
    # Create named window and set it to fullscreen
    window_name = 'Pushup counter'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Check for stop signal from AI coach
    while cap.isOpened() and (not ai_coach or not getattr(ai_coach, 'stop_exercise_flag', False)):
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
        
        # Get screen dimensions for responsive UI
        h, w, c = img.shape
        
        # Use the counter class
        count_increment, feedback = counter.process_frame(lmList, detector)
        
        # Create semi-transparent overlay for top info bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            
            # Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))
            
            # Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (h-100, 100))
            
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

            # Draw Progress Bar (right side, cleaner design)
            if counter.form == 1:
                bar_x = w - 60
                bar_width = 30
                bar_height = h - 200
                bar_y_start = 100
                
                # Background bar
                cv2.rectangle(img, (bar_x, bar_y_start), (bar_x + bar_width, bar_y_start + bar_height), (60, 60, 60), cv2.FILLED)
                cv2.rectangle(img, (bar_x, bar_y_start), (bar_x + bar_width, bar_y_start + bar_height), (200, 200, 200), 2)
                
                # Progress bar with gradient effect
                progress_height = int(np.interp(per, (0, 100), (0, bar_height)))
                bar_color = (0, 255, 0) if per > 70 else (0, 165, 255) if per > 40 else (0, 100, 255)
                cv2.rectangle(img, (bar_x, bar_y_start + bar_height - progress_height), 
                            (bar_x + bar_width, bar_y_start + bar_height), bar_color, cv2.FILLED)
                
                # Percentage text below bar
                cv2.putText(img, f'{int(per)}%', (bar_x - 10, bar_y_start + bar_height + 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Counter Display (left side with modern panel)
        counter_panel_w = 150
        counter_panel_h = 120
        counter_panel_x = 20
        counter_panel_y = h - counter_panel_h - 20
        
        # Semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (counter_panel_x, counter_panel_y), 
                     (counter_panel_x + counter_panel_w, counter_panel_y + counter_panel_h), 
                     (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
        
        # Border
        cv2.rectangle(img, (counter_panel_x, counter_panel_y), 
                     (counter_panel_x + counter_panel_w, counter_panel_y + counter_panel_h), 
                     (0, 200, 255), 3)
        
        # Label
        cv2.putText(img, "REPS", (counter_panel_x + 35, counter_panel_y + 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        
        # Count
        cv2.putText(img, str(int(counter.count)), (counter_panel_x + 45, counter_panel_y + 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 255), 3)

        # Top Info Bar - Form Score (left)
        form_score_color = (0, 255, 0) if score > 70 else (0, 200, 255) if score > 50 else (0, 100, 255)
        cv2.putText(img, f"FORM: {int(score)}%", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, form_score_color, 2)
        
        # Top Info Bar - Feedback (center)
        feedback_color = (0, 255, 0) if feedback in ["Up", "Down"] else (0, 200, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(img, feedback, (text_x, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, feedback_color, 3)

        # Face Emotion Detection
        emotion = "Neutral"
        try:
            emotion, img = emotion_detector.detect_emotion(img, draw=False)
            
            # Display emotion at top right
            mood_text = f"MOOD: {emotion}"
            text_size = cv2.getTextSize(mood_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
            cv2.putText(img, mood_text, (w - text_size[0] - 20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 100), 2)
            
            # Motivational Voice check
            if len(lmList) != 0 and emotion == "Strain" and per > 50:
                 pass
        except Exception as e:
            cv2.putText(img, "MOOD: --", (w - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (128, 128, 128), 2)


        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Pushups", int(counter.count), calories_module.calculate_calories("Pushups", int(counter.count)))
