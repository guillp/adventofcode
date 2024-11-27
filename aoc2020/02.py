import re


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for first, second, letter, password in re.findall(r"^(\d+)-(\d+) ([a-z]): (.+)$", content.strip(), re.MULTILINE):
        left, right = int(first), int(second)
        part1 += left <= password.count(letter) <= right
        part2 += (password[left - 1] == letter) ^ (password[right - 1] == letter)

    return part1, part2


assert solve("""\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""") == (2, 1)


with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
