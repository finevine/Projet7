import requests
import re
import os
from dotenv import load_dotenv
from app import app
load_dotenv()

GMAP_API_KEY = os.environ["GMAP_API_KEY"]
GMAP_API_URL = \
    'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
GMAP_STATIC_URL = \
    'http://maps.googleapis.com/maps/api/staticmap?'
WIKI_API_URL = 'https://fr.wikipedia.org/w/api.php'
SEARCH_HEADER = {
    "user-agent": "GrandPy - https://github.com/finevine/Projet7",
    "Origin": "https://grandpy.fr"
    }


class GmapAnswer():
    '''find place in google map'''
    def __init__(self, place):
        '''Instance of place to find
        ARGS:
            place (str): place to find 
        Attributes:
            formatted_address (str): Google Map address
            lat (float): latitude
            lon (float): longitude
        '''
        self.lat = None
        self.lon = None
        self.formatted_address = None
        PARAMS = {
            "input": place,
            "inputtype": "textquery",
            "fields": "formatted_address,name,geometry",
            "locationbias": "circle:2000000@47.0359,2.7868",
            "key": GMAP_API_KEY
        }
        req = requests.get(
            GMAP_API_URL,
            params=PARAMS,
            headers=SEARCH_HEADER
        )

        data = req.json()
        if data["status"] != "OK":
            pass
        else:
            try:
                best_res = data["candidates"][0]
                self.formatted_address = best_res["formatted_address"]
                location = best_res["geometry"]["location"]
                # accurate = "wikicoord == gmapcoord"
                self.lat, self.lon = location["lat"], location["lng"]
            except KeyError as error:
                # Output expected IndexErrors.
                pass
            except Exception as error:
                # Output unexpected Exceptions.
                print(error)
                print("il y a eu une erreur !")


class WikiSearch():
    '''class to find nearby pages in wikipedia'''
    def __init__(self, lat, lon):
        '''Instance of page found
        ARGS:
            lat (float): latitude
            lon (float): longitude
        Attributes:
            lat (float): latitude
            lon (float): longitude
            pageid (int): wikipedia pageid
            title (str): title of wikipedia page
        '''
        self.lat = lat
        self.lon = lon
        self.pageid = None
        self.title = None
        PARAMS = {
            "format": "json",
            "list": "geosearch",
            "gscoord": str(lat)+"|"+str(lon),
            "gslimit": "10",
            "gsradius": "10000",
            "action": "query"
        }
        req = requests.get(
            url=WIKI_API_URL,
            params=PARAMS,
            headers=SEARCH_HEADER
        )
        data = req.json()

        places = data["query"]["geosearch"]
        try:
            Best_res = places[0]
            self.pageid = Best_res["pageid"]
            self.title = Best_res["title"]
        except KeyError as error:
            # Output expected IndexErrors.
            pass
        except Exception as error:
            # Output unexpected Exceptions.
            print(error)
            print("il y a eu une erreur !")


class WikiSnippet():
    '''class that get snippet from wikipedia'''
    def __init__(self, title, pageid):
        '''Instance of stories to find
        ARGS:
            title (str): title of wikipedia page
            pageid (int): wikipedia pageid
        Attributes:
            story (str): Snippet from wikipedia
            accurate (bool): if pageid and title are coherents
        '''
        self.story = None
        self.accurate = False
        PARAMS = {
            "action": "query",
            "srsearch": title,
            "list": "search",
            "format": "json"
        }
        # Request :
        req = requests.get(
            url=WIKI_API_URL,
            params=PARAMS,
            headers=SEARCH_HEADER
        )
        candidates = req.json()
        wikiPage = candidates["query"]["search"][0]
        self.story = wikiPage["snippet"]
        self.accurate = wikiPage["pageid"] == pageid

# TO DELETE
class ApiAnswer():
    ''' represent the page found or not found '''
    def __init__(self, place):
        '''
        Instance of WikiPage
        ARGS :
            place (str): place to find in Wikipedia
        Attributes:
            place (str)
            pageid (str) : wikipedia page ID
            url (str) : URL of wikipedia
            title (str) : wikipedia title
            formatted_address (str) : Google Map address
            stories (list) : stories parsed from wikipedia
            accurate (bool) : if stories match to coordinates
            lat (float)
            lon (float)
            json (json) : formatted_address, accurate, title, stories'''

        # initialize wikipage attributes
        self.place = place
        self.pageid = 0
        self.url = ""
        self.title = ""

        # initialize wiki coordinates
        self.lat, self.lon = 0, 0
        self.accurate = False

        # define self.formatted_address :
        self.formatted_address = ""

        # define self.stories :
        self.stories = []

    @property
    def json(self):
        return {
            "formatted_address": self.formatted_address,
            "accurate": self.accurate,
            "title": self.title,
            "stories": self.stories
        }

    #########################
    #     WIKIPEDIA         #
    #########################

    def get_wikipage(self):
        '''
        Search a place on Wikipedia return the json page
        with most authority and fitting best the request.
        return:
            (dic): first result of wikipedia if pagetitle = place
                    {"pageid": None,"title": None} otherwise'''

        search_param = {
            "action": "query",
            "srsearch": self.place,
            "list": "search",
            "format": "json"
        }
        # Request :
        req = requests.get(
            WIKI_API_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )
        candidates = req.json()

        wikiPageJson = candidates['query']['search'][0]
        self.pageid = wikiPageJson.get("pageid", None)
        self.url = "https://fr.wikipedia.org/w/index.php?curid=" \
            + str(self.pageid)
        self.title = wikiPageJson['title']

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
            data = req.json()
            coordinates = data["query"]["pages"].get(
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
        data = req.json()

        # replace end line by space and make unicode readable
        if self.pageid:
            sentences = data["query"]["pages"][str(self.pageid)]["extract"]\
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
            self.stories = sentences
        else:
            self.stories = res

    #########################
    #     GMAP              #
    #########################

    def get_gmapMap(self):

        search_param = {
            "center": str(self.lat) + "," + str(self.lon),
            "zoom": 13,
            "size": "300x200",
            "maptype": "roadmap",
            "markers": "size:mid|color:red|" + str(self.lat) + "," + str(self.lon),
            "key": GMAP_API_KEY
        }
        req = requests.get(
            GMAP_STATIC_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )

        Photo_URL = req.url
        import pdb; pdb.set_trace()

        Picture_request = requests.get(Photo_URL)
        if Picture_request.status_code == 200:
            with open("/path/to/image.jpg", 'wb') as f:
                f.write(Picture_request.content)

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

        data = req.json()
        if data["status"] != "OK":
            pass
        else:
            Best_res = data["candidates"][0]
            self.formatted_address = Best_res["formatted_address"]
            location = Best_res["geometry"]["location"]
            # accurate = "wikicoord == gmapcoord"
            self.lat, self.lon = location["lat"], location["lng"]
            self.accurate = round(self.lat, 3) == round(location["lat"], 3) \
                and round(self.lon, 3) == round(location["lng"], 3)
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

# class UserQuestion():


def AJAX_answer(place):
    '''
    This function returns the json of the instance'''
    gmap = GmapAnswer(place)
    address = gmap.formatted_address
    lat, lon = gmap.lat, gmap.lon

    wikiPage = WikiSearch(lat, lon)
    title = wikiPage.title
    pageid = wikiPage.pageid

    wikiStory = WikiSnippet(title, pageid)
    accurate = wikiStory.accurate
    story = wikiStory.story

    res = {
        "formatted_address": address,
        "accurate": accurate,
        "title": title,
        "story": story
    }
    return res


if __name__ == '__main__':
    app.run(debug=True)
