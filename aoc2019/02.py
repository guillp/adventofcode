import operator
from collections.abc import Iterator


def execute(program: tuple[int, ...], noun: int, verb: int) -> int:
    positions = list(program)
    positions[1] = noun
    positions[2] = verb
    position, opcode = 0, positions[0]
    while opcode != 99:
        if opcode in (1, 2):
            left, right, target = positions[position + 1 : position + 4]
            positions[target] = {1: operator.add, 2: operator.mul}[opcode](positions[left], positions[right])
        position += 4
        opcode = positions[position]

    return positions[0]


def solve(content: str) -> Iterator[int]:
    positions = tuple(int(x) for x in content.split(","))
    yield execute(positions, 12, 2)

    for verb in range(100):
        for noun in range(100):
            if execute(positions, noun, verb) == 19690720:
                yield 100 * noun + verb


test_content = "1,9,10,3,2,3,11,0,99,30,40,50"

with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
