from flask import Flask, escape, render_template
from datetime import datetime, date
from app import models
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/chat')
@app.route('/chat/<username>')
def chat(username=None):
    '''
    path to chat'''
    today = date.today().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%H:%M")
    return render_template('chat.html', name=username, time=now, date=today)

@app.route('/answer/<string:question>')
def requete_AJAX(question):
    '''
    AJAX request calls this function.'''
    return models.AJAX_answer(question).formatted_address

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

@app.route('/projects/')
def projects():
    '''
    The canonical URL for the projects endpoint has a trailing slash. It’s similar to a folder in a file system. If you access the URL without a trailing slash, Flask redirects you to the canonical URL with the trailing slash.
    '''
    return 'The project page'

@app.route('/about')
def about():
    '''
    The canonical URL for the about endpoint does not have a trailing slash. It’s similar to the pathname of a file. Accessing the URL with a trailing slash produces a 404 “Not Found” error.
    '''
    return 'The about page'