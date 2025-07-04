import requests
from bs4 import BeautifulSoup
import re

URLS = {
    "Drama": 'https://www.imdb.com/search/title/?title_type=feature&genres=drama',
    "Action": 'https://www.imdb.com/search/title/?title_type=feature&genres=action',
    "Comedy": 'https://www.imdb.com/search/title/?title_type=feature&genres=comedy',
    "Horror": 'https://www.imdb.com/search/title/?title_type=feature&genres=horror',
    "Crime": 'https://www.imdb.com/search/title/?title_type=feature&genres=crime',
}

def get_titles(emotion):
    url = URLS.get(emotion.capitalize())
    if not url:
        return []

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "lxml")
    titles = [a.get_text() for a in soup.find_all('a', href=re.compile(r'/title/tt\d+/'))]
    return list(dict.fromkeys(titles))[:10]  # remove duplicates

# Vercel handler
def handler(request, response):
    try:
        emotion = request.query.get("emotion", "").capitalize()
        titles = get_titles(emotion)
        return response.json({"emotion": emotion, "movies": titles})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
