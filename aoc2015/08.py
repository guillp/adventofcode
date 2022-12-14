import json

with open('08.txt', "rt") as finput:
    content = finput.read()


s = 0

for line in content.splitlines():
    s += len(line) - len(eval(line))

print(s)


s2 = 0
for line in content.splitlines():
    s2 += len(json.dumps(line)) - len(line)


print(s2)