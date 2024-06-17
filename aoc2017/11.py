def solve(content: str) -> tuple[int, int]:
    x = y = furthest = 0
    for step in content.strip().split(","):
        match step:
            case "n":
                y -= 1
            case "ne":
                x += 1
                y -= 1
            case "se":
                x += 1
                y += 1
            case "s":
                y += 1
            case "sw":
                x -= 1
                y += 1
            case "nw":
                x -= 1
                y -= 1
        distance = max(
            abs(x),
            -(-abs(y) // 2),
            abs(x) - abs(y),
        )
        furthest = max(furthest, distance)

    return distance, furthest


assert solve("ne,ne,ne") == (3, 3)
assert solve("ne,ne,sw,sw") == (0, 2)
assert solve("ne,ne,s,s") == (2, 2)
assert solve("se,sw,se,sw,sw") == (3, 3)

with open("11.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
