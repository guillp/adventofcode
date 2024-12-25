from itertools import combinations


def solve(content: str) -> int:
    keys_and_locks = {
        frozenset((x, y) for y, line in enumerate(item.splitlines()) for x, c in enumerate(line) if c == "#")
        for item in content.strip().split("\n\n")
    }

    return sum(not (left & right) for left, right in combinations(keys_and_locks, 2))


with open("25.txt") as f:
    content = f.read()

print(solve(content))
