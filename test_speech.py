"""
Test script for speech recognition functionality
"""

import speech_recognition as sr

def test_microphone():
    print("Testing Speech Recognition...")
    print("=" * 50)
    
    # Check if microphone is available
    print("\n1. Checking for microphones...")
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"✅ Found {len(mic_list)} microphone(s):")
        for i, name in enumerate(mic_list):
            print(f"   [{i}] {name}")
    except Exception as e:
        print(f"❌ Error listing microphones: {e}")
        return
    
    # Test microphone access
    print("\n2. Testing microphone access...")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("✅ Microphone accessed successfully")
            print("\n3. Adjusting for ambient noise (please wait)...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Ambient noise adjustment complete")
            
            print("\n4. Listening for speech...")
            print("   Say something (e.g., 'start pushups')...")
            print("   Listening for 5 seconds...")
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("✅ Audio captured")
            
            print("\n5. Recognizing speech...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"✅ You said: '{text}'")
                print(f"   (lowercase: '{text.lower()}')")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Google Speech Recognition error: {e}")
                
    except OSError as e:
        print(f"❌ Microphone access error: {e}")
        print("\nPossible solutions:")
        print("  • Check microphone permissions in Windows Settings")
        print("  • Make sure microphone is not being used by another app")
        print("  • Try running as administrator")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    test_microphone()
