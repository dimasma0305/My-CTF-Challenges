#!/usr/bin/env python3
import pydash


class Books():
    def __init__(self): pass

    def load(self):
        return self.__dict__

    def __setitem__(self, key: str, value) -> None:
        return pydash.set_(self, key, value)



if __name__ == "__main__":
    obj = Books()
    while True:
        src = input("src: ")
        dst = input("dst: ")
        pydash.set_(obj, dst, pydash.get(obj, src))
