import re


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for first, second, letter, password in re.findall(r"^(\d+)-(\d+) ([a-z]): (.+)$", content.strip(), re.MULTILINE):
        left = int(first)
        right = int(second)
        part1 += left <= password.count(letter) <= right
        if (left <= len(password) and password[left - 1] == letter) + (
            right <= len(password) and password[right - 1] == letter
        ) == 1:
            part2 += 1

    return part1, part2


assert tuple(
    solve("""\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""),
) == (2, 1)


with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
