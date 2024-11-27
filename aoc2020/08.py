def part1(content: str) -> int:
    acc = 0
    pointer = 0
    instructions = content.strip().splitlines()
    visited = set()
    while pointer not in visited:
        instruction = instructions[pointer]
        visited.add(pointer)
        match instruction.split():
            case "acc", val:
                acc += int(val)
            case "jmp", val:
                pointer += int(val) - 1
            case "nop", val:
                pass
        pointer += 1
    return acc


def part2(content: str) -> int:
    instructions = content.strip().splitlines()
    for corrupted_instruction in instructions:
        acc = 0
        pointer = 0
        visited = set()
        while pointer not in visited:
            if pointer == len(instructions):
                return acc
            instruction = instructions[pointer]
            visited.add(pointer)
            match instruction.split():
                case "acc", val:
                    acc += int(val)
                case "jmp", val if instruction != corrupted_instruction:
                    pointer += int(val) - 1
                case "nop", val if instruction == corrupted_instruction:
                    pointer += int(val) - 1
            pointer += 1

    assert False, "Solution not found!"


test_content = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

assert part1(test_content) == 5
assert part2(test_content) == 8

with open("08.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
