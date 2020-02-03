import requests
import json
from io import BytesIO
from app import models
import pdb

# 
# 
# palais de justice versailles à tester
# 

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
    def __init__(self, api):
        self.api = api

    @staticmethod
    def json():
        if self.api
        return {"ns": 0,
            "title": "Montmartre",
            "pageid": 24951,
            "size": 37462,
            "wordcount": 3566,
            "snippet": "(autrefois Montmartrobus), la seule à circuler sur la butte <span class='searchmatch'>Montmartre</span>. Enfin, le Petit train de <span class='searchmatch'>Montmartre</span> propose également une visite guidée de cette dernière",
            "timestamp": "2020-01-24T09:45:54Z"}



def test__get_wikipage(monkeypatch):
    # Any arguments may be passed: mock_get() will always return a
    # mocked object, which only has the .json() method.
    def mock_get(api, **kwargs):
        return MockWikiResponse(api)
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get(api))

    # app.get_json, which contains requests.get, uses the monkeypatch
    place = models.API_Answer("fakeplace")
    result = place._get_wikipage()
    assert result["title"] == "Montmartre" and result["pageid"] == 24951


# class MockWikiResponse:
#     @staticmethod
#     def json():
#         with open("tests/Versailles.json", "r") as json_file:
#             res = json.dumps(json_file)
#         res.replace('"', '\\"')
#         res.replace("'", '"')
#         return res


# def test_get_clean_stories(monkeypatch):
#     # Any arguments may be passed: mock_get() will always return a
#     # mocked object, which only has the .json() method.
#     def mock_get(*args, **kwargs):
#         return MockWikiResponse()
#     # apply the monkeypatch for requests.get to mock_get
#     monkeypatch.setattr(requests, "get", mock_get)

#     # app.get_json, which contains requests.get, uses the monkeypatch
#     result = models.get_clean_stories("Versailles")
#     assert result == ['Située dans la banlieue ouest de la capitale française, à 17,1 km du centre de Paris, Versailles est au XXIe siècle une ville résidentielle aisée avec une économie principalement tertiaire et constitue une destination touristique internationale de premier plan']

