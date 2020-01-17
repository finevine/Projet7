import requests
import re
import os
import pdb
from unicodedata import normalize
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

GMAP_API_KEY = os.environ["GMAP_API_KEY"]
GMAP_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
WIKI_API_URL = 'https://fr.wikipedia.org/w/api.php'
SEARCH_HEADER = {
    "user-agent": "GrandPy - https://github.com/finevine/Projet7",
    "Origin": "https://grandpy.fr"
    }


#########################
#     WIKIPEDIA         #
#########################

class WikiPage():
    ''' represent the page found or not found '''

    def __init__(self, place):
        '''
        initialize an instance
        Would have been possible with
        https://fr.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=Versailles
        '''
        def get_wikiurl(place_searched):
            URL = "https://fr.wikipedia.org/w/api.php"
            search_param = {
                "action": "query",
                "srsearch": place_searched,
                "list": "search",
                "format": "json"
            }
            # pdb.set_trace()
            # Request :
            req = requests.get(
                WIKI_API_URL,
                params=search_param,
                headers=SEARCH_HEADER
            )
            candidates = req.json()

            # If no index error and unicode title is equal to research
            try:
                normalize('NFC', candidates['query']['search'][0]['title']) == normalize('NFC', place_searched)
                return candidates['query']['search'][0]
            except:
                # Raise Error
                return {
                    "pageid": "None",
                    "title": "None"
                }
        
        self.place = place
        self.pageid = str(get_wikiurl(place).get('pageid'))
        self.url = "https://fr.wikipedia.org/w/index.php?curid=" + self.pageid
        self.title = get_wikiurl(place)['title']

    def stories(self):
        ''' to retrieve stories, we use extension called TextExtract
        https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats
        '''
        URL = "https://fr.wikipedia.org/w/api.php"
        # https://fr.m.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&exsentences=4&titles=Ch%C3%A2teau_de_Versailles
        search_param = {
            "action": "query",
            "titles": self.title,
            "prop": "extracts",
            "explaintext": "true", # get plain text
            "exsentences": "20", # number of sentences to get in the extract
            "format": "json"
        }
        # Request :
        req = requests.get(
            WIKI_API_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )
        Data = req.json()
        print(req.url)

        # replace end line by space and make unicode readable
        sentences = Data["query"]["pages"][self.pageid]["extract"].replace('\n', ' ')
        sentences.encode('utf-8').decode('utf-8')

        res = []
        # Delete Title wikitext part such as "== Présentation générale =="
        regex = re.compile(r"== \b[^==]+==", re.IGNORECASE)
        sentences = regex.sub('', sentences)
        # Check if the place is in the sentence (more than 80 char)
        for sentence in sentences.split(". "):
            if len(sentence) >= 60 and self.place.lower() in sentence.lower():
                res.append(sentence)

        return res



        # text = mwparserfromhell.parse(soup.get_text())
        # sentences = []
        # for sentence in text.split(". "):
        #     if len(sentence) >= 250 and self.place.lower() in sentence.lower():
        #         sentences.append(sentence)
        # return sentences

        ####################
        # paragraphs = soup.find_all('p', class_=lambda x: x != 'mw-empty-elt')
        # pdb.set_trace()
        # sentences = []
        # for paragraph in paragraphs[1:]:
        #     for sentence in mwparserfromhell.parse(paragraph.get_text()).strip_code().split(". "):
        #         if len(sentence) >= 100 and self.place.lower() in sentence.lower():
        #             sentences.append(sentence)
        # # regex = re.compile(r"\[(.*?)\]", re.IGNORECASE)
        # # sentences = [regex.sub('', sentence.replace("\xa0", " ")) for sentence in sentences]
        # return sentences


#########################
#     GMAP              #
#########################

def get_place(name):
            ''' get Wikipedia pages candidates '''
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
