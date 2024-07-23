import re
from collections.abc import Iterator


def apply_value_mask(value: int, mask: str) -> int:
    return int("".join(v if m == "X" else m for v, m in zip(f"{value:036b}", mask)), 2)


def apply_mem_mask(mem: int, mask: str) -> str:
    return "".join(v if m == "0" else m for v, m in zip(f"{mem:036b}", mask))


def unfloat(mask: str) -> Iterator[int]:
    if "X" in mask:
        parts = mask.split("X", 1)
        for X in "01":
            yield from unfloat(X.join(parts))
    else:
        yield int(mask, 2)


def solve(content: str) -> tuple[int, int]:
    memory = {}
    memory_v2 = {}
    for line in content.splitlines():
        if line.startswith("mask = "):
            mask = line[7:]
        else:
            mem, value = (int(x) for x in re.findall(r"\d+", line))
            memory[mem] = apply_value_mask(value, mask)
            for float_mem in unfloat(apply_mem_mask(mem, mask)):
                memory_v2[float_mem] = value

    return sum(memory.values()), sum(memory_v2.values())


with open("14.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
