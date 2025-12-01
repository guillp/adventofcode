import re
from collections.abc import Iterator


def iter_reindeers(content: str) -> Iterator[tuple[str, tuple[int, int, int]]]:
    for name, speed, time, rest in re.findall(
        r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
        content,
        re.MULTILINE,
    ):
        yield name, (int(speed), int(time), int(rest))


def solve(content: str, seconds: int = 2503) -> Iterator[int]:
    reindeers = dict(iter_reindeers(content))

    part1 = 0
    for speed, time, rest in reindeers.values():
        d, m = divmod(seconds, int(time) + int(rest))
        distance = int(speed) * int(time) * d + int(speed) * min(int(time), m)
        part1 = max(distance, part1)

    yield part1

    state = dict.fromkeys(reindeers, 0)
    scores = dict.fromkeys(reindeers, 0)

    for i in range(seconds):
        max_dist = 0
        for name, distance in state.items():
            speed, time, rest = reindeers[name]
            d, m = divmod(i, time + rest)
            if m < time:
                distance += speed
            state[name] = distance
            max_dist = max(distance, max_dist)
        for name, distance in state.items():
            if distance == max_dist:
                scores[name] += 1

    yield max(scores.values())


assert tuple(
    solve(
        """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.""",
        1000,
    ),
) == (1120, 689)

with open("14.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
