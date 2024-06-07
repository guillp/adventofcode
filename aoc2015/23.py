def solve(content: str, part2: bool = False) -> int:
    registers = {"a": 0, "b": 0}
    if part2:
        registers["a"] = 1

    i = 0

    instructions = content.splitlines()

    while i < len(instructions):
        match instructions[i].split():
            case "hlf", reg:
                registers[reg] //= 2
            case "tpl", reg:
                registers[reg] *= 3
            case "inc", reg:
                registers[reg] += 1
            case "jmp", offset:
                i += int(offset) - 1
            case "jie", reg, offset:
                if registers[reg.strip(",")] % 2 == 0:
                    i += int(offset) - 1
            case "jio", reg, offset:
                if registers[reg.strip(",")] == 1:
                    i += int(offset) - 1
            case err:
                assert False, err

        i += 1

    return registers["b"]


with open("23.txt") as finput:
    content = finput.read()

print(solve(content))
print(solve(content, part2=True))
