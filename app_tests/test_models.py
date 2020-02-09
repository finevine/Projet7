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
                        "location": {
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
    assert fakeplace.lat == 5 and fakeplace.lon == 5 \
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


class MockWikiExtractResponse():
    '''class to Mock wikipedia Snippet find'''
    def __init__(self, url, headers=None, params=None):
        pass

    @staticmethod
    def json():
        return {
                "query": {
                    "pages": {
                        "12345": {
                            "pageid": 12345,
                            "title": "titre",
                            "extract": "5 histoires sur le titre"
                        },
                        "54321": {
                            "pageid": 54321,
                            "title": "titre2",
                            "extract": "5 histoires sur le titre2"
                        }
                    }
                }
            }

def test_WikiExtract_attr_OK(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockWikiExtractResponse
    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr("requests.get", mock_get())

    # app.get_json, which contains requests.get, uses the monkeypatch
    fakePage = models.WikiExtract("titre", 12345)
    assert fakePage.stories == "5 histoires sur le titre"


def test_AJAX_answer_OK(monkeypatch):
    class mock_GmapResponse():
        def __init__(self, *args, **kwargs):
            self.formatted_address = "address"
            self.lat = 1234.5
            self.lon = 5432.1

    monkeypatch.setattr('app.models.GmapAnswer', mock_GmapResponse)

    class mock_WikiSearch():
        def __init__(self, *args, **kwargs):
            self.title = "titre"
            self.pageid = 2
            self.lat = 1234.5
            self.lon = 5432.1

    monkeypatch.setattr('app.models.WikiSearch', mock_WikiSearch)

    class mock_WikiExtract():
        def __init__(self, *args, **kwargs):
            self.stories = "Once upon"
            self.accurate = True

    monkeypatch.setattr('app.models.WikiExtract', mock_WikiExtract)

    fakeplace = models.AJAX_answer("fake")
    expected = {
        "formatted_address": "address",
        "accurate": True,
        "title": "titre",
        "stories": "Once upon",
        "lat": 1234.5,
        "lon": 5432.1,
        "img": "/static/img/1234.5,5432.1.png"
    }

    assert fakeplace == expected


def test_UserQuestion_attr_OK():
    question1 = "Bonsoir Grandpy, j'espère que tu as passé une belle semaine. Est-ce que tu pourrais m'indiquer l'adresse de la tour eiffel? Merci d'avance et salutations à Mamie."
    question2 = "Salut grandpy! Comment s'est passé ta soirée avec Grandma hier soir? Au fait, pendant que j'y pense, pourrais-tu m'indiquer où se trouve le musée d'art et d'histoire de Fribourg, s'il te plaît?"
    place1 = models.UserQuestion(question1)
    place2 = models.UserQuestion(question2)
    assert place1.place == "tour eiffel" and place2.place == "musée art histoire fribourg"
