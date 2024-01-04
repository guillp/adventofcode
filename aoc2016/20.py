def blacklist(ranges: tuple[tuple[int, int]], bl: int, br: int):
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


def solve(content: str, max: int = 2**32 - 1) -> tuple[int, int]:
    ranges = [(0, max)]
    for line in content.splitlines():
        blacklist_left, blacklist_right = (int(x) for x in line.split("-"))
        ranges = tuple(blacklist(ranges, blacklist_left, blacklist_right))

    part1 = min(ranges)[0]
    part2 = sum(right - left + 1 for left, right in ranges)
    return part1, part2


with open("20.txt") as f:
    content = f.read()
print(*solve(content, 2**32 - 1))
