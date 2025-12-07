import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content("Hello, how are you?")
    print("Response:", response.text)
except Exception as e:
    print(f"Error: {e}")