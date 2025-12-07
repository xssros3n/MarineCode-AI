# import playsound
# import eel


# @eel.expose
# def playAssistantSound():
#     music_dir = "frontend\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)


from compileall import compile_path
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
import google.generativeai as genai
from dotenv import load_dotenv 
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3

from backend.helper import extract_yt_term, remove_words
conn = sqlite3.connect("marinecode.db")
cursor = conn.cursor()
# Initialize pygame mixer
pygame.mixer.init()

# Define the function to play sound
@eel.expose
def play_assistant_sound():
    sound_file = os.path.join("frontend", "assets", "audio", "start_sound.mp3")
    if os.path.exists(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    else:
        print(f"Audio file not found: {sound_file}")
    return "sound_played"
    
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["Marine Code","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        MarineCode_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        MarineCode_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        MarineCode_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(MarineCode_message)


def chatBot(query):
    try:
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            speak("Google API key not found")
            return "API key missing"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(query)
        response_text = response.text
        print(response_text)
        speak(response_text)
        return response_text
    except Exception as e:
        print(f"Error: {e}")
        # Fallback responses when API quota exceeded
        fallback_response = getFallbackResponse(query)
        speak(fallback_response)
        return fallback_response

def getFallbackResponse(query):
    query = query.lower()
    if "hello" in query or "hi" in query:
        return "Hello! I'm here to help you. My AI quota is temporarily limited, but I'm still listening!"
    elif "how are you" in query:
        return "I'm doing great! Ready to assist you with commands like opening apps or playing music."
    elif "what" in query and "time" in query:
        import datetime
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif "weather" in query:
        return "I can check weather for you, but my AI responses are limited right now."
    elif "thank" in query:
        return "You're welcome! Happy to help anytime."
    elif "bye" in query or "goodbye" in query:
        return "Goodbye! Have a great day!"
    else:
        return "I heard you! My AI quota is temporarily limited, but I can still help with opening apps, playing music, or other commands."