from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    calories = [sum(int(x) for x in elf.split()) for elf in content.split("\n\n")]
    yield max(calories)
    yield sum(sorted(calories)[-3:])


test_content = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
assert tuple(solve(test_content)) == (24000, 45000)

with open("01.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
