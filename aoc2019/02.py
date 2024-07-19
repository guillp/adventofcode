import operator
from collections.abc import Iterator


def int_program(positions: tuple[int, ...], noun: int, verb: int) -> int:
    positions_list = list(positions)
    positions_list[1] = noun
    positions_list[2] = verb
    position, opcode = 0, positions[0]
    while opcode != 99:
        if opcode in (1, 2):
            left, right, target = positions[position + 1 : position + 4]
            positions_list[target] = {1: operator.add, 2: operator.mul}[opcode](positions[left], positions[right])
        position += 4
        opcode = positions[position]

    return positions[0]


def solve(content: str) -> Iterator[int]:
    positions = tuple(int(x) for x in content.split(","))

    yield int_program(positions, 12, 2)

    for verb in range(0, 100):
        for noun in range(0, 100):
            if int_program(positions, noun, verb) == 19690720:
                yield 100 * noun + verb


test_content = "1,9,10,3,2,3,11,0,99,30,40,50"

with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
