import os
import requests
from dotenv import load_dotenv
from backend.command import speak

def get_weather(city="London"):
    try:
        load_dotenv()
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            return "Weather API key not found"
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            weather_info = f"The weather in {city} is {description} with temperature {temp} degrees Celsius"
            speak(weather_info)
            return weather_info
        else:
            speak("Sorry, I couldn't get weather information")
            return "Weather data unavailable"
    except Exception as e:
        speak("Error getting weather information")
        return f"Error: {e}"