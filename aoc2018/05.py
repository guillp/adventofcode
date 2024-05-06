import string
from itertools import pairwise

test_content = "dabAcCaCBAcCcaDA"


def part1(content: str) -> int:
    d = {i: c for i, c in enumerate(content)}

    while d:
        for i, j in pairwise(d.keys()):
            a = d[i]
            b = d[j]
            if (
                a.islower()
                and b.isupper()
                and a.upper() == b
                or a.isupper()
                and b.islower()
                and a.lower() == b
            ):
                del d[i]
                del d[j]
                break
        else:
            break

    return len(d)


def part2(content: str) -> int:
    def check(letter: str) -> int:
        return part1(content.replace(letter.lower(), "").replace(letter.upper(), ""))

    return min(check(letter) for letter in string.ascii_lowercase)


assert part1(test_content) == 10
assert part2(test_content) == 4


with open("05.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
