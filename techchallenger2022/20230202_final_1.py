import itertools

n = int(input())
conds = [tuple((c, int(i) - 1) for c, i in input().split()) for _ in range(n)]  # type: ignore[misc, has-type]


pool = set(itertools.product("RVB", repeat=5))

for i, ((x, X), (y, Y), (z, Z)) in enumerate(conds):
    for lights in list(pool):
        if lights[X] == x or lights[Y] == y or lights[Z] == z:
            continue
        pool.remove(lights)

    if not pool:
        print(i)
        break
else:
    print(i + 1)
