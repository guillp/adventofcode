import hashlib


def md5hash(door_id: str, i: int) -> str:
    return hashlib.md5((door_id + str(i)).encode()).hexdigest()


hash_cache = {}


def part1(door_id: str) -> str:
    p = ""
    i = 0
    while len(p) < 8:
        md5 = md5hash(door_id, i)
        if md5.startswith("00000"):
            p += md5[5]
            # print(p)
            hash_cache[i] = md5
        i += 1

    return p


def get_char(md5: str) -> tuple[int, str]:
    if md5.startswith("00000") and md5[5].isdigit():
        n = int(md5[5])
        if 0 <= n < 8:
            return n, md5[6]
    raise ValueError


def part2(door_id: str) -> str:
    p: list[str | None] = [None] * 8
    for i, md5 in hash_cache.items():
        try:
            n, c = get_char(md5)
            if p[n] is None:
                p[n] = c
        except ValueError:
            pass
    # print("".join(p[n] or "." for n in range(8)))
    while None in p:
        i += 1
        md5 = md5hash(door_id, i)
        try:
            n, c = get_char(md5)
            if p[n] is None:
                p[n] = c
                # print("".join(p[n] or "." for n in range(8)))
        except ValueError:
            pass

    return "".join(p)  # type: ignore[arg-type]


assert part1("abc") == "18f47a30"
assert part2("abc") == "05ace8e3"

content = "cxdnnyjw"
print(part1(content))
print(part2(content))
