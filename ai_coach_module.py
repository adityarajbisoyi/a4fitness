
import math

class AICoach:
    def __init__(self):
        pass

    def calculate_angle(self, lm_list, p1, p2, p3):
        """Calculates angle between three points p1-p2-p3"""
        if not lm_list or len(lm_list) < 33:
            return 0
            
        # Get coordinates
        x1, y1 = lm_list[p1][1:]
        x2, y2 = lm_list[p2][1:]
        x3, y3 = lm_list[p3][1:]

        # Calculate Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 180:
            angle = 360 - angle
            
        return angle

    def evaluate_squat(self, lm_list):
        """
        Evaluates a squat pose.
        Returns: (score (0-100), feedback_string)
        """
        if not lm_list:
            return 0, "No Body Detected"

        # Landmarks: 23=Left Hip, 25=Left Knee, 27=Left Ankle
        # 11=Left Shoulder
        
        knee_angle = self.calculate_angle(lm_list, 23, 25, 27)
        hip_angle = self.calculate_angle(lm_list, 11, 23, 25) # Torso-Thigh angle

        score = 0
        feedback = "Good"

        # Depth Analysis (Knee Angle)
        # Deep squat ~ < 90 degree. Parallel ~ 90-100.
        if knee_angle < 80:
            score = 100
            feedback = "Perfect Depth! 🔥"
        elif 80 <= knee_angle <= 100:
            score = 90
            feedback = "Good Depth"
        elif 100 < knee_angle <= 130:
            score = 60
            feedback = "Go Lower!"
        else:
            score = 10
            feedback = "Squat Down"

        # Form Analysis (Back Stability)
        # If hip angle is too small, they are leaning forward too much
        if hip_angle < 70:
            score -= 20
            feedback = "Keep Back Straight"
        
        return max(0, min(100, score)), feedback

    def evaluate_pushup(self, lm_list):
        """
        Evaluates a pushup pose.
        """
        if not lm_list:
            return 0, ""
            
        # 11=Shoulder, 13=Elbow, 15=Wrist
        elbow_angle = self.calculate_angle(lm_list, 11, 13, 15)
        
        # 11=Shoulder, 23=Hip, 25=Knee
        body_straightness = self.calculate_angle(lm_list, 11, 23, 25)
        
        score = 0
        feedback = ""
        
        # Depth
        if elbow_angle < 90:
            score = 100
            feedback = "Perfect Depth!"
        elif elbow_angle < 120:
            score = 80
            feedback = "Good"
        else:
            score = 40
            feedback = "Go Lower"
            
        # Body Line (Plank form)
        if body_straightness < 150:
             score -= 30
             feedback = "Don't sagging hips"
             
        return max(0, min(100, score)), feedback
