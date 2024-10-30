from collections import defaultdict


def solve(content: str, *, part2: bool = False) -> int:
    graph = defaultdict(set)
    for line in content.strip().splitlines():
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)
    pool: list[tuple[str, ...]] = [("start",)]
    paths = set()
    while pool:
        path = pool.pop()
        current_cave = path[-1]
        for next_cave in graph.get(current_cave, ()):
            if next_cave == "end":
                paths.add((*path, next_cave))
                continue
            if next_cave in path and next_cave.islower():
                if part2:
                    if next_cave in ("start", "end") or any(path.count(cave) == 2 for cave in path if cave.islower()):
                        continue
                else:
                    continue
            pool.append((*path, next_cave))

    return len(paths)


assert (
    solve("""\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""")
    == 19
)

assert (
    solve(
        """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""",
        part2=True,
    )
    == 36
)

with open("12.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
