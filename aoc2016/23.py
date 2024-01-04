test_content = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


def execute(
    content: str, a: int = 0, b: int = 0, c: int = 0, part2: bool = False
) -> int:
    registers = {"a": a, "b": b, "c": c}

    def val(x: str|int) -> int:
        if x in registers:
            return registers[x]
        else:
            return int(x)

    instructions = [tuple(i.split()) for i in content.splitlines()]
    i = 0
    while i < len(instructions):
        match instructions[i]:
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
                if y in registers:
                    y = registers[y]
                if x != 0:
                    y = int(y)
                    if y < 0:
                        if y == -2:
                            # probably an add operation
                            match instructions[i - 2], instructions[i - 1]:
                                case ("dec", a), ("inc", b):
                                    registers[b] += registers[a]
                                    registers[a] = 0
                                case ("inc", b), ("dec", a):
                                    registers[b] += registers[a]
                                    registers[a] = 0
                                case _:
                                    assert False
                        elif y == -5:
                            # probably a multiply operation
                            match instructions[i-5:i]:
                                case [('cpy', a, b), ("inc", c), ("dec", bb), ("jnz", bbb, '-2'), ("dec", d)]:
                                    assert b == bb == bbb
                                    registers[c] += val(d)*val(a)
                                case _:
                                    assert False
                        else:
                            i += y - 1
                    else:
                        i += y - 1
            case "tgl", x:
                if x in registers:
                    x = registers[x]
                if x != 0 and 0 <= i + x < len(instructions):
                    match instructions[i + x]:
                        case "inc", y:
                            instructions[i + x] = "dec", y
                        case _, y:
                            instructions[i + x] = "inc", y
                        case "jnz", y, z:
                            instructions[i + x] = "cpy", y, z
                        case _, y, z:
                            instructions[i + x] = "jnz", y, z

        i += 1

    print(registers)


# assert execute(test_content) == 3

with open("23.txt") as f:
    content = f.read()
print(execute(content, a=7))

print(execute(content, a=12, part2=True))
