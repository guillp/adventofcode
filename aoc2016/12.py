def solve(content: str, *, part2: bool = False) -> int:
    registers = {"a": 0, "b": 0, "c": 0}
    if part2:
        registers["c"] = 1

    instructions = content.splitlines()
    i = 0
    while i < len(instructions):
        match instructions[i].split():
            case "cpy", x, y:
                if x in registers:
                    registers[y] = registers[x]
                else:
                    registers[y] = int(x)
            case "inc", x:
                registers[x] += 1
            case "dec", x:
                registers[x] -= 1
            case "jnz", x, y:
                if registers[x] if x.isalpha() else int(x) != 0:
                    i += int(y) - 1
        i += 1

    return registers["a"]


test_content = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""

with open("12.txt") as f:
    content = f.read()

assert solve(test_content) == 42
print(solve(content))
print(solve(content, part2=True))
