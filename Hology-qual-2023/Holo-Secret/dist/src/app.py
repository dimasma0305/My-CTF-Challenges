from flask import (
    Flask, Response, render_template, request,
)

app = Flask(__name__)
app.static_folder = "public"
app.template_folder = "views"


@app.after_request
def after(res: Response):
    res.headers.add(
        "Content-Security-Policy", "default-src 'none';style-src *;img-src *;"
    )
    return res

@app.get("/")
def flag():
    html = request.args.get("html")
    secret = request.cookies.get("secret")
    return render_template("index.html",
                           html=(html or "<h1>Welcome to Holo Secret!</h1>"),
                           secret=(secret or "secret"))


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
