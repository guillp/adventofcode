from collections import Counter


def solve(content: str) -> tuple[str, str]:
    messages = content.strip().splitlines()
    n = len(messages[0])

    most_common: list[str] = []
    least_common: list[str] = []
    for i in range(n):
        count = Counter(message[i] for message in messages)
        most_common += count.most_common()[0][0]
        least_common += count.most_common()[-1][0]

    return "".join(most_common), "".join(least_common)


test_content = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""


assert solve(test_content) == ("easter", "advent")


with open("06.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
