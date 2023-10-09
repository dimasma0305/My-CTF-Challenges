from app import app, cache
from flask import (
    render_template
)


@app.route('/', methods=['GET'])
@cache.cached(timeout=5)
def index():
    return render_template("index.html")
