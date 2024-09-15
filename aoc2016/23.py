def solve(content: str, *, part2: bool = False) -> int:
    registers = {"a": 12 if part2 else 7, "b": 0, "c": 0}

    def val(x: str) -> int:
        return registers[x] if x in registers else int(x)

    instructions = [tuple(i.split()) for i in content.splitlines()]
    i = 0
    while i < len(instructions):
        match instructions[i]:
            case "cpy", x, y:
                registers[y] = val(x)
            case "inc", x:
                registers[x] += 1
            case "dec", x:
                registers[x] -= 1
            case "jnz", x, y:
                y_ = val(y)
                if val(x) != 0:
                    if y_ < 0:
                        if y_ == -2:
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
                        elif y_ == -5:
                            # probably a multiply operation
                            match instructions[i - 5 : i]:
                                case [
                                    ("cpy", a, b),
                                    ("inc", c),
                                    ("dec", bb),
                                    ("jnz", bbb, "-2"),
                                    ("dec", d),
                                ]:
                                    assert b == bb == bbb
                                    registers[c] += val(d) * val(a)
                                case _:
                                    assert False
                        else:
                            i += y_ - 1
                    else:
                        i += y_ - 1
            case "tgl", x:
                j = i + val(x)
                if val(x) != 0 and 0 <= j < len(instructions):
                    match instructions[j]:
                        case "inc", y:
                            instructions[j] = "dec", y
                        case _, y:
                            instructions[j] = "inc", y
                        case "jnz", y, z:
                            instructions[j] = "cpy", y, z
                        case _, y, z:
                            instructions[j] = "jnz", y, z

        i += 1

    return registers["a"]


test_content = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


assert solve(test_content) == 3

with open("23.txt") as f:
    content = f.read()
print(solve(content))
print(solve(content, part2=True))
