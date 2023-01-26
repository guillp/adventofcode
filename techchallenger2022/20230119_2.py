n = int(input())
m = int(input())
squads = [int(input()) for _ in range(m)]

target = (n + sum(squads)) // 2 - n + 1


# def hire(squads: list[int], target: int, i: int = 0, total: int= 0) -> tuple[int, ...]:
#     if total == target:
#         return total
#     if total >= target:
#         yield total
#     elif i < len(squads):
#         yield from hire(squads, target, i + 1, total+squads[i])
#         yield from hire(squads, target, i + 1, total)


def hire(squads: list[int], target: int) -> int:
    totals = {0}
    for squad in squads:
        for total in tuple(totals):
            totals.add(total + squad)

    return min(total for total in totals if total >= target)


squads.sort()
best_groups = hire(squads, target)
print(best_groups)
