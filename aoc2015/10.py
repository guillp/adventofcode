import re
from collections.abc import Iterator


def look_and_say(s: str) -> str:
    groups = re.findall(r"1+|2+|3+", s)
    return "".join(f"{len(group)}{group[0]}" for group in groups)


def solve(content: str) -> Iterator[int]:
    for _ in range(40):
        content = look_and_say(content)

    yield len(content)

    for _ in range(10):
        content = look_and_say(content)

    yield len(content)


content = "1321131112"
for part in solve(content):
    print(part)
