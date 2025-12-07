import time
import pyttsx3
import speech_recognition as sr
import eel
import threading

def speak(text):
    try:
        text = str(text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        
        # Set voice
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        elif len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        
        # Faster speech settings
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.9)
        
        print(f"Speaking: {text}")
        eel.DisplayMessage(text)
        eel.receiverText(text)
        
        # Quick speech without blocking
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Speech error: {e}")
        eel.DisplayMessage(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    r.energy_threshold = 250
    r.pause_threshold = 0.5  # Faster response
    r.dynamic_energy_threshold = True
    
    try:
        # Use the best microphone
        mic_index = None
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            if "NVIDIA Broadcast" in name or "Realtek" in name:
                mic_index = i
                break
        
        with sr.Microphone(device_index=mic_index) as source:
            r.adjust_for_ambient_noise(source, duration=0.3)  # Faster adjustment
            audio = r.listen(source, timeout=2, phrase_time_limit=4)  # Shorter timeouts
        
        # Quick recognition
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
        
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        speak("I'm listening")
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            speak("I didn't hear anything. Please try again.")
            return "no_query"  # Return something
        print(f"Voice command: {query}")
        eel.senderText(query)
        speak(f"I heard: {query}")
    else:
        query = message  # If there's a message, use it
        print(f"Text message: {query}")
        eel.senderText(query)

    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            elif "weather" in query:
                from backend.weather import get_weather
                city = query.replace("weather", "").replace("in", "").strip()
                if not city:
                    city = "London"
                get_weather(city)
            elif "search" in query:
                from backend.search import google_search
                search_term = query.replace("search", "").strip()
                google_search(search_term)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")

    eel.ShowHood()
    return "done"

# Conversation mode variables
conversation_active = False
conversation_thread = None

@eel.expose
def startConversationMode():
    global conversation_active, conversation_thread
    conversation_active = True
    speak("Conversation mode activated. I'm listening continuously.")
    conversation_thread = threading.Thread(target=continuousListening)
    conversation_thread.daemon = True
    conversation_thread.start()
    return "conversation_started"

@eel.expose
def stopConversationMode():
    global conversation_active
    conversation_active = False
    speak("Conversation mode deactivated.")
    return "conversation_stopped"

def continuousListening():
    global conversation_active
    while conversation_active:
        try:
            query = takecommand()
            if query and conversation_active:
                print(f"Continuous voice: {query}")
                eel.senderText(query)
                # Process command in separate thread to allow concurrent listening
                command_thread = threading.Thread(target=processCommand, args=(query,))
                command_thread.daemon = True
                command_thread.start()
                if "stop conversation" in query or "exit conversation" in query:
                    break
            elif conversation_active:
                time.sleep(0.5)  # Shorter sleep for faster response
        except Exception as e:
            print(f"Continuous listening error: {e}")
            time.sleep(1)

def processCommand(query):
    try:
        if "open" in query:
            from backend.feature import openCommand
            openCommand(query)
        elif "send message" in query or "call" in query or "video call" in query:
            from backend.feature import findContact, whatsApp
            flag = ""
            Phone, name = findContact(query)
            if Phone != 0:
                if "send message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    query = takecommand()
                elif "call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                whatsApp(Phone, query, flag, name)
        elif "on youtube" in query:
            from backend.feature import PlayYoutube
            PlayYoutube(query)
        elif "weather" in query:
            from backend.weather import get_weather
            city = query.replace("weather", "").replace("in", "").strip()
            if not city:
                city = "London"
            get_weather(city)
        elif "search" in query:
            from backend.search import google_search
            search_term = query.replace("search", "").strip()
            google_search(search_term)
        else:
            from backend.feature import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Command processing error: {e}")
        speak("Sorry, something went wrong.")
