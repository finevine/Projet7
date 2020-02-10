from flask import Flask

app = Flask(__name__)
app.config["TESTING"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["UPLOAD_FOLDER"] = ""
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=30)

from . import views