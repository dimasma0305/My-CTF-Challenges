from app import app, cache
from decorator import token_required

from flask import (
    make_response,
    request,
)
from http import HTTPStatus


@app.route("/check", methods=['GET'])
@cache.cached(timeout=5, query_string=True)
@token_required
def check():
    to_read = request.args.get('file')
    if not to_read:
        return make_response(
            "missing file argument",
            HTTPStatus.BAD_REQUEST,
        )
    try:
        file = open(f"feedback/{to_read}", "r")
    except Exception as e:
        return make_response(f"{e}", HTTPStatus.NOT_FOUND)
    res = make_response(
        file.read(),
        HTTPStatus.OK
    )
    res.mimetype = "text/plain"
    file.close()
    return res
