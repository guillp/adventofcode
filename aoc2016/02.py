def solve(content: str, *, part2: bool = False) -> str:
    if not part2:
        grid = {
            (-1, -1): "1",
            (0, -1): "2",
            (1, -1): "3",
            (-1, 0): "4",
            (0, 0): "5",
            (1, 0): "6",
            (-1, 1): "7",
            (0, 1): "8",
            (1, 1): "9",
        }
        x = y = 0
    else:
        grid = {
            (0, -2): "1",
            (-1, -1): "2",
            (0, -1): "3",
            (1, -1): "4",
            (-2, 0): "5",
            (-1, 0): "6",
            (0, 0): "7",
            (1, 0): "8",
            (2, 0): "9",
            (-1, 1): "A",
            (0, 1): "B",
            (1, 1): "C",
            (0, 2): "D",
        }
        x, y = -2, 0
    code = ""

    for line in content.splitlines():
        for c in line:
            match c:
                case "U":
                    if (x, y - 1) in grid:
                        y -= 1
                case "D":
                    if (x, y + 1) in grid:
                        y += 1
                case "L":
                    if (x - 1, y) in grid:
                        x -= 1
                case "R":
                    if (x + 1, y) in grid:
                        x += 1
        code += grid[x, y]

    return code


test_content = """\
ULL
RRDDD
LURDL
UUUUD
"""

assert solve(test_content) == "1985"
assert solve(test_content, part2=True) == "5DB3"


with open("02.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
