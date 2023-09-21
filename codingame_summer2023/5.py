def gear_balance(n_gears: int, connections: list[list[int]]) -> list[int]:
    G = {x: set() for x in range(n_gears)}
    for a, b in connections:
        G[a].add(b)
        G[b].add(a)

    R = {0: True}
    checked = set()

    while set(R) - checked:
        for x in set(R)-checked:
            clockwise = R[x]
            for next_gear in G[x]:
                if next_gear in R and R[next_gear] == clockwise:
                    return [-1, -1]
                R[next_gear] = not clockwise
            checked.add(x)

    return [sum(R.values()), len(R)-sum(R.values())]