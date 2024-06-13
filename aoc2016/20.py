from collections.abc import Iterator


def blacklist(ranges: tuple[tuple[int, int], ...], bl: int, br: int) -> Iterator[tuple[int, int]]:
    for rl, rr in ranges:
        assert rl <= rr
        if bl <= rl <= br < rr:  # overlap on the left
            yield br + 1, rr
        elif rl < bl <= br < rr:  # overlap in the middle
            yield rl, bl - 1
            yield br + 1, rr
        elif rl < bl <= rr <= br:  # overlap on the right
            yield rl, bl - 1
        elif br < rl or rr < bl:  # no overlap
            yield rl, rr
        elif bl <= rl <= rr <= br:  # full overlap
            pass
        else:
            assert False


def solve(content: str, max_: int = 2**32 - 1) -> Iterator[int]:
    ranges: tuple[tuple[int, int], ...] = ((0, max_),)
    for line in content.splitlines():
        blacklist_left, blacklist_right = (int(x) for x in line.split("-"))
        ranges = tuple(blacklist(ranges, blacklist_left, blacklist_right))

    yield min(ranges)[0]
    yield sum(right - left + 1 for left, right in ranges)


with open("20.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
