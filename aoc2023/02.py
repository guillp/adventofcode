import re

with open("02.txt") as f:
    content = f.read()

s1 = s2 = 0
for line in content.splitlines():
    game_id = int(re.findall(r"^Game (\d+):", line)[0])

    red = max(int(x) for x in re.findall(r"(\d+) red", line))
    green = max(int(x) for x in re.findall(r"(\d+) green", line))
    blue = max(int(x) for x in re.findall(r"(\d+) blue", line))
    if red <= 12 and green <= 13 and blue <= 14:
        s1 += game_id
    s2 += red * green * blue

print(s1)
print(s2)
