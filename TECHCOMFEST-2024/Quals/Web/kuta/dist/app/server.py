from flask import Flask, request, render_template
import subprocess


class HTTPException(Exception):
    def __init__(self, status, text, *args: object) -> None:
        self.status = status
        self.message = text
        super().__init__(*args)


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return render_template("template.html", status=e.status, message=str(e.message))
    return render_template("template.html", status=500, message=str(e))


@app.post("/")
def index_post():
    url = request.form.get("url")
    if not url:
        raise HTTPException(400, "url not found")
    try:
        subprocess.run(["qutebrowser", "-T", "-s", "url.start_pages", "data:text/plain,", url], timeout=30, cwd="/tmp")
    except Exception as e:
        raise HTTPException(500, e)


@app.get("/")
def index_get():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
