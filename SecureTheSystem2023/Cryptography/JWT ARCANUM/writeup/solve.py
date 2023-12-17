import httpx
from pwn import xor, urldecode, base64
from multiprocessing import Process

URL = "http://localhost:8306/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url, timeout=99999)

class API(BaseAPI):
    def cook(s, cookie):
        return s.c.get("/", cookies={"jwt_token": cookie})

if __name__ == "__main__":
    api = API()
    cookie = httpx.get(URL).cookies.get("jwt_token")
    header, data, mac = urldecode(cookie).split(".")
    raw_data = base64.b64decode(data)

    # Define three blocks for manipulation: block0, block1 (unknown), block2
    block0 = b'{"role":"guest","secret":"'
    block2 = b'","isLogin":false}'

    # Separate the raw data into three blocks: block0enc, block1enc (unknown), block2enc
    block0enc = raw_data[:len(block0)]
    block1enc = raw_data[len(block0):-len(block2)]
    block2enc = raw_data[len(block1enc + block0):]

    # Define new values for block0 and block2
    block0new = b'{"role":"admin","secret":"'
    block2new = b'","isLogin":"xxx"}'

    # Assert the lengths of the blocks for consistency
    assert(len(block0) == len(block0enc))
    assert(len(block2) == len(block2enc))
    assert(len(block1enc) == (len(raw_data) - len(block0 + block2)))
    assert(len(block0new) == len(block0))
    assert(len(block2new) == len(block2))
    assert(len(block0enc + block1enc + block2enc) == len(raw_data))

    # Tamper with block0 and block2 by XORing with the original and desired plain text
    tampered_block0 = xor(block0enc, block0)
    tampered_block0 = xor(tampered_block0, block0new)
    tampered_block2 = xor(block2enc, block2)
    tampered_block2 = xor(tampered_block2, block2new)

    tampered_data = tampered_block0 + block1enc + tampered_block2

    assert(len(tampered_data) == len(raw_data))

    tampered_data_b64 = base64.b64encode(tampered_data).decode()

    def cook(i):
        cookie = f"{header}.{tampered_data_b64}.{base64.b64encode(chr(i).encode()).decode()}"
        res = api.cook(cookie)
        if "Unauthorized" not in res.text and "Server Error" not in res.text:
            print(res.text)

    for i in range(0, 255):
        p = Process(target=cook, args=(i,))
        p.start()

    p.join()
