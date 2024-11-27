def solve(content: str, *, part2: bool = False) -> int:
    stack = dict[int, list[int]]()
    initial_numbers = tuple(int(x) for x in content.split(","))
    for i, x in enumerate(initial_numbers):
        stack.setdefault(x, []).append(i+1)

    latest = initial_numbers[-1]
    for i in range(len(initial_numbers)+1, 30000001 if part2 else 2021):
        if len(stack[latest]) == 1:
            latest = 0
        else:
            latest = stack[latest][-1] - stack[latest][-2]
        stack.setdefault(latest, []).append(i)
    return latest

assert solve("0,3,6") == 436
assert solve("1,3,2") == 1
assert solve("2,1,3") == 10
assert solve("1,2,3") == 27
assert solve("2,3,1") == 78

content = "0,13,1,8,6,15"
print(solve(content))
print(solve(content, part2=True))