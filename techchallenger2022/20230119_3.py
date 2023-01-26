from collections import defaultdict

X, Y = (int(x) for x in input().split())
urdl = input()


def solve(X: int, Y: int, urdl: str) -> int | None:
    if X == 0 and Y == 0:
        return 0

    diffs = {0: (0, 0)}

    # calc the position after each step of the pattern
    for i, c in enumerate(urdl, start=1):
        x, y = diffs[i - 1]
        if c == "R":
            x += 1
        elif c == "L":
            x -= 1
        elif c == "U":
            y += 1
        elif c == "D":
            y -= 1

        # if target is reached on first pattern
        if (x, y) == (X, Y):
            return i

        diffs[i] = (x, y)

    # offset from a whole pattern
    dx, dy = (x, y)

    revs = defaultdict(set)
    for i, xy in diffs.items():
        revs[xy].add(i)

    # avoid cases where it is impossible to reach target
    if dx >= 0 > X or dy >= 0 > Y or dx <= 0 < X or dy <= 0 < Y:
        return

    # for each step of the pattern, check how many more whole loops are needed to reach the target
    for i, (x, y) in diffs.items():
        divx, modx = divmod(X - x, dx)
        divy, mody = divmod(Y - y, dy)
        if modx == mody == 0 and divx == divy:
            N = divx
            # if the pattern creates loops, it may visit the target before the last pattern is finished
            if (x + dx, y + dy) in revs:
                return (N - 1) * len(urdl) + min(revs[x + dx, y + dy])
            # otherwise we need N loops plus i steps of the pattern
            return N * len(urdl) + i


n = solve(X, Y, urdl)
print(n if n is not None else "not possible")
