from flask import render_template, request, send_file, send_from_directory
from datetime import datetime, date
from io import BytesIO
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
    res = models.AJAX_answer(question)
    if res != "500":
        return res
    else:
        return {
            "formatted_address": "Pétaouchnok",
            "accurate": False,
            "title": "Connais pas",
            "stories": "Non, en fait, je n'ai jamais entendu parlé \
                de cet endroit ! Ça ne me dit rien...",
            "img": {{ url_for('/static/img/None-None.png') }}
        }


# @app.route('/static/img/<float:lat>,<float:lon>.png')
# def map(lat, lon):
#     """Serves the map image."""
#     # image = request to GmapStatic.content
#     print(lat, lon)
#     image = models.GmapStatic(lat, lon).img

#     return send_file(BytesIO(image), mimetype="image/png", \
#         attachment_filename=str(lat) + "," + str(lon) + ".png", \
#         as_attachment=True)


@app.route('/static/img/<string:coords>.png')
def map(coords):
    """Serves the map image.
    ARGS:
        coords(str): lat, lon in a string to cope south hemisphere"""
    try:
        [lat, lon] = coords.split(",")
    except ValueError:
        lat, lon = None, None
    image = models.GmapStatic(lat, lon).img
    if coords == "None,None":
        return send_from_directory('static/img', "None-None.png")
    else:
        return send_file(
            BytesIO(image),
            mimetype="image/png",
            attachment_filename=coords + ".png",
            as_attachment=True)


@app.errorhandler(500)
def internal_error(error):
    return "500"


@app.route('/about')
def about():
    '''
    The canonical URL for the about endpoint does not have a trailing slash.
    It’s similar to the pathname of a file. Accessing the URL
    with a trailing slash produces a 404 “Not Found” error.
    '''
    return 'The about page'
