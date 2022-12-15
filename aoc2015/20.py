TARGET = 34000000

houses = [0] * TARGET
for i in range(1, TARGET // 10 + 1):
    for j in range(i, TARGET // 10 + 1, i):
        houses[j] += i * 10
    if houses[i] >= TARGET:
        print(i, houses[i], houses[i] - TARGET)
        break

houses = [0] * TARGET
for i in range(1, TARGET // 10 + 1):
    for j in range(i, min(i * 50, TARGET), i):
        try:
            houses[j] += i * 11
        except IndexError:
            print("IndexError", j)
    if houses[i] >= TARGET:
        print(i, houses[i], houses[i] - TARGET)
        break
