import re
from collections import defaultdict
from datetime import datetime, time, timedelta


def parse(content: str) -> dict[int, dict[time, int]]:
    current_guard = None
    guards: dict[int, dict[time, int]] = {}
    for line in sorted(content.splitlines()):
        match [int(x) for x in re.findall(r"(\d+)", line)]:
            case _, _, _, _, _, guard:
                current_guard = guard
            case year, month, day, hour, minute if "falls asleep" in line:
                asleep_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            case year, month, day, hour, minute if "wakes up" in line and current_guard is not None:
                awake_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
                while asleep_time < awake_time:
                    guards.setdefault(current_guard, defaultdict(int))
                    guards[current_guard][asleep_time.time()] += 1
                    asleep_time += timedelta(minutes=1)
            case _:
                breakpoint()

    return guards


def part1(content: str) -> int:
    guards = parse(content)
    most_asleep_guard = max(guards, key=lambda g: sum(guards[g].values()))
    most_asleep_minute = max(guards[most_asleep_guard], key=lambda minute: guards[most_asleep_guard][minute])
    return most_asleep_guard * most_asleep_minute.minute


def part2(content: str) -> int:
    guards = parse(content)
    most_asleep_guard = max(guards, key=lambda g: max(guards[g].values()))
    most_asleep_minute = max(guards[most_asleep_guard], key=lambda minute: guards[most_asleep_guard][minute])
    return most_asleep_guard * most_asleep_minute.minute


test_content = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""


assert part1(test_content) == 240
assert part2(test_content) == 4455

with open("04.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
