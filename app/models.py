import requests
import re
import os
from dotenv import load_dotenv
from app import app
from .config import INTENT, STOPWORDS, GMAP_API_URL, GMAP_STATIC_URL, \
    WIKI_API_URL, SEARCH_HEADER, NOT_KNOW
load_dotenv()

GMAP_API_KEY = os.environ["GMAP_API_KEY"]


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
            self.formatted_address = "Pétaouchnok"
        else:
            try:
                best_res = data["candidates"][0]
                self.formatted_address = best_res["formatted_address"]
                location = best_res["geometry"]["location"]
                # accurate = "wikicoord == gmapcoord"
                self.lat, self.lon = location["lat"], location["lng"]
            except KeyError:
                # Output unexpected Exceptions.
                self.formatted_address = "Pétaouchnok"
                self.lat, self.lon = None, None


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

        try:
            places = data["query"]["geosearch"]
            Best_res = places[0]
            self.pageid = Best_res["pageid"]
            self.title = Best_res["title"]
        except KeyError:
            # Output expected IndexErrors.
            pass
        except Exception as error:
            # Output unexpected Exceptions.
            print(error)
            print("il y a eu une erreur !")


class WikiExtract():
    def __init__(self, title, pageid):
        '''Instance of stories found
        uses Wikimedia extension called TextExtract
        https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats
        ARGS:
            title (str): title of wikipedia page
            pageid (int): pageid of wikipedia page
        Attributes:
            accurate (bool): if pageid in results
            stories (str): 2 sentences of story
        '''

        search_param = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": "true",  # get plain text
            "exsentences": "2",  # number of sentences to get in the extract
            "format": "json"
        }
        # Request :
        req = requests.get(
            url=WIKI_API_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )
        data = req.json()

        # replace end line by space and make unicode readable
        try:
            sentences = data["query"]["pages"][str(pageid)]["extract"]
            sentences.encode('utf-8').decode('utf-8')
            self.accurate = True
        except KeyError:
            try:
                page = data["query"]["pages"].popitem()
                sentences = page[0]
                sentences.encode('utf-8').decode('utf-8')
            except KeyError:
                sentences = NOT_KNOW
            self.accurate = False
        except IndexError:
            sentences = NOT_KNOW
            self.accurate = False

        # Delete Title wikitext part such as "== Présentation générale =="
        wikiTitles = re.compile(r"== \b[^==]+==", re.IGNORECASE)
        sentences = wikiTitles.sub('', sentences)

        self.stories = sentences


class GmapStatic():
    '''This class save image of map to a file'''
    def __init__(self, lat, lon):
        '''Instance of a static map
        ARGS:

        ATTR:
            img()'''

        coords = str(lat) + "," + str(lon)
        search_param = {
            "action": "query",
            "center": coords,
            "zoom": "13",
            "size": "300x200",
            "maptype": "roadmap",
            "markers": coords,
            "format": "json",
            "key": GMAP_API_KEY
        }
        # Request :
        req = requests.get(
            url=GMAP_STATIC_URL,
            params=search_param,
            headers=SEARCH_HEADER
        )

        # self.img = io.BytesIO(req.content)
        # import pdb; pdb.set_trace()
        self.img = req.content


class UserQuestion():
    '''This class parse the question to get the good question'''
    def __init__(self, text):
        '''
        Instance of the question extracted
        ARGS:
            text(str): text of the question in natural language
        ATTR:
            place(str): place found with manual NLP'''
        # split into words by white space and isolate punctuation
        words = text.replace('?', ' ?').replace('.', ' .').replace('!', ' !').split()
        # isolate intent
        for intent in INTENT:
            try:
                indexBegin = words.index(intent)
                words = words[indexBegin:]
                break
            except ValueError:
                pass
        try:
            indexEnd = words.index("?")
            question = words[:indexEnd]
        except ValueError:
            question = words

        # remove punctuation from each word
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        table = str.maketrans(punctuation, " " * len(punctuation))
        stripped = [w.translate(table).lower() for w in question]
        # import pdb; pdb.set_trace()
        if stripped:
            sep = " "
            self.place = sep.join([w for w in " ".join(stripped).split() if w not in STOPWORDS])
        else:
            self.place = ""


def AJAX_answer(text):
    '''
    This function returns the json of the instance'''
    intent = UserQuestion(text)
    gmap = GmapAnswer(intent.place)
    address = gmap.formatted_address
    lat, lon = gmap.lat, gmap.lon

    wikiPage = WikiSearch(lat, lon)
    title = wikiPage.title
    pageid = wikiPage.pageid

    wikiStories = WikiExtract(title, pageid)
    accurate = wikiStories.accurate
    stories = wikiStories.stories

    res = {
        "formatted_address": address,
        "accurate": accurate,
        "title": title,
        "stories": stories,
        "lat": lat,
        "lon": lon,
        "img": "/static/img/" + str(lat) + "," + str(lon) + ".png"
    }
    return res


if __name__ == '__main__':
    app.run(debug=True)
