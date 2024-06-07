import re
from collections.abc import Iterator
from itertools import permutations


def solve(content: str) -> Iterator[int]:
    gains = {}
    people = set()
    for a, gain_or_lose, points, b in re.findall(
        r"^(\w+?) would (gain|lose) (\d+) happiness units by sitting next to (\w+).", content, re.MULTILINE
    ):
        if gain_or_lose == "gain":
            gains[(a, b)] = int(points)
        elif gain_or_lose == "lose":
            gains[(a, b)] = -int(points)
        people |= {a, b}

    def score(table: tuple[str, ...]) -> int:
        return sum(gains[(a, b)] + gains[(b, a)] for a, b in zip(table, table[1:] + table[:1]))

    best_table = max(permutations(people), key=score)
    yield (part1 := score(best_table))

    candidates = {gains[(a, b)] + gains[(b, a)]: (a, b) for a, b in zip(best_table, best_table[1:] + best_table[:1])}
    yield part1 - min(candidates)


test_content = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

assert tuple(solve(test_content)) == (330, 286)

with open("13.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
