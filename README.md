# NOTA :
Le mock de classe est intéressant :

```python
def test_get_wikipage(monkeypatch):
    class mock_API_Answer():
        def __init__(self, *args, **kwargs):
            self.place = "Versailles"
            self.pageid = 12345
            self.url = 'https://fr.wikipedia.org/w/index.php?curid='+str(self.pageid)
            self.title = "Versailles"
            self.lat, self.lon = 0, 0
            self.accurate = False
            self.formatted_address = "addresse de Versailles"
            self.stories = ["il était une fois à Versailles", "dans les rues de Versailles, un jour..."]
            self.json = {
                "formatted_address": self.formatted_address,
                "accurate": self.accurate,
                "title": self.title,
                "stories": self.stories
            }

        def get_wikipage(self):
            self.place = "toto"

    monkeypatch.setattr('app.models.API_Answer', mock_API_Answer)

    fakeplace = app.models.API_Answer("fake")

    assert fakeplace.place == "toto"
```

# Projet7 : Grandpy bot a bot for OpenClassrooms
[Assignement](https://openclassrooms.com/fr/projects/158/assignment) is online.

[Kanban of the project](https://github.com/finevine/Projet7/projects/3) is given to see the roadmap.

## Setup
Setup consist in creating a `.env` file in the main folder with this syntax :
```
GMAP_API_KEY=YourApiKeyWithoutQuote
```

## TDD
This project is codded using Test Driven Development. Here are 2 videos about testing programs :
- [Rails Conf 2013 The Magic Tricks of Testing](https://youtu.be/URSWYvyc42M)
- [Advanced Test Driven Development](https://vimeo.com/97516288)

## Flask
To test the app in the Project folder:
```
export FLASK_APP=app/views.py
python -m flask run
```
Useful ressources about Flask :
- [quick Start](http://flask.palletsprojects.com/en/1.1.x/quickstart/#url-building)
- [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) but no DB is required for this project
- [Jinja 2](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- [lesson OpenClassroom](https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask)
