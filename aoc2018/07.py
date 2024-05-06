import re

test_content = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def part1(content: str) -> str:
    predecessors = {}
    successors = {}
    for line in content.splitlines():
        before, after = re.match(
            r"Step (\w) must be finished before step (\w) can begin", line
        ).groups()
        predecessors.setdefault(after, set())
        predecessors[after].add(before)
        successors.setdefault(before, set())
        successors[before].add(after)

    all_steps = set(successors) | set(predecessors)
    roots = set(successors) - set(predecessors)
    path = sorted(roots)[0]
    while set(path) != all_steps:
        visitable = sorted(
            successor
            for successor in all_steps - set(path)
            if all(
                predecessor in path for predecessor in predecessors.get(successor, ())
            )
        )
        path += visitable[0]
    return path


def part2(content: str, nb_workers: int, base_time: int) -> int:
    predecessors = {}
    successors = {}
    for line in content.splitlines():
        before, after = re.match(
            r"Step (\w) must be finished before step (\w) can begin", line
        ).groups()
        predecessors.setdefault(after, set())
        predecessors[after].add(before)
        successors.setdefault(before, set())
        successors[before].add(after)

    all_steps = set(successors) | set(predecessors)
    roots = set(successors) - set(predecessors)

    in_progress = {root: ord(root) - 64 + base_time for root in sorted(roots)}
    completed = set()

    required_seconds = 0
    while completed != all_steps:
        for step, worker in zip(in_progress, range(nb_workers)):
            in_progress[step] -= 1
            if in_progress[step] == 0:
                completed.add(step)

        for step in completed:
            if step in in_progress:
                del in_progress[step]

        required_seconds += 1
        for visitable in sorted(
            successor
            for successor in all_steps - set(in_progress) - completed
            if all(
                predecessor in completed
                for predecessor in predecessors.get(successor, ())
            )
        ):
            in_progress[visitable] = ord(visitable) - 64 + base_time

    return required_seconds


assert part2(test_content, 2, 0) == 15
assert part1(test_content) == "CABDFE"


with open("07.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content, 5, 60))
