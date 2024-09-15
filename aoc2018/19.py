def solve(content: str, *, part2: bool = False) -> int:
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
                if pointer == 3:  ## THIS PART MAY CHANGE BASED ON YOUR INPUT
                    n = max(registers)
                    # program adds all factors of a given number into register 0
                    return sum({factor for i in range(1, int(n**0.5) + 1) if n % i == 0 for factor in (i, n // i)})
                registers[int(c)] = registers[int(a)] * registers[int(b)]
            case "eqrr", a, b, c:
                registers[int(c)] = 1 if registers[int(a)] == registers[int(b)] else 0
            case "gtrr", a, b, c:
                registers[int(c)] = 1 if registers[int(a)] > registers[int(b)] else 0
            case _:
                assert False
        pointer = registers[pointer_register]
        pointer += 1
    return registers[0]


test_content = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
"""

# assert solve(test_content) == 6

with open("19.txt") as f:
    content = f.read()
print(solve(content))
print(solve(content, part2=True))
