import statistics
from collections.abc import Iterator


def solve(content: str) -> Iterator[int]:
    positions = tuple(sorted(int(x) for x in content.strip().split(",")))
    median = round(statistics.median(positions))
    yield sum(abs(pos - median) for pos in positions)
    average = round(statistics.mean(positions))
    yield min(
        sum(c + 1 for pos in positions for c in range(abs(pos - best_pos)))
        for best_pos in (average - 1, average, average + 1)
    )


assert tuple(solve("16,1,2,0,4,2,7,1,2,14")) == (37, 168)

with open("07.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
