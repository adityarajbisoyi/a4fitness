import cv2
import numpy as np
import PoseModule as pm
import utils
import database
import calories_module

def run_bicep_curl():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0  # 0 = down, 1 = up
    feedback = "Fix Form"
    last_feedback = ""
    
    # Create fullscreen window
    window_name = 'Bicep Curl Counter'
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
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16)
            
            # Map angle to percentage (approximate range for curl)
            per = np.interp(angle, (30, 160), (100, 0))

            # Logic
            if angle > 160:
                if direction == 1:
                    count += 0.5
                    direction = 0
                    feedback = "Down"
                else:
                    feedback = "Curl Up"

            if angle < 30:
                if direction == 0:
                    count += 0.5
                    direction = 1
                    feedback = "Up"
                else:
                    feedback = "Down"

            # Voice Feedback
            if feedback != last_feedback:
                if feedback in ["Up", "Down"]:
                    utils.speak(feedback)
                elif feedback == "Fix Form" and last_feedback != "Fix Form":
                    utils.speak("Fix Form")
                last_feedback = feedback

            # Draw Progress Bar (right side)
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
        cv2.putText(img, str(int(count)), (counter_panel_x + 45, counter_panel_y + 95), 
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
    database.save_session("Bicep Curls", int(count), calories_module.calculate_calories("Bicep Curls", int(count)))
