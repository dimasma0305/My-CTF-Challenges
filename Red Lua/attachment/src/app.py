from flask import (
    Flask,
)
from flask_session import Session
from flask_caching import Cache


app = Flask(__name__)
app.config.from_object("config.Config")
cache = Cache(app)
server_session = Session(app)

import router