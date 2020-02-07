from app import models


class MockGmapResponse():
    '''class to mock Google Map search'''
    def __init__(self, url, headers=None, params=None):
        pass

    @staticmethod
    def json():
        return {
            "status": "OK",
            "candidates": [
                {
                "geometry": {
                    "location":{
                        "lng": 5,
                        "lat": 5
                        }
                },
                "formatted_address": "leboncoin"
                }
                ]
        }

def test_GmapAnswer_attr_OK(monkeypatch):
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockGmapResponse
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr("requests.get", mock_get())

    # app.get_json, which contains requests.get, uses the monkeypatch
    fakeplace = models.GmapAnswer("fakeplace")
    assert fakeplace.lat == 5 \
        and fakeplace.lon == 5 \
            and fakeplace.formatted_address == "leboncoin"


class MockWikiGeoSearchResponse():
    '''class to Mock wikipedia GeoSearch find nearby pages'''
    def __init__(self, url, headers=None, params=None):
        pass

    @staticmethod
    def json():
        return {
                "query": {
                    "geosearch": [
                        {
                            "pageid": 12345,
                            "title": "OK1"
                        },
                        {
                            "pageid": 54321,
                            "title": "OK2"
                        }
                    ]
                }
        }

def test_WikiGeoSearch_attr_OK(monkeypatch):
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockWikiGeoSearchResponse
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr("requests.get", mock_get())

    # app.get_json, which contains requests.get, uses the monkeypatch
    fakePage = models.WikiSearch(1, 2)
    assert fakePage.pageid == 12345 \
        and fakePage.title == "OK1"


class MockWikiSnippetResponse():
    '''class to Mock wikipedia Snippet find'''
    def __init__(self, url, headers=None, params=None):
        pass

    @staticmethod
    def json():
        return {
                "query": {
                    "searchinfo": {
                        "totalhits": 22354
                    },
                    "search": [
                        {
                            "ns": 0,
                            "title": "Versailles",
                            "pageid": 56789,
                            "snippet": "histoire"
                        },
                        {
                            "ns": 0,
                            "title": "Château de Versailles",
                            "pageid": 54321,
                            "snippet": "une autre histoire"
                        }]
                }
        }

def test_WikiSnippet_attr_OK(monkeypatch):
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockWikiSnippetResponse
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr("requests.get", mock_get())

    # app.get_json, which contains requests.get, uses the monkeypatch
    fakePage = models.WikiSnippet("titre", 12345)
    assert fakePage.story == "histoire" and fakePage.accurate == False


