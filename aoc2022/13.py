import json

content = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

with open("13.txt", "rt") as finput:
    content = finput.read()


def compare(left: int | list, right: int | list, level: int = 0) -> bool | None:
    # print("  "*level,"Compare", left, "vs", right)
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        # print("  "*level,"left is smaller" if left < right else "right is smaller")
        return left < right
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            if (c := compare(l, r, level=level + 1)) is None:
                continue
            return c
        if len(left) == len(right):
            return None
        return len(left) < len(right)


s = 0
for i, pair in enumerate(content.split("\n\n"), start=1):
    left, right = pair.splitlines()
    left = json.loads(left)
    right = json.loads(right)
    if compare(left, right):
        s += i
        print(i, True)

print(s)


all_packets = [json.loads(packet) for packet in content.splitlines() if packet]
all_packets.append([[2]])
all_packets.append([[6]])


def bubble_sort(packets):
    swapped = False
    for n in reversed < (range(len(packets))):
        for i in range(n):
            if compare(packets[i], packets[i + 1]) is False:
                swapped = True
                packets[i], packets[i + 1] = packets[i + 1], packets[i]
        if not swapped:
            return


bubble_sort(all_packets)
print(all_packets.index([[2]]) + 1, all_packets.index([[6]]) + 1)
