import requests
import json
import os
from io import BytesIO
from app import api_call


class MockGmapResponse:
    @staticmethod
    def json():
        return {
                "candidates" : [
                    {
                        "formatted_address" : "Place d'Armes, 78000 Versailles, France",
                        "name" : "Château de Versailles"
                    }
                ],
                "status" : "OK"
                }


def test_get_place(monkeypatch):
    # Any arguments may be passed: mock_get() will always return a
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockGmapResponse()
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    place = api_call.Answer("fakeplace")
    result = place.find_place()
    assert result["candidates"][0]["formatted_address"] == "Place d'Armes, 78000 Versailles, France"


class MockWikiResponse:
    @staticmethod
    def json():
        with open("tests/Versailles.json", "r") as json_file:
            res = json.dumps(json_file)     
        res.replace('"', '\\"')
        res.replace("'", '"')
        return res


def test_get_clean_stories(monkeypatch):
    # Any arguments may be passed: mock_get() will always return a
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockWikiResponse()
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = api_call.get_clean_stories("Versailles")
    assert result == ['Située dans la banlieue ouest de la capitale française, à 17,1 km du centre de Paris, Versailles est au XXIe siècle une ville résidentielle aisée avec une économie principalement tertiaire et constitue une destination touristique internationale de premier plan']

# def test_gmap_return_none():
#     return {"candidates" : [],
#             "status" : "ZERO_RESULTS"}

# def test_gmap_return_multiple():
#     results = {
#             "candidates" : [
#                 {
#                     "formatted_address" : "22940 Saint-Julien, France",
#                     "name" : "Saint-Julien"
#                 },
#                 {
#                     "formatted_address" : "69640 Saint-Julien, France",
#                     "name" : "Saint-Julien"
#                 },
#                 {
#                     "formatted_address" : "74160 Saint-Julien-en-Genevois, France",
#                     "name" : "Saint-Julien-en-Genevois"
#                 }
#             ],
#             "status" : "OK"
#             }
#     return results