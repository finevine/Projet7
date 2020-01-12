import requests
import re
from bs4 import BeautifulSoup
from config import GMAP_API_KEY

GMAP_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
WIKI_API_URL = 'https://fr.wikipedia.org/w/api.php'
SEARCH_HEADER = {
    "user-agent": "GrandPy - https://github.com/finevine/Projet7",
    "Origin": "https://grandpy.fr"
    }


def get_place(name):
    search_param = {
        "input": name,
        "inputtype": "textquery",
        "fields": "formatted_address,name,geometry",
        "locationbias": "circle:2000000@47.0359,2.7868",
        "key": GMAP_API_KEY
    }
    req = requests.get(
        GMAP_API_URL,
        params=search_param,
        headers=SEARCH_HEADER
    )
    return req.json()

# print("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=ribecourt&inputtype=textquery&fields=formatted_address,name,geometry&locationbias=circle:2000000@47.0359,2.7868&key=" + MAP_API_KEY)

def get_stories(place_searched):
    URL = "https://fr.wikipedia.org/w/api.php"
    search_param = {
        "action": "parse",
        "page": place_searched,
        "prop": "text",
        "section": "0",
        "format": "json"
    }

    req = requests.get(
        WIKI_API_URL,
        params=search_param,
        headers=SEARCH_HEADER
    )
    DATA = req.json()

    HTML_code = DATA["parse"]["text"]["*"]
    soup = BeautifulSoup(HTML_code, 'html.parser')
    paragraphs = soup.find_all('p', class_=lambda x: x != 'mw-empty-elt')

    sentences = []
    for paragraph in paragraphs[1:]:
        for sentence in paragraph.get_text().split(". "):
            # WORK GREAT WITH PLACE WITHOUT SPECIAL CHAR
            # TO BE REPLACED BY SOMETHING MORE ROBUST
            if len(sentence) >= 250 and place_searched in sentence:
                sentences.append(sentence)

    regex = re.compile(r"\[(.*?)\]", re.IGNORECASE)
    sentences = [regex.sub('', sentence.replace("\xa0", " ")) for sentence in sentences]

    return sentences
