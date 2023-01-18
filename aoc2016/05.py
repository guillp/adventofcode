import hashlib

# content = "abc"
content = "cxdnnyjw"


def hash(door_id: str, i: int) -> str:
    return hashlib.md5((door_id + str(i)).encode()).hexdigest()


hash_cache = {}


def password(door_id: str) -> str:
    p = ""
    i = 0
    while len(p) < 8:
        md5 = hash(door_id, i)
        if md5.startswith("00000"):
            p += md5[5]
            print(p)
            hash_cache[i] = md5
        i += 1

    return p


print(password(content))


def get_char(md5: str) -> tuple[int, str]:
    if md5.startswith("00000"):
        if md5[5].isdigit():
            n = int(md5[5])
            if 0 <= n < 8:
                return n, md5[6]
    raise ValueError()


def password2(door_id: str) -> str:
    p = [None] * 8
    for i, md5 in hash_cache.items():
        try:
            n, c = get_char(md5)
            if p[n] is None:
                p[n] = c
        except ValueError:
            pass
    print("".join(p[n] or "." for n in range(8)))
    while None in p:
        i += 1
        md5 = hash(door_id, i)
        try:
            n, c = get_char(md5)
            if p[n] is None:
                p[n] = c
                print("".join(p[n] or "." for n in range(8)))
        except ValueError:
            pass

    return "".join(p)


print(password2(content))
