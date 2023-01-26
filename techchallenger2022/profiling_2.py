# run with $ python -m cProfile profiling_2.py

# results on my device:
#          37153 function calls in 0.194 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.194    0.194 {built-in method builtins.exec}
#         1    0.000    0.000    0.194    0.194 profiling_2.py:1(<module>)
#         1    0.186    0.186    0.186    0.186 profiling_2.py:47(remi)
#         1    0.006    0.006    0.009    0.009 profiling_2.py:64(guillaume)
#     35652    0.002    0.000    0.002    0.000 {method 'add' of 'set' objects}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.min}
#      1492    0.000    0.000    0.000    0.000 profiling_2.py:72(<genexpr>)
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.sum}
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.max}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


n = 1000
squads = [
    931,
    930,
    933,
    931,
    929,
    928,
    927,
    931,
    925,
    928,
    933,
    923,
    932,
    933,
    926,
    930,
    933,
    927,
    927,
    932,
    930,
    928,
    928,
    932,
    923,
    929,
    933,
    930,
    923,
    925,
    926,
    926,
    931,
    925,
    923,
    927,
    926,
    932,
    930,
    926,
]
resp = 18517


def remi():
    total = sum(squads)

    can_reach = [False] * (total + 1)
    can_reach[0] = True

    for m in squads:
        for i in range(total, 0, -1):
            if i - m >= 0 and can_reach[i - m]:
                can_reach[i] = True

    seuil = max((total - n) // 2 + 1, 0)
    for i in range(seuil, total + 1):
        if can_reach[i]:
            return i


def guillaume():
    target = (n + sum(squads)) // 2 - n

    totals = {0}
    for squad in squads:
        for total in tuple(totals):
            totals.add(total + squad)

    return min(total for total in totals if total > target)


assert remi() == guillaume() == resp
