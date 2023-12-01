import regex

with open('01.txt') as f: content = f.read()

s = 0
for line in content.splitlines():
    first = regex.search(r"(\d)", line).group()
    last = regex.search(r"(?r)(\d)", line).group()

    s += 10 * int(first)
    s += int(last)

print(s)

d = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

s2 = 0
for line in content.splitlines():
    first = regex.search(r"(one|two|three|four|five|six|seven|eight|nine|\d)", line).group()
    last = regex.search(r"(?r)(one|two|three|four|five|six|seven|eight|nine|\d)", line).group()

    s2 += 10 * (d.get(first) or int(first))
    s2 += d.get(last) or int(last)

print(s2)
