import os
import requests
from dotenv import load_dotenv
from backend.command import speak

def google_search(query):
    try:
        load_dotenv()
        api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        search_engine_id = os.getenv('SEARCH_ENGINE_ID')
        
        if not api_key or not search_engine_id:
            return "Google Search API credentials not found"
        
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' in data:
            results = []
            for item in data['items'][:3]:  # Get top 3 results
                results.append(f"{item['title']}: {item['snippet']}")
            
            search_results = "Here are the search results: " + ". ".join(results)
            speak("I found some search results for you")
            return search_results
        else:
            speak("No search results found")
            return "No results found"
    except Exception as e:
        speak("Error performing search")
        return f"Search error: {e}"