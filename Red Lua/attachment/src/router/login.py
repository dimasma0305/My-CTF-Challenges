from flask import (
    request,
    session,
    jsonify,
    make_response,
)
from http import HTTPStatus
from app import app

@app.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    if not form:
        return make_response(
            jsonify(
                message="bad request"
            ),
            HTTPStatus.BAD_REQUEST,
        )
    username = form['username']
    if not username:
        return make_response(
            jsonify(
                message="field username not provided",
            ),
            HTTPStatus.BAD_REQUEST
        )
    session['username'] = username
    return make_response(
        jsonify(
            message="success",
        ),
        HTTPStatus.ACCEPTED,
    )