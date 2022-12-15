from stringparser import Parser

with open("05.txt", "rt") as finput:
    content = finput.read()


def parse(content: str) -> tuple[tuple[list[str]], list[tuple[int, str, str]]]:
    stacks_str, moves_str = content.split("\n\n")
    *stack_contents, stack_names = stacks_str.splitlines()
    stacks = {name: [] for name in stack_names.split()}
    for line in reversed(stack_contents):
        for crate_name, crate in zip(stack_names.split(), line[1::4]):
            if crate.strip():
                stacks[crate_name].append(crate)

    parser = Parser("move {:d} from {} to {}")
    moves = [parser(line) for line in moves_str.splitlines()]
    return stacks, moves


stacks, moves = parse(content)

for n, s, d in moves:
    for _ in range(n):
        stacks[d].append(stacks[s].pop())

print([stack[-1] for stack in stacks.values()])

stacks, moves = parse(content)
for n, s, d in moves:
    stacks[d].extend(stacks[s][-n:])
    stacks[s] = stacks[s][:-n]

print([stack[-1] for stack in stacks.values()])
