import hashlib
from functools import cache
from heapq import heappush, heappop

test_content = "hijkl"
content = "qtetzkpl"

@cache
def hash(passwd: str, path: str) -> str:
    directions = tuple(
        c in "bcdef" for c in hashlib.md5((passwd + path).encode()).hexdigest()[:4]
    )
    return "".join(l for d, l in zip(directions, "UDLR") if d)


def part1(passwd: str) -> str:
    pool = []
    heappush(pool, (0, "", (0, 0)))
    best = -500
    best_path = None
    while pool:
        l, path, (x, y) = heappop(pool)
        if l < best:
            continue

        for d in hash(passwd, path):
            nx, ny = {
                "D": (x, y + 1),
                "R": (x + 1, y),
                "L": (x - 1, y),
                "U": (x, y - 1),
            }[d]
            if nx < 0 or nx > 3 or ny < 0 or ny > 3:
                continue
            if nx == ny == 3:
                if -len(path) - 1 > best:
                    best = - len(path) + 1
                    best_path = path+d
            else:
                heappush(pool, (l + 1, path + d, (nx, ny)))

    return best_path


assert hash("hijkl", "") == "UDL"
assert hash("hijkl", "D") == "ULR"
assert hash("hijkl", "DR") == ""

assert part1("ihgpwlah") == "DDRRRD"

print(part1(content))

@cache
def part2(passwd: str) -> str:
    pool = {(0, "", (0,0))}
    best = 0
    while pool:
        l, path, (x,y) = pool.pop()
        for d in hash(passwd, path):
            nx, ny = {
                "D": (x, y + 1),
                "R": (x + 1, y),
                "L": (x - 1, y),
                "U": (x, y - 1),
            }[d]
            if nx < 0 or nx > 3 or ny < 0 or ny > 3:
                continue
            if nx == ny == 3:
                if len(path) +1 > best:
                    best = len(path) + 1
            else:
                pool.add((l+1, path+d, (nx,ny)))

    return best


assert part2("ihgpwlah") == 370
print(part2(content))