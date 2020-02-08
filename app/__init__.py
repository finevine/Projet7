from flask import Flask

app = Flask(__name__)
app.config["TESTING"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

from . import views