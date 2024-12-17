import re
from collections.abc import Iterator


def solve(content: str) -> Iterator[str|int]:
    a, b, c, *instructions = map(int, re.findall(r"\d+", content, re.MULTILINE))
    yield ",".join(map(str, computer(a, b, c, *instructions)))

    # On each iteration, the computer divides `a` by 8 so it becomes smaller and smaller until it reaches 0.
    # There is 1 output instruction for each iteration.
    # There are 15 instructions so `8**15 <= a < 8**16`.
    # We'll work backwards to find the initial value of `a`.
    # On every step `i`:
    #  - value of `a` is multiplied by 8 and added a number m that is less than 8**(i+1),
    #    so that the output matches the last `i` instructions.
    #  - value of `a` will then always be 8**i <= a < 8**(i+1)
    a = 0
    for i in range(len(instructions)):
        for m in range(8**(i+1)):
            if list(computer(a * 8 + m, 0, 0, *instructions)) == instructions[-i-1:]:
                a = a * 8 + m
                break
        else:
            assert False, "Solution not found :("
        assert 8 ** i <= a < 8 ** (i + 1)

    assert tuple(computer(a, 0, 0, *instructions)) == tuple(instructions)
    yield a


def computer(a: int, b: int, c: int, *instructions: int) -> Iterator[int]:
    pointer = 0

    def combo_operand(operand: int) -> int:
        return [0, 1, 2, 3, a, b, c][operand]

    while 0 <= pointer < len(instructions) - 1:
        instruction, operand = instructions[pointer : pointer + 2]
        match instruction:
            case 0:
                a >>= combo_operand(operand)
            case 1:
                b ^= operand
            case 2:
                b = combo_operand(operand) % 8
            case 3:
                if a:
                    pointer = operand - 2
            case 4:
                b ^= c
            case 5:
                yield combo_operand(operand) % 8
            case 6:
                b = a >> combo_operand(operand)
            case 7:
                c = a >> combo_operand(operand)
        pointer += 2


test_content = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

assert next(solve(test_content)) == "4,6,3,5,6,3,5,2,1,0"

with open("17.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
