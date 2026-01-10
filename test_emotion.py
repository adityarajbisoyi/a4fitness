"""
Test script to verify emotion detection functionality
"""

import cv2
import face_emotion_module

def test_emotion_detection():
    print("Testing Emotion Detection...")
    print("=" * 50)
    
    # Initialize detector
    try:
        detector = face_emotion_module.EmotionDetector()
        print("✅ Emotion detector initialized")
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        return
    
    # Try to open camera
    cap = None
    for camera_index in [0, 1, 2]:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            print(f"✅ Camera opened on index {camera_index}")
            break
        cap.release()
    
    if not cap or not cap.isOpened():
        print("❌ Could not access camera")
        return
    
    print("\nPress 'q' to quit")
    print("Try different expressions:")
    print("  - Smile for 'Happy 😃'")
    print("  - Open mouth wide for 'Strain 😫'")
    print("  - Neutral face for 'Focused 😐'")
    print()
    
    frame_count = 0
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        
        img = cv2.flip(img, 1)
        
        try:
            # Detect emotion
            emotion, img = detector.detect_emotion(img, draw=True)
            
            # Display emotion prominently
            cv2.rectangle(img, (10, 10), (400, 80), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, f"Emotion: {emotion}", (20, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
            
            # Print to console every 30 frames
            if frame_count % 30 == 0:
                print(f"Detected: {emotion}")
            
            frame_count += 1
            
        except Exception as e:
            cv2.putText(img, f"Error: {str(e)[:50]}", (10, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            print(f"Error processing frame: {e}")
        
        cv2.imshow('Emotion Detection Test', img)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Test completed")

if __name__ == "__main__":
    test_emotion_detection()
