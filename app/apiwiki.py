"""
    parse.py
    MediaWiki API Demos
    Demo of `Parse` module: Parse content of a page
"""

import requests
import re
from bs4 import BeautifulSoup

place_searched = "Paris"
S = requests.Session()
URL = "https://fr.wikipedia.org/w/api.php"

PARAMS = {
    "action": "parse",
    "page": place_searched,
    "prop": 'text',
    "section": "0",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
print(R.url)
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

print(sentences)

regex = re.compile(r"\[(.*?)\]", re.IGNORECASE)
sentences = [regex.sub('', sentence.replace("\xa0", " ")) for sentence in sentences]

print(sentences)
