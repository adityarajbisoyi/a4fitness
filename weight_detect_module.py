
import cv2
import numpy as np

class WeightDetector:
    def __init__(self):
        # HSV Ranges for Gym Equipment Colors
        self.colors = {
            "Red (5kg)": ((0, 150, 50), (10, 255, 255)),     # Lower Red
            "Red_2":     ((170, 150, 50), (180, 255, 255)),  # Upper Red
            "Blue (10kg)": ((100, 150, 0), (140, 255, 255)), # Blue
            "Black (20kg)": ((0, 0, 0), (180, 255, 30))      # Black (Very low Value)
        }

    def detect_weight(self, img_roi):
        """
        Analyzes an ROI to guess the dumbell weight based on color.
        Returns: (inferred_weight_kg, color_name)
        """
        hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        
        max_area = 0
        detected_weight = 0
        detected_color = "Unknown"
        
        for name, (lower, upper) in self.colors.items():
            lower = np.array(lower)
            upper = np.array(upper)
            
            mask = cv2.inRange(hsv, lower, upper)
            
            # Count pixels
            area = cv2.countNonZero(mask)
            
            if area > max_area and area > 500: # Threshold
                max_area = area
                detected_color = name
                
                if "Red" in name: detected_weight = 5
                elif "Blue" in name: detected_weight = 10
                elif "Black" in name: detected_weight = 20
                
        return detected_weight, detected_color

def scan_for_weight():
    """ Runs a standalone weight scanner loop """
    cap = cv2.VideoCapture(1) # Default camera
    detector = WeightDetector()
    
    while True:
        success, img = cap.read()
        if not success: break
        
        h, w, c = img.shape
        
        # Define ROI (Center Box)
        roi_size = 200
        x1 = w//2 - roi_size//2
        y1 = h//2 - roi_size//2
        x2 = x1 + roi_size
        y2 = y1 + roi_size
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, "Place Weight Here", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        roi = img[y1:y2, x1:x2]
        if roi.size > 0:
            weight, color = detector.detect_weight(roi)
            
            if weight > 0:
                text = f"Detected: {color} ({weight}kg)"
                cv2.rectangle(img, (x1, y2), (x2, y2+40), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, text, (x1, y2+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        cv2.imshow("Auto Weight Detect", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_for_weight()
