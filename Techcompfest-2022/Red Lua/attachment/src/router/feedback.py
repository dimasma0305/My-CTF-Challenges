from flask import (
    make_response,
    request,
    render_template,
    jsonify,
)
from http import HTTPStatus
from decorator import register_required
import urllib.request
from app import app

def get_req_data(url: str) -> str:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        content = response.read()
    return content

@app.route("/feedback", methods=["GET", "POST"])
@register_required
def feedback():
    if request.method == "GET":
        return render_template("feedback.html")
    if request.method == "POST":
        form = request.get_json()
        url = form["feedback-url"]
        data = get_req_data(url)
        with open("./feedback/feedback.txt", "w") as f:
            data = ((
                f"{'='*20}\n"
                f"{data}\n"
                f"{'='*20}\n"
            ))
            f.write(data)
        return make_response(
            jsonify(
                message="success",
            ),
            HTTPStatus.ACCEPTED,
        )