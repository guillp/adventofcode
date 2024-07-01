import re


def parse(content: str) -> tuple[dict[str, list[str]], list[tuple[int, str, str]]]:
    stacks_str, moves_str = content.split("\n\n")
    *stack_contents, stack_names = stacks_str.splitlines()
    stacks: dict[str, list[str]] = {name: [] for name in stack_names.split()}
    for line in reversed(stack_contents):
        for crate_name, crate in zip(stack_names.split(), line[1::4]):
            if crate.strip():
                stacks[crate_name].append(crate)

    moves = [
        (int(amount), from_, to)
        for amount, from_, to in re.findall(r"^move (\d+) from (\d+) to (\d+)$", moves_str, re.MULTILINE)
    ]
    return stacks, moves


def part1(content: str) -> str:
    stacks, moves = parse(content)

    for n, s, d in moves:
        for _ in range(n):
            stacks[d].append(stacks[s].pop())

    return "".join([stack[-1] for stack in stacks.values()])


def part2(content: str) -> str:
    stacks, moves = parse(content)
    for n, s, d in moves:
        stacks[d].extend(stacks[s][-n:])
        stacks[s] = stacks[s][:-n]

    return "".join([stack[-1] for stack in stacks.values()])


test_content = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

assert part1(test_content) == "CMZ"
assert part2(test_content) == "MCD"

with open("05.txt") as finput:
    content = finput.read()

print(part1(content))
print(part2(content))
