
from functools import wraps
from app import app
from http import HTTPStatus
from flask import (
    request,
    make_response,
    redirect,
    session,
)


def register_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = session.get("username")
        if not username:
            return redirect("/")
        return f(*args, **kwargs)
    return decorator
