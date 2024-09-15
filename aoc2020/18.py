import re


def evaluate(operation: str, *, advanced: bool = False) -> int:
    operation = operation.replace(" ", "")
    while "(" in operation:
        operation = re.sub(
            r"\(([^\(]+?)\)",
            lambda m: str(evaluate(m.group(1), advanced=advanced)),
            operation,
            count=1,
        )
    while advanced and "+" in operation:
        operation = re.sub(r"\d+[+]\d+", lambda m: str(eval(m.group(0))), operation, count=1)
    while "+" in operation or "*" in operation:
        operation = re.sub(r"\d+[+*]\d+", lambda m: str(eval(m.group(0))), operation, count=1)
    return int(operation)


def part1(content: str) -> int:
    return sum(evaluate(operation) for operation in content.splitlines())


def part2(content: str) -> int:
    return sum(evaluate(operation, advanced=True) for operation in content.splitlines())


assert part1("2 * 3 + (4 * 5)") == 26
assert part1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert part1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert part1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

assert part2("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert part2("2 * 3 + (4 * 5)") == 46
assert part2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert part2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert part2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

with open("18.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
