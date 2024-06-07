from collections import defaultdict
from collections.abc import Iterable, Iterator


def solve(content: str) -> Iterable[int]:
    replacements, molecule = content.strip().split("\n\n")

    transformations = defaultdict(set)
    for line in replacements.splitlines():
        a, b = line.split(" => ")
        transformations[a].add(b)

    def transform(molecule: str) -> Iterator[str]:
        for char, targets in transformations.items():
            parts = molecule.split(char)
            if len(parts) > 1:
                for i in range(1, len(parts)):
                    for target in targets:
                        yield char.join(parts[:i]) + target + char.join(parts[i:])

    yield len(set(transform(molecule)))

    reverse_transformations = {target: origin for origin, targets in transformations.items() for target in targets}

    def reverse(molecule: str) -> Iterator[str]:
        for target, previous in reverse_transformations.items():
            parts = molecule.split(target)
            if len(parts) > 1:
                for i in range(1, len(parts)):
                    yield target.join(parts[:i]) + previous + target.join(parts[i:])

    pool = {(0, molecule)}
    while pool:
        n, mol = max(pool, key=lambda x: (x[0], -len(x[1])))
        pool.remove((n, mol))
        for prev in reverse(mol):
            if prev == "e":
                yield n + 1
                return  # there is only 1 solution
            else:
                pool.add((n + 1, prev))


with open("19.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
