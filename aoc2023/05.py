from itertools import count
from typing import Callable

content = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

with open("05.txt") as f:
    content = f.read()


def read_map() -> Callable[[int], int]:
    ranges: list[tuple[int, int, int]] = []

    while lines and lines[0].strip():
        dest, source, length = (int(x) for x in lines.pop(0).split())
        ranges.append((dest, source, length))
    if lines:
        lines.pop(0)

    def check(i: int) -> int:
        for dest, source, length in ranges:
            if source <= i < source + length:
                return dest + i - source
        return i

    return check


lines = content.splitlines()

assert lines[0].startswith("seeds: ")
seeds = tuple(int(x) for x in lines.pop(0).removeprefix("seeds: ").split())
assert lines[0] == ""
lines.pop(0)

assert lines[0].startswith("seed-to-soil map:")
lines.pop(0)
seed2soil = read_map()

assert lines[0].startswith("soil-to-fertilizer map:")
lines.pop(0)
soil2fertilizer = read_map()


assert lines[0].startswith("fertilizer-to-water map:")
lines.pop(0)
fertilizer2water = read_map()

assert lines[0].startswith("water-to-light map:")
lines.pop(0)
water2light = read_map()

assert lines[0].startswith("light-to-temperature map:")
lines.pop(0)
light2temperature = read_map()

assert lines[0].startswith("temperature-to-humidity map:")
lines.pop(0)
temperature2humidity = read_map()

assert lines[0].startswith("humidity-to-location map:")
lines.pop(0)
humidity2location = read_map()


def seed2location(seed: int) -> int:
    soil = seed2soil(seed)
    fertilizer = soil2fertilizer(soil)
    water = fertilizer2water(fertilizer)
    light = water2light(water)
    temperature = light2temperature(light)
    humidity = temperature2humidity(temperature)
    location = humidity2location(humidity)
    return location


print(min(seed2location(seed) for seed in seeds))


def read_map_reverse() -> Callable[[int], int]:
    ranges: list[tuple[int, int, int]] = []

    while lines and lines[0].strip():
        dest, source, length = (int(x) for x in lines.pop(0).split())
        ranges.append((dest, source, length))
    if lines:
        lines.pop(0)

    def check(i: int) -> int:
        for dest, source, length in ranges:
            if dest <= i < dest + length:
                return source + i - dest
        return i

    return check


lines = content.splitlines()

assert lines[0].startswith("seeds: ")
seed_spec = tuple(int(x) for x in lines.pop(0).removeprefix("seeds: ").split())
seed_ranges = [(start, length) for start, length in zip(seed_spec[::2], seed_spec[1::2])]


def check_seed(seed: int) -> bool:
    for start, length in seed_ranges:
        if start <= seed < start + length:
            return True
    return False


assert lines[0] == ""
lines.pop(0)

assert lines[0].startswith("seed-to-soil map:")
lines.pop(0)
soil2seed = read_map_reverse()

assert lines[0].startswith("soil-to-fertilizer map:")
lines.pop(0)
fertilizer2soil = read_map_reverse()

assert lines[0].startswith("fertilizer-to-water map:")
lines.pop(0)
water2fertilizer = read_map_reverse()

assert lines[0].startswith("water-to-light map:")
lines.pop(0)
light2water = read_map_reverse()

assert lines[0].startswith("light-to-temperature map:")
lines.pop(0)
temperature2light = read_map_reverse()

assert lines[0].startswith("temperature-to-humidity map:")
lines.pop(0)
humidity2temperature = read_map_reverse()

assert lines[0].startswith("humidity-to-location map:")
lines.pop(0)
location2humidity = read_map_reverse()

for location in count():
    if check_seed(
        soil2seed(
            fertilizer2soil(
                water2fertilizer(
                    light2water(
                        temperature2light(humidity2temperature(location2humidity(location)))
                    )
                )
            )
        )
    ):
        print(location)
        break
