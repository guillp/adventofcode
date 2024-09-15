from collections.abc import Iterator


def part1(content: str, *, part2: bool = False) -> int:
    registers = [0] * 6
    if part2:
        registers[0] = 1
    pointer = 0
    ip, *instructions = content.strip().splitlines()
    pointer_register = int(ip.split()[1])
    while 0 <= pointer < len(instructions):
        instruction = instructions[pointer]
        registers[pointer_register] = pointer
        match instruction.split():
            case "seti", a, b, c:
                registers[int(c)] = int(a)
            case "setr", a, b, c:
                registers[int(c)] = registers[int(a)]
            case "addi", a, b, c:
                registers[int(c)] = registers[int(a)] + int(b)
            case "addr", a, b, c:
                registers[int(c)] = registers[int(a)] + registers[int(b)]
            case "muli", a, b, c:
                registers[int(c)] = registers[int(a)] * int(b)
            case "mulr", a, b, c:
                registers[int(c)] = registers[int(a)] * registers[int(b)]
            case "eqri", a, b, c:
                registers[int(c)] = 1 if registers[int(a)] == int(b) else 0
            case "eqrr", a, b, c:
                # comparing something to register 0
                if a == "0":
                    return registers[int(b)]
                if b == "0":
                    return registers[int(a)]
                registers[int(c)] = 1 if registers[int(a)] == registers[int(b)] else 0
            case "gtir", a, b, c:
                registers[int(c)] = 1 if int(a) > registers[int(b)] else 0
            case "gtrr", a, b, c:
                registers[int(c)] = 1 if registers[int(a)] > registers[int(b)] else 0
            case "bani", a, b, c:
                registers[int(c)] = registers[int(a)] & int(b)
            case "bori", a, b, c:
                registers[int(c)] = registers[int(a)] | int(b)
            case _:
                assert False
        pointer = registers[pointer_register]
        pointer += 1

    assert False, "Solution not found!"


def part2(content: str) -> int:
    def iter_f() -> Iterator[int]:
        """This program is equivalent to my input, but is obviously MUCH faster.
        Change the values based on your input."""
        F = 0
        while True:
            D = F | 65536
            F = 733884
            while True:
                F = ((F + (D % 256) % 2**24) * 65899) % 2**24
                if D < 256:
                    yield F
                    break
                D //= 256

    history: list[int] = []
    for f in iter_f():
        if f in history:
            return history[-1]  # last element that does not repeat
        history.append(f)

    assert False, "Solution not found!"


# assert solve(test_content) == 6

with open("21.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
