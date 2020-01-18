import requests
import re
import os
import pdb
from unicodedata import normalize
from dotenv import load_dotenv
# from bs4 import BeautifulSoup
load_dotenv()

GMAP_API_KEY = os.environ["GMAP_API_KEY"]
GMAP_API_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
WIKI_API_URL = 'https://fr.wikipedia.org/w/api.php'
SEARCH_HEADER = {
    "user-agent": "GrandPy - https://github.com/finevine/Projet7",
    "Origin": "https://grandpy.fr"
    }


class API_Answer():
    ''' represent the page found or not found '''
    def __init__(self, place):
        '''
        Instance of WikiPage
        ARGS :
            place (str): place to find in Wikipedia'''

        wikiurl = self._get_wikipage(place)
        self.place = place
        self.pageid = str(wikiurl.get("pageid", None))
        self.url = "https://fr.wikipedia.org/w/index.php?curid=" + self.pageid
        self.title = wikiurl['title']
        coord = self.get_coord()
        self.lat = coord["lat"]
        self.lon = coord["lon"]

    #########################
    #     WIKIPEDIA         #
    #########################

    def _get_wikipage(self, place_searched):
        '''
        Search a place on Wikipedia return the page with most authority and fitting best the request
        ARGS:
            place_searched (str): place to find on Wikipedia'''

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
            normalize("NFC", candidates['query']['search'][0]['title']) == normalize('NFC', place_searched)
            return candidates['query']['search'][0]
        except:
            return {
                "pageid": None,
                "title": None
            }
    
    def get_coord(self):
        '''
        Retrieve geolocalization of a place
        uses Wikimedia module called Geosearch
        module is supported through the Extension:GeoData installed on Wikipedia
        https://www.mediawiki.org/wiki/API:Geosearch'''

        URL = "https://fr.wikipedia.org/w/api.php"
        search_param = {
            "action": "query",
            "titles": self.title,
            "prop": "coordinates",
            "format": "json"
        }
        # Set default values to None
        default_dic = {"coordinates":[{'lat': None, 'lon': None}]}
        coordinates = {}

        # Request geoloc if title exist
        if self.title:
            req = requests.get(
                WIKI_API_URL,
                params=search_param,
                headers=SEARCH_HEADER
            )
            Data = req.json()
            # Régler le problème des pages avec title mais pas de coordonnées
            coordinates = Data["query"]["pages"].get(self.pageid, default_dic)["coordinates"][0]
        return {"lat": coordinates.get('lat'), "lon": coordinates.get('lon')}

    def stories(self):
        '''
        Retrieve stories about a place
        uses Wikimedia extension called TextExtract
        https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats
        return:
            list of sentences found about the instance'''
        
        URL = "https://fr.wikipedia.org/w/api.php"
        search_param = {
            "action": "query",
            "titles": self.title,
            "prop": "extracts",
            "explaintext": "true", # get plain text
            "exsentences": "10", # number of sentences to get in the extract
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
        if self.pageid:
            sentences = Data["query"]["pages"][self.pageid]["extract"].replace('\n', ' ')
            sentences.encode('utf-8').decode('utf-8')
        else:
            sentences = ''

        res = []
        # Delete Title wikitext part such as "== Présentation générale =="
        wikiTitles = re.compile(r"== \b[^==]+==", re.IGNORECASE)
        sentences = wikiTitles.sub('', sentences).split(". ")
        # Check if the place is in the sentence (more than 80 char)
        for sentence in sentences:
            if len(sentence) >= 60 and self.place.lower() in sentence.lower():
                res.append(sentence)

        if not res:
            return sentences
        else:
            return res

    #########################
    #     GMAP              #
    #########################

    def find_place(self):
        '''
        find a place on Google Map
        ARGS:
            name (str): place to find on Google Map
        return:
            a json of the request'''

        search_param = {
            "input": self.place,
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

    #########################
    #     MAGIC METHODS     #
    #########################

    def __repr__(self):
        '''
        print an instance'''

        if self.title:
            return self.place + \
                "\ntitle: " + self.title + \
                "\nurl: " + self.url + \
                "\n(lat, lon): (" + str(self.lat) + ", " + str(self.lon) + ")\n"
        else:
            return 'Not found on Wikipedia'