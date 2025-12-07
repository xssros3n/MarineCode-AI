import speech_recognition as sr
import pyttsx3

def test_microphone():
    r = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")
    
    # Test speech recognition
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            print("Say something!")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        print("Recognizing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        
        # Test text-to-speech
        engine = pyttsx3.init()
        engine.say(f"I heard you say: {text}")
        engine.runAndWait()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_microphone()