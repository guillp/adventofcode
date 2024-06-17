from collections import defaultdict


def next_instruction(instructions: list[str], pointer: int = 0, **registers: int) -> tuple[dict[str, int], int]:
    registers = defaultdict(int, registers)

    def get_value(p: str) -> int:
        if p.isalpha():
            return registers[p]
        return int(p)

    match instructions[pointer].split():
        case "set", x, y:
            registers[x] = get_value(y)
        case "sub", x, y:
            registers[x] -= get_value(y)
        case "mul", x, y:
            registers[x] *= get_value(y)
        case "jnz", x, y if get_value(x) != 0:
            pointer += get_value(y) - 1

    return registers, pointer + 1


def part1(content: str) -> int:
    instructions = content.strip().splitlines()

    pointer = 0
    registers: dict[str, int] = defaultdict(int)

    mul_count = 0
    while 0 <= pointer < len(instructions):
        if instructions[pointer].startswith("mul "):
            mul_count += 1
        registers, pointer = next_instruction(instructions, pointer, **registers)

    return mul_count


def part2(content: str) -> int:
    instructions = content.strip().splitlines()

    pointer = 0
    registers: dict[str, int] = defaultdict(int, a=1)

    while 0 <= pointer < len(instructions):
        if instructions[pointer] == "set f 1":
            break  # execute instruction up to this point to get values in b and c
        registers, pointer = next_instruction(instructions, pointer, **registers)

    # replace the remaining of the program with an equivalent fast program
    b, c = registers["b"], registers["c"]
    h = 0
    for b in range(b, c + 1, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break

    return h


with open("23.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
