import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module

def run_high_knees():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    feedback = "Start"
    state = 0
    last_state = 0
    
    # Create fullscreen window
    window_name = 'High Knees Counter'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
            
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        # Create semi-transparent top bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (40, 40, 40), cv2.FILLED)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

        if len(lmList) != 0:
            l_hip_y = lmList[23][2]
            l_knee_y = lmList[25][2]
            r_hip_y = lmList[24][2]
            r_knee_y = lmList[26][2]
            
            is_left_up = l_knee_y < l_hip_y
            is_right_up = r_knee_y < r_hip_y
            
            if is_left_up and state != 1:
                state = 1
                count += 0.5
                feedback = "Left"
            elif is_right_up and state != 2:
                state = 2
                count += 0.5
                feedback = "Right"
            elif not is_left_up and not is_right_up:
                state = 0

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
        feedback_color = (0, 255, 0) if feedback in ["Left", "Right"] else (0, 200, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(img, feedback, (text_x, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, feedback_color, 3)

        cv2.imshow(window_name, img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    database.save_session("High Knees", int(count), calories_module.calculate_calories("High Knees", int(count)))
