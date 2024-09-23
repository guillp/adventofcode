import re
from collections import defaultdict
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    fabric = defaultdict[tuple[int, int], set[int]](set)

    for claim_id, x, y, w, h in re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", content, re.MULTILINE):
        x_min = int(x)
        x_max = x_min + int(w)
        y_min = int(y)
        y_max = y_min + int(h)

        for c in range(x_min, x_max):
            for r in range(y_min, y_max):
                fabric[c, r].add(claim_id)

    yield sum(len(claims) > 1 for claims in fabric.values())

    all_claims = {claim for claims in fabric.values() for claim in claims}
    for claims in fabric.values():
        if len(claims) > 1:
            all_claims -= claims

    assert len(all_claims) == 1
    yield all_claims.pop()


with open("03.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
