from collections import Counter

content = """eedadn
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

with open("06.txt") as f:
    content = f.read()

messages = content.splitlines()
n = len(messages[0])

most_common = []
least_common = []
for i in range(n):
    count = Counter(message[i] for message in content.splitlines())
    most_common += count.most_common()[0][0]
    least_common += count.most_common()[-1][0]

print("".join(most_common))
print("".join(least_common))
