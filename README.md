# Projet7 : Grandpy, a bot for OpenClassrooms

## Features
 * Interactions are in AJAX: the user sends his question by pressing enter and the answer is displayed directly on the screen, without reloading the page.
 * Google Maps API and the Media Wiki API are used.
 * Nothing is saved. If the user reloads the page again, all history is lost.

Several different answers from GrandPy are coded

## User experience
The user opens its browser and enters the URL provided. After giving his name to customize experience, a page opens containing the following elements:
 * header: logo and catchphrase
 * central area: empty area (which will be used to display the dialog) and form field to send a question.
 * footer: your first & last name, link to your Github repository and other social networks if you have any

The user types *"Salut Grandpy tu connais l'adresse d'OpenClassrooms?"* in the form field and press Enter. The message appears in the top field which displays all messages exchanged. An icon rotates to indicate that GrandPy is thinking.

The bot answer with the address and underneath, a Google Maps appears with a marker indicating the requested address.

The bot then sends a new message with small stories from Wikipedia.

[Kanban of the project](https://github.com/finevine/Projet7/projects/3) is given to see the roadmap.

## Setup
Setup consist in creating a `.env` file in the main folder with this syntax :
```
GMAP_API_KEY=YourApiKeyWithoutQuote 
```

A Pipfile is provided to install all dependencies with this command in root folder :
```
pipenv install
```

## Flask
To test the app in the Project folder:
```
export FLASK_APP=app
python -m flask run
```
Useful ressources about Flask :
- [quick Start](http://flask.palletsprojects.com/en/1.1.x/quickstart/#url-building)
- [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) but no DB is required for this project
- [Jinja 2](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- [lesson OpenClassroom](https://openclassrooms.com/fr/courses/4425066-concevez-un-site-avec-flask)

## TDD
This project is codded using Test Driven Development (tests are written before the main code). Here are 2 videos about testing programs :
- [Rails Conf 2013 The Magic Tricks of Testing](https://youtu.be/URSWYvyc42M)
- [Advanced Test Driven Development](https://vimeo.com/97516288)

To launch the tests use `pytest` command in root folder.

## Deployment
This app is deployed through [Heroku](https://grandpychat.herokuapp.com/)

he Procfile is build as follow: `web: gunicorn run:app`. Procfile specifies the commands that are executed by the app on startup. Here: [WSGI gunicorn is ran](https://docs.gunicorn.org/en/stable/run.html) 
```
gunicorn [OPTIONS] APP_MODULE
```
Where APP_MODULE is of the pattern `$(MODULE_NAME):$(VARIABLE_NAME)` here : `run:app`.