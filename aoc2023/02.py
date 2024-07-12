import re


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for line in content.splitlines():
        game_id = int(re.findall(r"^Game (\d+):", line)[0])

        red = max(int(x) for x in re.findall(r"(\d+) red", line))
        green = max(int(x) for x in re.findall(r"(\d+) green", line))
        blue = max(int(x) for x in re.findall(r"(\d+) blue", line))
        if red <= 12 and green <= 13 and blue <= 14:
            part1 += game_id
        part2 += red * green * blue

    return part1, part2


assert solve("""\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""") == (8, 2286)

with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
