import os
from typing import Any
from flask import Flask, render_template, Response, session
from werkzeug.exceptions import HTTPException
import pydash
from random import randint
from faker import Faker

fake = Faker()


class Books():
    def __init__(self): pass

    def load(self):
        return self.__dict__

    def __setitem__(self, key: str, value: Any) -> None:
        return pydash.set_(self, key, value)

def unserialize(obj: dict[str, Any | str | object]):
    books = Books()
    for book in obj:
        if isinstance(obj[book], str) and obj[book].startswith("!"):
            new_obj_book = obj[book][1::].strip()
            books[book.strip()] = pydash.get(books, new_obj_book)
        else:
            books[book.strip()] = pydash.get(obj, book)
    return books


def serialize(obj: object):
    return obj.__dict__


app = Flask(__name__, static_url_path="/", static_folder="./static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
LIBRARY: dict[bytes, Books] = {}
app.add_template_global(randint)


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return str(e), 500


@app.after_request
def after_request_callback(response: Response):
    if response.status_code >= 500:
        updated = render_template(
            template_name_or_list="template.html",
            status=response.status_code,
            message=response.response[0].decode()
        )
        response.set_data(updated)
    return response


@app.before_request
def before_request_callback():
    if not (session.get("books")):
        books = Books()
        for _ in range(5):
            books[fake.country()] = fake.text()
        session["books"] = serialize(books)


@app.route("/")
def index():
    books = unserialize(session["books"])
    return render_template("index.html", bulletins=books.load())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", debug=True)
