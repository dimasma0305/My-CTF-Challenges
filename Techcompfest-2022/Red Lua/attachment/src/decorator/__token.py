
from functools import wraps
from app import app
from http import HTTPStatus
from flask import (
    request,
    make_response,
    jsonify,
)

WHITE_LIST = [
    "127.0.0.1",
    "172.0.0.1",
    "0.0.0.0",
]

def is_local():
    print(request.remote_addr)
    if request.remote_addr in WHITE_LIST:
        return True
    return False

def has_token():
    if 'x-access-token' in request.headers:
        return True
    return False

def is_token_valid():
    access_token = request.headers.get("x-access-token")
    if access_token == app.secret_key:
        return True
    return False

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if is_local():
            return f(*args, **kwargs)
        if has_token():
            if is_token_valid():
                return f(*args, **kwargs)
            else:
                return make_response(
                    jsonify(
                        message="invalid token",
                    ),
                    HTTPStatus.FORBIDDEN,
                )
        else:
            return make_response(
                jsonify(
                    message="missing token",
                ),
                HTTPStatus.BAD_REQUEST,
            )
    return decorator
