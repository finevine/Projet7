"""
Init app package
"""
import os
from flask import Flask, escape, render_template
from datetime import datetime, date

app = Flask(__name__)

# Get environment variables
GMAP_API_KEY = os.environ.get("GMAP_API_KEY")

@app.route('/')
def index():
    return 'Index Page'

@app.route('/chat')
@app.route('/chat/<username>')
def chat(username=None):
    today = date.today().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%H:%M")
    return render_template('chat.html', name=username, time=now, date=today)

