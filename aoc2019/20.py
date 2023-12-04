with open("20.txt") as f: content = f.read()

paths = {
    complex(x, y)
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
    if c == "."
}

portal_labels = {
    complex(x, y): c
    for y, line in enumerate(content.splitlines())
    for x, c in enumerate(line)
    if c.isalpha()
}

portal_cache = {}
portal_map = {}

for pos, letter in portal_labels.items():
    for d in (1, -1, 1j, -1j):
        if pos + d in paths:  # there is an adjacent path
            other_letter = portal_labels[pos - d]  # the other letter is opposite to the path
            label = f"{other_letter}{letter}" if d in (1, 1j) else f"{letter}{other_letter}"  # read the label
            if label == "AA":
                start = pos + d
            elif label == "ZZ":
                stop = pos + d
            else:
                if label in portal_cache:
                    orig, dest = portal_cache[label]
                    portal_map[pos] = dest
                    portal_map[orig] = pos + d
                else:
                    portal_cache[label] = pos, pos + d

pool = [(start,)]
best_path = tuple(paths)

while pool:
    pool.sort(key=len)
    path = pool.pop()
    if len(path) >= len(best_path):
        continue

    current_pos = path[-1]
    for d in (1, -1, 1j, -1j):
        next_pos = current_pos + d
        if next_pos in portal_map:  # walking through portal
            next_pos = portal_map[next_pos]
        if next_pos not in paths:
            continue  # avoid stepping outside of open passages
        if next_pos in path:
            continue  # avoid loops
        next_path = path + (next_pos,)
        if next_pos == stop:
            if len(next_path) < len(best_path):
                best_path = next_path
                #print("found possible path", len(next_path), next_path)
        else:
            pool.append(next_path)

lines = content.replace("#", "*").splitlines()
for y in range(len(lines)):
    print(
        "".join(
            str(best_path.index(complex(x, y)) % 10) if complex(x, y) in best_path else lines[y][x]
            for x in range(len(lines[y])))
    )
print(len(best_path) - 1)