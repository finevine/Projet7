import requests
import re
import os
import pdb
from unicodedata import normalize
from dotenv import load_dotenv
# from bs4 import BeautifulSoup
load_dotenv()

GMAP_API_KEY = os.environ["GMAP_API_KEY"]
GMAP_API_URL = \
    'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
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
            place (str): place to find in Wikipedia
        return:
            place (str)
            pageid (str) : wikipedia page ID
            url (str) : URL of wikipedia
            title (str) : wikipedia title
            formatted_address (str) : Google Map address
            stories (list) : stories parsed from wikipedia
            accurate (bool) : if stories match to coordinates
            lat (float)
            lon (float)'''

        # Get wikipage attributes
        wikiPageJson = self._get_wikipage(place)
        self.place = place
        self.pageid = wikiPageJson.get("pageid", None)
        self.url = "https://fr.wikipedia.org/w/index.php?curid=" \
            + str(self.pageid)
        self.title = wikiPageJson['title']

        # Get wiki coordinates
        self.lat, self.lon = None, None
        self.accurate = False
        self.get_wikicoord()

        # Get address on Google MAP and if necessary get coord
        self.formatted_address = ""
        self.get_gmapaddress()

        # Get stories to tell
        self.stories = []
        self.stories = self.get_wikistories()

        # print(wikiurl)
        # print(self.url, self.title, sep="\n")

    #########################
    #     WIKIPEDIA         #
    #########################

    def _get_wikipage(self, place_searched):
        '''
        Search a place on Wikipedia return the json page
        with most authority and fitting best the request.
        ARGS:
            place_searched (str): place to find on Wikipedia
        return:
            (dic): first result of wikipedia if pagetitle = place_searched
                    {"pageid": None,"title": None} otherwise'''

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
            normalize("NFC", candidates['query']['search'][0]['title']) \
                == normalize('NFC', place_searched)
            return candidates['query']['search'][0]
        except:
            return {
                "pageid": None,
                "title": None
            }

    def get_wikicoord(self):
        '''
        Retrieve geolocalization of a place
        uses Wikimedia module called Geosearch
        module is supported through the Extension:GeoData
        installed on Wikipedia
        https://www.mediawiki.org/wiki/API:Geosearch
        return:
            (dic) if found on Wikipedia, "lat", "lon"'''

        search_param = {
            "action": "query",
            "titles": self.title,
            "prop": "coordinates",
            "format": "json"
        }
        # Set default values to None
        default_list = [{'lat': 0, 'lon': 0}]
        default_dic = {"coordinates": [{'lat': 0, 'lon': 0}]}
        coordinates = {}

        # Request geoloc if title and coodinates exist
        if self.title:
            req = requests.get(
                WIKI_API_URL,
                params=search_param,
                headers=SEARCH_HEADER
            )
            Data = req.json()
            coordinates = Data["query"]["pages"].get(
                str(self.pageid), default_dic)\
                .get(
                    "coordinates", default_list
                    )[0]

        self.lat = coordinates.get('lat')
        self.lon = coordinates.get('lon')
        # print("wikilat = " + str(self.lat))

    def get_wikistories(self):
        '''
        Retrieve stories about a place
        uses Wikimedia extension called TextExtract
        https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats
        return:
            list of sentences found about the instance'''

        search_param = {
            "action": "query",
            "titles": self.title,
            "prop": "extracts",
            "explaintext": "true",  # get plain text
            "exsentences": "5",  # number of sentences to get in the extract
            "format": "json"
        }
        # Request :
        req = requests.get(
            WIKI_API_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )
        Data = req.json()

        # replace end line by space and make unicode readable
        if self.pageid:
            sentences = Data["query"]["pages"][str(self.pageid)]["extract"]\
                .replace('\n', ' ')
            sentences.encode('utf-8').decode('utf-8')
        else:
            sentences = ''

        res = []
        # Delete Title wikitext part such as "== Présentation générale =="
        wikiTitles = re.compile(r"== \b[^==]+==", re.IGNORECASE)
        sentences = wikiTitles.sub('', sentences).split(". ")
        # Check if the place is in the sentence (more than XX char)
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

    def get_gmapaddress(self):
        '''
        find a place on Google Map
        ARGS:
            name (str): place to find on Google Map
        return:
            json of the request'''

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

        Data = req.json()
        if Data["status"] != "OK":
            pass
        else:
            Best_res = Data["candidates"][0]
            self.formatted_address = Best_res["formatted_address"]
            location = Best_res["geometry"]["location"]
            # accurate = "wikicoord == gmapcoord"
            self.accurate = round(self.lat, 3) == round(location["lat"], 3) \
                and round(self.lon, 3) == round(location["lng"], 3)
            self.lat, self.lon = location["lat"], location["lng"]
            # print("googlelat = " + str(self.lat))

    #########################
    #     MAGIC METHODS     #
    #########################

    def __repr__(self):
        '''
        print an instance'''

        stories = ''
        for story in self.stories:
            stories += story + ", "
        if self.title or self.formatted_address:
            return self.place + \
                "\ntitle: " + self.title + \
                "\nurl: " + self.url + \
                "\n(lat, lon): (" + str(self.lat) + \
                ", " + str(self.lon) + ")" + \
                "\nadresse: " + self.formatted_address + \
                "\nprécis: " + str(self.accurate) + \
                "\nhistoires: " + stories + "\n"

        else:
            return 'Not found'

def AJAX_answer(question):
    answer = API_Answer(question)
    return answer