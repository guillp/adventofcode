from collections import defaultdict
from functools import cache

content = """COM)B
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

with open("06.txt") as f: content = f.read()

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


print(sum(orbits(leave) for leave in G))

you_to_com = ("YOU",)
while you_to_com[0] != "COM":
    you_to_com = G[you_to_com[0]], *you_to_com

san_to_com = ("SAN",)
while san_to_com[0] != "COM":
    san_to_com = G[san_to_com[0]], *san_to_com

total_tranfers = len(you_to_com) + len(san_to_com)

for a, b in zip(you_to_com, san_to_com):
    if a == b:
        total_tranfers -= 2

print(total_tranfers - 2)
