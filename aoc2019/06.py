from functools import cache

test_content = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


def solve(content: str) -> tuple[int, int | None]:
    G = {}
    for line in content.splitlines():
        a, b = line.split(")")
        G[b] = a

    assert "COM" not in G

    @cache
    def orbits(leave):
        if leave not in G:
            return 0
        else:
            return 1 + orbits(G[leave])

    part1 = sum(orbits(leave) for leave in G)

    part2 = None
    if "YOU" not in G:
        return part1, part2

    you_to_com = ("YOU",)
    while you_to_com[0] != "COM":
        you_to_com = G[you_to_com[0]], *you_to_com

    san_to_com = ("SAN",)
    while san_to_com[0] != "COM":
        san_to_com = G[san_to_com[0]], *san_to_com

    total_transfers = len(you_to_com) + len(san_to_com)

    for a, b in zip(you_to_com, san_to_com):
        if a == b:
            total_transfers -= 2

    part2 = total_transfers - 2

    return part1, part2


assert solve(test_content) == (42, None)

test_content2 = """COM)B
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
I)SAN"""

assert solve(test_content2) == (54, 4)


with open("06.txt") as f:
    content = f.read()
print(*solve(content), sep="\n")
