from collections.abc import Iterator

test_content = r"""/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
  """


def solve(content: str) -> Iterator[str]:
    grid = {(x, y): c for y, line in enumerate(content.splitlines()) for x, c in enumerate(line)}
    carts = {}
    for (x, y), c in grid.items():
        if c in "><":
            grid[x, y] = "-"
            carts[y, x] = c, 0
        elif c in "v^":
            grid[x, y] = "|"
            carts[y, x] = c, 0

        # for tick in count():
        #    for y in range(0, len(content.splitlines())):
        #       print("".join(carts[y,x][0] if (y,x) in carts else grid.get((x,y)," ") for x in range(len(content.splitlines()[0]))))
        #       print()

        for y, x in sorted(carts):
            if (y, x) not in carts:
                continue  # cart may have been removed due to collision
            direction, intersections = carts.pop((y, x))
            track = grid[x, y]

            if track == "+":
                track = {"^": "\\|/", "v": "\\|/", ">": "/-\\", "<": "/-\\"}[direction][intersections % 3]
                intersections += 1
            match track, direction:
                case "|", "^":
                    y -= 1
                case "|", "v":
                    y += 1
                case "-", ">":
                    x += 1
                case "-", "<":
                    x -= 1
                case "/", "^":
                    x += 1
                    direction = ">"
                case "/", "<":
                    y += 1
                    direction = "v"
                case "/", ">":
                    y -= 1
                    direction = "^"
                case "/", "v":
                    x -= 1
                    direction = "<"
                case "\\", ">":
                    y += 1
                    direction = "v"
                case "\\", "<":
                    y -= 1
                    direction = "^"
                case "\\", "v":
                    x += 1
                    direction = ">"
                case "\\", "^":
                    x -= 1
                    direction = "<"
                case _:
                    assert False

            if (y, x) in carts:  # collision
                yield f"{x},{y}"
                del carts[(y, x)]
                if len(carts) == 0:
                    return
                if len(carts) == 1:
                    (y, x) = tuple(carts)[0]
                    yield f"{x},{y}"
            else:
                carts[y, x] = direction, intersections
    assert False


# assert next(solve(test_content)) == "7,3"

with open("13.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
