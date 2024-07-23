from collections.abc import Iterator
from functools import cache


def solve(content: str) -> Iterator[int]:
    G: dict[str, str] = {}
    for line in content.splitlines():
        a, b = line.split(")")
        G[b] = a

    assert "COM" not in G

    @cache
    def orbits(leave: str) -> int:
        if leave not in G:
            return 0
        else:
            return 1 + orbits(G[leave])

    yield sum(orbits(leave) for leave in G)

    if "YOU" not in G:
        return

    you_to_com: tuple[str, ...] = ("YOU",)
    while you_to_com[0] != "COM":
        you_to_com = G[you_to_com[0]], *you_to_com

    san_to_com: tuple[str, ...] = ("SAN",)
    while san_to_com[0] != "COM":
        san_to_com = G[san_to_com[0]], *san_to_com

    total_transfers = len(you_to_com) + len(san_to_com)

    for a, b in zip(you_to_com, san_to_com):
        if a == b:
            total_transfers -= 2

    yield total_transfers - 2


assert (
    next(
        solve("""\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""")
    )
    == 42
)


assert tuple(
    solve("""\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""")
) == (54, 4)


with open("06.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
