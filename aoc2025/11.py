from functools import cache


def solve(content: str) -> tuple[int, int]:
    graph = dict[str, list[str]]()
    for line in content.splitlines():
        source, dests = line.split(": ")
        graph[source] = dests.split(" ")

    @cache
    def nb_paths(source: str, target: str) -> int:
        return (source == target) + sum(nb_paths(node, target) for node in graph.get(source, []))

    part1 = nb_paths("you", "out")
    part2 = (  # fmt: skip
        nb_paths("svr", "dac") * nb_paths("dac", "fft") * nb_paths("fft", "out")
        + nb_paths("svr", "fft") * nb_paths("fft", "dac") * nb_paths("dac", "out")
    )
    return part1, part2


test_content1 = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

test_content2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

assert solve(test_content1) == (5, 0)
assert solve(test_content2) == (0, 2)

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
