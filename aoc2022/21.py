from sympy import symbols, solve

content = """root: pppw + sjmn
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

with open('21.txt') as f: content = f.read()

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

print(int(eval(root, solved)))

solved = {}
to_solve = {}
root = None
for line in content.splitlines():
    key, val = line.split(": ")
    if key == "root":
        root = val.replace("+", "-")
    if key == "humn":
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


print(int(solve(eval(root, solved))[0]))