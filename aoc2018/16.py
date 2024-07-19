import re
from collections.abc import Callable, Iterator


def addr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] + reg[b]
    return tuple(res)


def addi(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] + b
    return tuple(res)


def mulr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] * reg[b]
    return tuple(res)


def muli(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] * b
    return tuple(res)


def banr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] & reg[b]
    return tuple(res)


def bani(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] & b
    return tuple(res)


def borr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] | reg[b]
    return tuple(res)


def bori(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a] | b
    return tuple(res)


def setr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = reg[a]
    return tuple(res)


def seti(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = a
    return tuple(res)


def gtir(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if a > reg[b] else 0
    return tuple(res)


def gtri(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if reg[a] > b else 0
    return tuple(res)


def gtrr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if reg[a] > reg[b] else 0
    return tuple(res)


def eqir(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if a == reg[b] else 0
    return tuple(res)


def eqri(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if reg[a] == b else 0
    return tuple(res)


def eqrr(reg: tuple[int, ...], a: int, b: int, c: int) -> tuple[int, ...]:
    res = list(reg)
    res[c] = 1 if reg[a] == reg[b] else 0
    return tuple(res)


def solve(content: str) -> Iterator[int]:
    samples = content.strip().split("\n\n")
    if len(samples) > 2:
        *samples, _, program = samples

    all_opcodes = frozenset(
        {
            addr,
            addi,
            mulr,
            muli,
            banr,
            bani,
            borr,
            bori,
            setr,
            seti,
            gtir,
            gtri,
            gtrr,
            eqir,
            eqri,
            eqrr,
        }
    )
    instructions_map = {i: all_opcodes for i in range(16)}
    part1 = 0
    for sample in samples:
        br0, br1, br2, br3, i, a, b, c, ar0, ar1, ar2, ar3 = map(int, re.findall(r"\d+", sample))

        candidates = {opcode for opcode in all_opcodes if opcode((br0, br1, br2, br3), a, b, c) == (ar0, ar1, ar2, ar3)}

        if len(candidates) >= 3:
            part1 += 1

        instructions_map[i] &= candidates
        if not instructions_map[i]:
            assert False

    yield part1

    known_opcodes: dict[int, Callable[[tuple[int, ...], int, int, int], tuple[int, ...]]] = {}
    while len(known_opcodes) < 16:
        for opcode, methods in instructions_map.items():
            methods -= set(known_opcodes.values())  # type: ignore[arg-type]
            if len(methods) == 1:
                known_opcodes[opcode] = tuple(methods)[0]

    registers: tuple[int, ...] = (0, 0, 0, 0)
    for line in program.splitlines():
        opcode, a, b, c = map(int, line.split())
        registers = known_opcodes[opcode](registers, a, b, c)

    yield registers[0]


assert (
    next(
        solve(
            """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""
        )
    )
    == 1
)

with open("16.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
