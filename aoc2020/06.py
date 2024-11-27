def solve(content: str) -> tuple[int, int]:
    all_answers = set("abcdefghijklmnopqrstuvwxyz")
    part1 = part2 = 0
    for group in content.strip().split("\n\n"):
        answers = set(group.replace("\n", ""))
        part1 += len(answers)
        group_answers = all_answers.copy()
        for person in group.splitlines():
            group_answers &= set(person)
        part2 += len(group_answers)
    return part1, part2


assert solve("""\
abc

a
b
c

ab
ac

a
a
a
a

b
""") == (11, 6)

with open("06.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
