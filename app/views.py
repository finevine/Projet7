from flask import render_template, request
from datetime import datetime, date
from app import models
from . import app


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/chat')
def chat(username=None):
    '''
    path to chat'''
    username = request.args.get('user')
    today = date.today().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%H:%M")
    return render_template('chat.html', name=username, time=now, date=today)


@app.route('/answer')
def requete_AJAX():
    '''
    AJAX request calls this function.'''
    question = request.args.get('question')
    return models.AJAX_answer(question)


@app.route('/about')
def about():
    '''
    The canonical URL for the about endpoint does not have a trailing slash.
    It’s similar to the pathname of a file. Accessing the URL
    with a trailing slash produces a 404 “Not Found” error.
    '''
    return 'The about page'
