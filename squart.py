import cv2
import numpy as np
import PoseModule as pm
import database
import calories_module

class SquatCounter:
    """Reusable squat counting logic for both standalone and auto-detect modes"""
    def __init__(self, ai_coach=None):
        self.count = 0
        self.direction = 0
        self.form = 0
        self.threshold = 100
        self.arr = []
        self.shoulder_level = 0
        self.feedback = "Fix Form"
        self.ai_coach = ai_coach
        self.last_rep_update = 0
    
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
        
        count_increment = 0
        
        if self.form == 1:
            if per > 85:
                if knee > 140 and hip > 140:
                    self.feedback = "Down"
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
            
            if per < 15:
                difference = 0
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

def run_squat(ai_coach=None):
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not access camera!")
        return
    
    detector = pm.poseDetector()
    counter = SquatCounter(ai_coach=ai_coach)
    
    # Create fullscreen window
    window_name = 'Squat counter'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Check for stop signal from AI coach
    while cap.isOpened() and (not ai_coach or not getattr(ai_coach, 'stop_exercise_flag', False)):
        ret, img = cap.read()  # 640 x 480
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        h, w, c = img.shape

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        # Use the counter class
        count_increment, feedback = counter.process_frame(lmList, detector)
        
        # Create semi-transparent top bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        if len(lmList) != 0:
            knee = detector.findAngle(img, 11, 13, 15, draw=False)
            per = np.interp(knee, (90, 160), (0, 100))

            # Draw Progress Bar (right side)
            if counter.form == 1:
                bar_x = w - 60
                bar_width = 30
                bar_height = h - 200
                bar_y_start = 100
                
                cv2.rectangle(img, (bar_x, bar_y_start), (bar_x + bar_width, bar_y_start + bar_height), (60, 60, 60), cv2.FILLED)
                cv2.rectangle(img, (bar_x, bar_y_start), (bar_x + bar_width, bar_y_start + bar_height), (200, 200, 200), 2)
                
                progress_height = int(np.interp(per, (0, 100), (0, bar_height)))
                bar_color = (0, 255, 0) if per > 70 else (0, 165, 255) if per > 40 else (0, 100, 255)
                cv2.rectangle(img, (bar_x, bar_y_start + bar_height - progress_height), 
                            (bar_x + bar_width, bar_y_start + bar_height), bar_color, cv2.FILLED)
                
                cv2.putText(img, f'{int(per)}%', (bar_x - 10, bar_y_start + bar_height + 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Counter Panel
        counter_panel_w = 150
        counter_panel_h = 120
        counter_panel_x = 20
        counter_panel_y = h - counter_panel_h - 20
        
        overlay = img.copy()
        cv2.rectangle(overlay, (counter_panel_x, counter_panel_y), 
                     (counter_panel_x + counter_panel_w, counter_panel_y + counter_panel_h), 
                     (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
        cv2.rectangle(img, (counter_panel_x, counter_panel_y), 
                     (counter_panel_x + counter_panel_w, counter_panel_y + counter_panel_h), 
                     (0, 200, 255), 3)
        
        cv2.putText(img, "REPS", (counter_panel_x + 35, counter_panel_y + 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        cv2.putText(img, str(int(counter.count)), (counter_panel_x + 45, counter_panel_y + 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 255), 3)

        # Feedback centered at top
        feedback_color = (0, 255, 0) if feedback in ["Up", "Down"] else (0, 200, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(img, feedback, (text_x, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, feedback_color, 3)
        
        cv2.imshow(window_name, img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Squats", int(counter.count), calories_module.calculate_calories("Squats", int(counter.count)))