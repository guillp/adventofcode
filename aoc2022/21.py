from sympy import solve, symbols  # type: ignore[import-untyped]


def part1(content: str) -> int:
    solved = {}
    to_solve = {}
    root = None
    for line in content.splitlines():
        key, val = line.split(": ")
        if key == "root":
            root = val
        if val.isdigit():
            solved[key] = int(val)
        else:
            to_solve[key] = val

    assert root

    while to_solve:
        for key, val in tuple(to_solve.items()):
            try:
                solved[key] = eval(val, solved)
                to_solve.pop(key)
            except NameError:
                pass

    return int(eval(root, solved))


def part2(content: str) -> int:
    solved = {}
    to_solve = {}
    root: str | None = None
    for line in content.splitlines():
        key, val = line.split(": ")
        if key == "root":
            root = val.replace("+", "-").replace("*", "-").replace("/", "-")
        elif key == "humn":
            solved["humn"] = symbols("humn")
        elif val.isdigit():
            solved[key] = int(val)
        else:
            to_solve[key] = val

    while to_solve:
        for key, val in tuple(to_solve.items()):
            try:
                solved[key] = eval(val, solved)
                to_solve.pop(key)
            except NameError:
                pass

    assert root is not None
    equation = eval(root, solved)
    return int(solve(equation)[0])


test_content = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

assert part1(test_content) == 152
assert part2(test_content) == 301

with open("21.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
