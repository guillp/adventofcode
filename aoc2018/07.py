import re
from collections.abc import Iterator


def solve(content: str, nb_workers: int = 5, base_time: int = 60) -> Iterator[str | int]:
    predecessors: dict[str, set[str]] = {}
    successors: dict[str, set[str]] = {}
    for before, after in re.findall(r"^Step (\w) must be finished before step (\w) can begin", content, re.MULTILINE):
        predecessors.setdefault(after, set())
        predecessors[after].add(before)
        successors.setdefault(before, set())
        successors[before].add(after)

    all_steps = set(successors) | set(predecessors)
    roots = set(successors) - set(predecessors)
    path = sorted(roots)[0]
    while set(path) != all_steps:
        visitables = sorted(
            successor
            for successor in all_steps - set(path)
            if all(predecessor in path for predecessor in predecessors.get(successor, ()))
        )
        path += visitables[0]
    yield path

    in_progress = {root: ord(root) - 64 + base_time for root in sorted(roots)}
    completed: set[str] = set()

    required_seconds = 0
    while completed != all_steps:
        for step, worker in zip(in_progress, range(nb_workers), strict=False):
            in_progress[step] -= 1
            if in_progress[step] == 0:
                completed.add(step)

        for step in completed:
            in_progress.pop(step, None)

        required_seconds += 1
        for visitable in sorted(
            successor
            for successor in all_steps - set(in_progress) - completed
            if all(predecessor in completed for predecessor in predecessors.get(successor, ()))
        ):
            in_progress[visitable] = ord(visitable) - 64 + base_time

    yield required_seconds


test_content = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


assert tuple(solve(test_content, 2, 0)) == ("CABDFE", 15)


with open("07.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
