from collections import Counter, deque


def solve(content: str, *, part2: bool = False) -> int:
    lanternfishs = Counter(int(x) for x in content.split(","))
    queue = deque(lanternfishs.get(x, 0) for x in range(6))
    queue.extend((0, 0, 0))
    for day in range(256 if part2 else 80):
        queue.rotate(-1)
        queue[6] += queue[8]

    return sum(queue)


assert solve("3,4,3,1,2") == 5934
assert solve("3,4,3,1,2", part2=True) == 26984457539

with open("06.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
