test_content = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""

with open('12.txt') as f: content = f.read()


def execute(content: str, a: int = 0, b: int = 0, c: int = 0) -> int:
    registers = {"a": a, "b": b, "c": c}
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
                if x in registers:
                    x = registers[x]
                if x != 0:
                    i += int(y) - 1
        i += 1

    return registers["a"]


assert execute(test_content) == 42
print(execute(content))
print(execute(content, c=1))
