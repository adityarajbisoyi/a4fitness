
import cv2
import mediapipe as mp
import math

class EmotionDetector:
    def __init__(self):
        try:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            self.mp_draw = mp.solutions.drawing_utils
            self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)
            self.initialized = True
            print("✅ Emotion Detector initialized successfully")
        except Exception as e:
            print(f"⚠️  Emotion Detector initialization failed: {e}")
            self.initialized = False

    def detect_emotion(self, img, draw=True):
        """
        Detects emotion from image.
        Returns: (emotion_string, img_with_drawing)
        """
        if not self.initialized:
            return "N/A", img
        
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(img_rgb)
            
            emotion = "Neutral"
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Get landmarks
                    h, w, c = img.shape
                    
                    # Helper to get coords
                    def get_coords(idx):
                        lm = face_landmarks.landmark[idx]
                        return int(lm.x * w), int(lm.y * h)
                    
                    # Smile Detection (Lip Corners vs Top/Bottom Lip)
                    # 61: Left Corner, 291: Right Corner
                    # 0: Top Lip Center, 17: Bottom Lip Center
                    left_corner = get_coords(61)
                    right_corner = get_coords(291)
                    top_lip = get_coords(0)
                    bottom_lip = get_coords(17)
                    
                    mouth_width = math.dist(left_corner, right_corner)
                    mouth_height = math.dist(top_lip, bottom_lip)
                    
                    # Check if corners are above the lip center (Smile)
                    # Y increases downwards. So if corner_y < lip_center_y, it's a smile
                    avg_corner_y = (left_corner[1] + right_corner[1]) / 2
                    avg_lip_y = (top_lip[1] + bottom_lip[1]) / 2
                    
                    # Improved emotion detection logic
                    if avg_corner_y < avg_lip_y - 5:  # Corners lifted (smile)
                        emotion = "Happy"
                    elif mouth_height > 25:  # Mouth open wide
                        emotion = "Strain"
                    elif mouth_height > 15:  # Mouth slightly open
                        emotion = "Focused"
                    else:
                        emotion = "Neutral"
                        
                    # Draw emotion text prominently
                    if draw:
                        # Draw background box for better visibility
                        text_size = cv2.getTextSize(emotion, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                        box_x = left_corner[0] - 10
                        box_y = left_corner[1] - 70
                        
                        cv2.rectangle(img, 
                                    (box_x, box_y - text_size[1] - 10), 
                                    (box_x + text_size[0] + 20, box_y + 10), 
                                    (0, 0, 0), cv2.FILLED)
                        
                        cv2.putText(img, emotion, (box_x + 10, box_y), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        
                        # Optional: Draw face mesh for debugging
                        # self.mp_draw.draw_landmarks(
                        #     img, face_landmarks, self.mp_face_mesh.FACEMESH_CONTOURS,
                        #     self.draw_spec, self.draw_spec)
                        
            return emotion, img
            
        except Exception as e:
            print(f"⚠️  Emotion detection error: {e}")
            return "Error", img
