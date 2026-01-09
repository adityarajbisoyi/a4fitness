
import cv2
import mediapipe as mp
import math

class EmotionDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.draw_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

    def detect_emotion(self, img, draw=True):
        """
        Detects emotion from image.
        Returns: (emotion_string, img_with_drawing)
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        
        emotion = "Neutral"
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                if draw:
                    # Optional: Draw mesh
                    # self.mp_draw.draw_landmarks(img, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION, 
                    #                             self.draw_spec, self.draw_spec)
                    pass
                
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
                
                # Normalized metrics
                # Smile: Corners move up relative to center? Simplified: Mouth width increases significantly
                
                # Eyebrow Raise (Surprise/Happy)
                # 66: Right Eye Inner, 107: Right Eyebrow Inner
                # 296: Left Eye Inner, 336: Left Eyebrow Inner
                
                
                # Simple Heuristics
                # 1. Smile: Width is large relative to face width? 
                # Let's use Mouth Aspect Ratio or simply corner height vs lip center
                
                # Check if corners are above the lip center (Smile)
                # Y increases downwards. So if corner_y < lip_center_y, it's a smile
                avg_corner_y = (left_corner[1] + right_corner[1]) / 2
                avg_lip_y = (top_lip[1] + bottom_lip[1]) / 2
                
                if avg_corner_y < avg_lip_y - 2: # Threshold
                    emotion = "Happy 😃"
                elif mouth_height > 30: # Mouth open (gasping/shouting)
                    emotion = "Strain 😫"
                else:
                    emotion = "Focused 😐"
                    
                # Draw emotion text near face
                if draw:
                    cv2.putText(img, emotion, (left_corner[0], left_corner[1] - 50), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                    
        return emotion, img
