import hashlib
from functools import cache


@cache
def md5hash(door_id: str, i: int) -> str:
    return hashlib.md5((door_id + str(i)).encode()).hexdigest()


def part1(door_id: str) -> str:
    p = ""
    i = 0
    while len(p) < 8:
        md5 = md5hash(door_id, i)
        if md5.startswith("00000"):
            p += md5[5]
        i += 1

    return p


def part2(door_id: str) -> str:
    p: list[str | None] = [None] * 8
    i = 0
    while None in p:
        md5 = md5hash(door_id, i)
        if md5.startswith("00000") and md5[5].isdigit():
            n = int(md5[5])
            if 0 <= n < 8 and p[n] is None:
                c = md5[6]
                p[n] = c
        i += 1
    return "".join(p)  # type: ignore[arg-type]


assert part1("abc") == "18f47a30"
assert part2("abc") == "05ace8e3"

content = "cxdnnyjw"
print(part1(content))
print(part2(content))
