import sys

n = int(input())
m = int(input())
squads = [int(input()) for _ in range(m)]


def hire(n: int, squads: list[int]) -> tuple[int, tuple[int, ...]]:
    possible_hires: dict[int, tuple[int, ...]] = {0: ()}
    for squad in squads:
        for total, hired in list(possible_hires.items()):
            possible_hires[total + squad] = hired + (squad,)

    target = (n + sum(squads)) // 2 - n + 1
    while target not in possible_hires:
        target += 1

    return target, possible_hires[target]


total, hired = hire(n, squads)
print(total)
print(hired, file=sys.stderr)
