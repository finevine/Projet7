import requests
import json
import pytest
from app import models

class MockAPIResponse:
    @staticmethod
    def json():
        return {
            "accurate":true,
            "formatted_address":"Montmartre, 75018 Paris, France",
            "stories":[
                "Jusqu'en 1860, Montmartre \u00e9tait une commune du d\u00e9partement de la Seine",
                "Le territoire restant de l'ancien Montmartre, aujourd'hui un lieu-dit sans r\u00e9alit\u00e9 officielle ni d\u00e9limitation g\u00e9ographique particuli\u00e8re, est alors int\u00e9gr\u00e9 dans ce qui devient le 18e arrondissement de Paris, baptis\u00e9 \u00ab des Buttes-Montmartre \u00bb et constitu\u00e9 des quartiers administratifs des Grandes-Carri\u00e8res, de Clignancourt, de la Goutte-d'Or et de la Chapelle",
                " Connu pour ses rues \u00e9troites et escarp\u00e9es flanqu\u00e9es d'escaliers interminables et pour son ambiance de village, ce secteur tr\u00e8s touristique du nord de Paris abrite le point culminant de la capitale sur la butte Montmartre, une des buttes-t\u00e9moins gypseuses form\u00e9es de part et d'autre de la Seine et d\u00e9nomm\u00e9es les \u00ab collines de Paris \u00bb."
            ],
            "title":"Montmartre"
            }

class MockWikiResponse:
    @staticmethod
    def json():
        return {
                "ns": 0,
                "title": "Versailles",
                "pageid": 15750,
                "size": 155885,
                "wordcount": 18498,
                "snippet": "Château de <span class=\"searchmatch\">Versailles</span> et <span class=\"searchmatch\">Versailles</span> (homonymie). « Versaillais » redirige ici. Pour les autres significations, voir Versaillais (homonymie). <span class=\"searchmatch\">Versailles</span> (/vɛʁ",
                "timestamp": "2020-01-25T13:59:17Z"
            }


pytest.fixture(scope="class")
def monkeypatch_for_class(request):
    request.cls.monkeypatch = MonkeyPatch()

@pytest.mark.usefixtures("monkeypatch_for_class")
class test_API_Answer(models.API_Answer):
    def __init__(self):
        models.API_Answer.__init__(self)
    
    def test_classmethod(self):
        self.monkeypatch.setattr('get_gmapaddress', lambda: 1)


# def test_get_wikipage(monkeypatch):
#     # mocked object, which only has the .json() method.
#     def mock_get(*args, **kwargs):
#         return MockWikiResponse
#     # apply the monkeypatch for requests.get to mock_get
#     monkeypatch.setattr(requests, "get", mock_get())
#     monkeypatch.setattr('test_API_Answer.get_wikicoord', staticmethod(lambda: 1))
#     monkeypatch.setattr('API_answer().get_gmapaddress', lambda: 1)
#     monkeypatch.setattr('API_answer().get_wikistories', lambda: 1)


#     # app.get_json, which contains requests.get, uses the monkeypatch
#     # place = models.API_Answer("fakeplace")
#     fakeplace = API_answer("fake place")
#     result = fakeplace.get_wikipage()
#     assert result["title"] == "Versailles" and result["pageid"] == 15750

# @pytest.fixture
# class API_answer():
#     """mock the instance creation"""
#     def __init__(self):
#         self.place = "Versailles"
#         self.pageid = 12345
#         self.url = 'https://fr.wikipedia.org/w/index.php?curid='+str(self.pageid)
#         self.title = "Versailles"
#         self.lat, self.lon = 0, 0
#         self.accurate = False
#         self.formatted_address = "addresse de Versailles"
#         self.stories = ["il était une fois à Versailles", "dans les rues de Versailles, un jour..."]
#         self.json = {
#             "formatted_address": self.formatted_address,
#             "accurate": self.accurate,
#             "title": self.title,
#             "stories": self.stories
#         }