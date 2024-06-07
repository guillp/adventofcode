from itertools import pairwise


def is_nice(s: str) -> bool:
    return (
        sum(letter in "aeiou" for letter in s) >= 3
        and any(a == b for a, b in pairwise(s))
        and not any(seq in s for seq in ("ab", "cd", "pq", "xy"))
    )


def part1(content: str) -> int:
    words = content.splitlines()
    return sum(is_nice(word) for word in words)


def cond1(s: str) -> bool:
    return any(s[i : i + 2] in s[:i] or s[i : i + 2] in s[i + 2 :] for i in range(len(s) - 1))


def cond2(s: str) -> bool:
    return any(a == b for a, b in zip(s, s[2:]))


def part2(content: str) -> int:
    words = content.splitlines()
    return sum(cond1(word) and cond2(word) for word in words)


with open("05.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
