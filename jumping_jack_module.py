import cv2
import numpy as np
import PoseModule as pm
import utils
import time
import database
import calories_module

class JumpingJackCounter:
    """Reusable jumping jack counting logic for both standalone and auto-detect modes"""
    def __init__(self):
        self.count = 0
        self.direction = 0  # 0 = arms down, 1 = arms up
        self.feedback = "Stand Ready"
    
    def process_frame(self, lmList):
        """Process pose and return count increment"""
        if len(lmList) == 0:
            return 0, self.feedback
        
        left_shoulder_y = lmList[11][2]
        right_shoulder_y = lmList[12][2]
        left_wrist_y = lmList[15][2]
        right_wrist_y = lmList[16][2]
        
        left_hip_x = lmList[23][1]
        right_hip_x = lmList[24][1]
        left_ankle_x = lmList[27][1]
        right_ankle_x = lmList[28][1]
        
        # Calculate leg spread
        leg_spread = abs(left_ankle_x - right_ankle_x)
        hip_width = abs(left_hip_x - right_hip_x)
        
        # Hands are UP when BOTH wrists are above shoulders
        hands_up = (left_wrist_y < left_shoulder_y - 30) and (right_wrist_y < right_shoulder_y - 30)
        
        # Legs are SPREAD when ankles are wider apart than hips
        legs_spread = leg_spread > (hip_width * 1.5)
        
        count_increment = 0
        
        # Position 1: Arms up, legs spread
        if hands_up and legs_spread:
            self.feedback = "Arms Up! ⬆️"
            if self.direction == 0:
                count_increment = 0.5
                self.count += 0.5
                self.direction = 1
                
        # Position 2: Arms down, legs together
        elif not hands_up and not legs_spread:
            self.feedback = "Arms Down ⬇️"
            if self.direction == 1:
                count_increment = 0.5
                self.count += 0.5
                self.direction = 0
        
        return count_increment, self.feedback

def run_jumping_jack():
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
    count = 0
    direction = 0  # 0 = arms down, 1 = arms up
    feedback = "Stand Ready"
    last_feedback = ""
    start_time = time.time()
    
    # Flag for welcome message
    welcome_said = False
    last_count = 0
    
    # Create fullscreen window
    window_name = 'Jumping Jack Counter'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        if not welcome_said:
            utils.speak("Welcome to jumping jack training")
            welcome_said = True

        if int(count) > last_count:
            utils.speak(str(int(count)))
            last_count = int(count)

        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        
        # Create semi-transparent top bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # Get key landmarks
            # 11 = Left Shoulder, 12 = Right Shoulder
            # 15 = Left Wrist, 16 = Right Wrist
            # 23 = Left Hip, 24 = Right Hip
            # 27 = Left Ankle, 28 = Right Ankle
            
            left_shoulder_y = lmList[11][2]
            right_shoulder_y = lmList[12][2]
            left_wrist_y = lmList[15][2]
            right_wrist_y = lmList[16][2]
            
            left_hip_x = lmList[23][1]
            right_hip_x = lmList[24][1]
            left_ankle_x = lmList[27][1]
            right_ankle_x = lmList[28][1]
            
            # Calculate average shoulder and wrist heights
            avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
            avg_wrist_y = (left_wrist_y + right_wrist_y) / 2
            
            # Calculate leg spread (distance between ankles)
            leg_spread = abs(left_ankle_x - right_ankle_x)
            hip_width = abs(left_hip_x - right_hip_x)
            
            # Hands are UP when wrists are above shoulders
            hands_up = (left_wrist_y < left_shoulder_y - 30) and (right_wrist_y < right_shoulder_y - 30)
            
            # Legs are SPREAD when ankles are wider apart than hips
            legs_spread = leg_spread > (hip_width * 1.5)
            
            # Jumping Jack Logic
            # Position 1: Arms up, legs spread
            if hands_up and legs_spread:
                feedback = "Arms Up"
                if direction == 0:
                    count += 0.5
                    direction = 1
                    
            # Position 2: Arms down, legs together
            elif not hands_up and not legs_spread:
                feedback = "Arms Down"
                if direction == 1:
                    count += 0.5
                    direction = 0
            else:
                if hands_up:
                    feedback = "Spread Legs"
                elif legs_spread:
                    feedback = "Raise Arms"
                else:
                    feedback = "Start Movement"
            
            # Draw visual indicators
            hand_color = (0, 255, 0) if hands_up else (100, 100, 100)
            leg_color = (0, 255, 0) if legs_spread else (100, 100, 100)
            
            cv2.circle(img, (lmList[15][1], lmList[15][2]), 10, hand_color, cv2.FILLED)
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 10, hand_color, cv2.FILLED)
            cv2.circle(img, (lmList[27][1], lmList[27][2]), 10, leg_color, cv2.FILLED)
            cv2.circle(img, (lmList[28][1], lmList[28][2]), 10, leg_color, cv2.FILLED)

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
        cv2.putText(img, str(int(count)), (counter_panel_x + 45, counter_panel_y + 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 255), 3)

        # Feedback centered at top
        feedback_color = (0, 255, 0) if feedback in ["Arms Up", "Arms Down"] else (0, 200, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(img, feedback, (text_x, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, feedback_color, 3)

        cv2.imshow('Jumping Jack Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("Jumping Jacks", int(count), calories_module.calculate_calories("Jumping Jacks", int(count)))
