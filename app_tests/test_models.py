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
                        "snippet": "Château de Versailles",
                        "timestamp": "2020-01-25T13:59:17Z"
                    },
                    {
                        "ns": 0,
                        "title": "Château de Versailles",
                        "pageid": 57821,
                        "size": 138518,
                        "wordcount": 16211,
                        "snippet": "Le château de Versailles fut la résidence",
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
    fakeplace = models.ApiAnswer("fakeplace")
    fakeplace.get_wikipage()
    assert fakeplace.title == "Versailles" and fakeplace.pageid == 15750
