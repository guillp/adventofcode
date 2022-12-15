from collections import defaultdict

with open("19.txt", "rt") as finput:
    content = finput.read()

replacements, molecule = content.strip().split("\n\n")

transformations = defaultdict(set)
for line in replacements.splitlines():
    a, b = line.split(" => ")
    transformations[a].add(b)

possibles = set()


def transform(molecule: str):
    for char, targets in transformations.items():
        parts = molecule.split(char)
        if len(parts) > 1:
            for i in range(1, len(parts)):
                for target in targets:
                    yield char.join(parts[:i]) + target + char.join(parts[i:])


all_molecules = set(transform(molecule))
print(len(all_molecules))


reverse_transformations = {
    target: origin for origin, targets in transformations.items() for target in targets
}


def reverse(molecule: str):
    for target, previous in reverse_transformations.items():
        parts = molecule.split(target)
        if len(parts) > 1:
            for i in range(1, len(parts)):
                yield target.join(parts[:i]) + previous + target.join(parts[i:])


s = 10**10
pool = {(0, molecule)}
while pool:
    n, mol = max(pool, key=lambda x: (x[0], -len(x[1])))
    pool.remove((n, mol))
    if n >= s - 1:
        continue
    for prev in reverse(mol):
        if prev == "e":
            s = n + 1
            print(s)
        else:
            pool.add((n + 1, prev))

print(s)
