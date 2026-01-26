import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import time
import calories_module

def run_plank():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    
    start_time = 0
    total_time = 0
    is_planking = False
    feedback = "Fix Form"
    last_feedback = ""
    
    # Create fullscreen window
    window_name = 'Plank Timer'
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
            angle = detector.findAngle(img, 11, 23, 27)
            
            # Logic: Plank is roughly 170-180 degrees straight body
            if 170 < angle < 190:
                if not is_planking:
                    start_time = time.time()
                    is_planking = True
                    feedback = "Hold It"
                    utils.speak("Hold It")
                current_time = time.time()
                session_time = current_time - start_time
            else:
                if is_planking:
                    total_time += (time.time() - start_time)
                    is_planking = False
                    start_time = 0
                    feedback = "Fix Form"
                    utils.speak("Fix Form")
                session_time = 0

            display_time = total_time + session_time if is_planking else total_time
            
            # Draw timer panel (center)
            timer_panel_w = 250
            timer_panel_h = 120
            timer_panel_x = (w - timer_panel_w) // 2
            timer_panel_y = h - timer_panel_h - 20
            
            overlay = img.copy()
            cv2.rectangle(overlay, (timer_panel_x, timer_panel_y), 
                         (timer_panel_x + timer_panel_w, timer_panel_y + timer_panel_h), 
                         (40, 40, 40), cv2.FILLED)
            cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
            
            timer_color = (0, 255, 0) if is_planking else (0, 200, 255)
            cv2.rectangle(img, (timer_panel_x, timer_panel_y), 
                         (timer_panel_x + timer_panel_w, timer_panel_y + timer_panel_h), 
                         timer_color, 3)
            
            cv2.putText(img, "TIME", (timer_panel_x + 80, timer_panel_y + 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            cv2.putText(img, f"{int(display_time)}s", (timer_panel_x + 65, timer_panel_y + 95), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 255), 3)

        # Feedback centered at top
        feedback_color = (0, 255, 0) if feedback == "Hold It" else (0, 200, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = (w - text_size[0]) // 2
        cv2.putText(img, feedback, (text_x, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, feedback_color, 3)

        cv2.imshow(window_name, img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    # Add final session time if quit while planking
    if is_planking:
        total_time += (time.time() - start_time)

    cap.release()
    cv2.destroyAllWindows()
    # Saving time in "reps" column for simplicity, or we could handle differently
    database.save_session("Plank (Secs)", int(total_time), calories_module.calculate_calories("Plank (Secs)", int(total_time)))
