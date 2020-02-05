import requests
import json
import pytest
from app import models

class MockWikiResponse():
    def __init__(self, url, headers=None, params=None):
        pass

    @staticmethod
    def json():
        return {
            "batchcomplete": "",
            "continue": {
                "sroffset": 10,
                "continue": "-||"
            },
            "query": {
                "searchinfo": {
                    "totalhits": 22344
                },
                "search": [
                    {
                        "ns": 0,
                        "title": "Versailles",
                        "pageid": 15750,
                        "size": 155885,
                        "wordcount": 18498,
                        "snippet": "Château de <span class=\"searchmatch\">Versailles</span> et <span class=\"searchmatch\">Versailles</span> (homonymie). « Versaillais » redirige ici. Pour les autres significations, voir Versaillais (homonymie). <span class=\"searchmatch\">Versailles</span> (/vɛʁ",
                        "timestamp": "2020-01-25T13:59:17Z"
                    },
                    {
                        "ns": 0,
                        "title": "Château de Versailles",
                        "pageid": 57821,
                        "size": 138518,
                        "wordcount": 16211,
                        "snippet": "Le château de <span class=\"searchmatch\">Versailles</span> est un château et un monument historique français qui se situe à <span class=\"searchmatch\">Versailles</span>, dans les Yvelines, en France. Il fut la résidence",
                        "timestamp": "2020-01-28T11:47:55Z"
                    }
                ]
            }
        }

def test_get_wikipage(monkeypatch):
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockWikiResponse
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr("requests.get", mock_get())

    # app.get_json, which contains requests.get, uses the monkeypatch
    fakeplace = models.API_Answer("fakeplace")
    fakeplace.get_wikipage()
    assert fakeplace.title == "Versailles" and fakeplace.pageid == 15750




# WORK OK TO MOCK AN INSTANCE
# def test_get_wikipage_uses_API_OK(monkeypatch):
#     class mock_API_Answer():
#         def __init__(self, *args, **kwargs):
#             self.place = "Versailles"
#             self.pageid = 12345
#             self.url = 'https://fr.wikipedia.org/w/index.php?curid='+str(self.pageid)
#             self.title = "Versailles"
#             self.lat, self.lon = 0, 0
#             self.accurate = False
#             self.formatted_address = "addresse de Versailles"
#             self.stories = ["il était une fois à Versailles", "dans les rues de Versailles, un jour..."]
#             self.json = {
#                 "formatted_address": self.formatted_address,
#                 "accurate": self.accurate,
#                 "title": self.title,
#                 "stories": self.stories
#             }

#         def get_wikipage(self):
#             self.place = "toto"

#     monkeypatch.setattr('app.models.API_Answer', mock_API_Answer)

#     fakeplace = app.models.API_Answer("fake")

#     assert fakeplace.place == "toto"


