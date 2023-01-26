n = int(input())
m = int(input())
squads = [int(input()) for _ in range(m)]

target = (n + sum(squads)) // 2 - n + 1

def hire(squads: list[int], target: int) -> int:
    totals = {0}
    for squad in squads:
        for total in tuple(totals):
            totals.add(total + squad)

    return min(total for total in totals if total >= target)


print(hire(squads, target))
