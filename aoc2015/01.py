with open("01.txt") as finput:
    line = finput.read()

print(line.count("(") - line.count(")"))

f = 0
for i, c in enumerate(line):
    if c == "(":
        f += 1
    elif c == ")":
        f -= 1
    if f < 0:
        print(i + 1)
        break
