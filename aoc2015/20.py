def solve(target: int = 34000000) -> tuple[int, int]:
    houses = [0] * target
    for i in range(1, target // 10 + 1):
        for j in range(i, target // 10 + 1, i):
            houses[j] += i * 10
        if houses[i] >= target:
            part1 = i
            break

    houses = [0] * target
    for i in range(1, target // 10 + 1):
        for j in range(i, min(i * 50, target), i):
            try:
                houses[j] += i * 11
            except IndexError:
                print("IndexError", j)
        if houses[i] >= target:
            part2 = i
            break

    return part1, part2


TARGET = 34000000

for part in solve(TARGET):
    print(part)
