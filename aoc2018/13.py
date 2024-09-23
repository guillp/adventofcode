from collections.abc import Iterator
from itertools import count


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

    first_crash = True
    for tick in count():
        #    for y in range(0, len(content.splitlines())):
        #       print("".join(
        #           carts[y,x][0] if (y,x) in carts else grid.get((x,y)," ")
        #           for x in range(len(content.splitlines()[0])))
        #       )
        #       print()

        for y, x in sorted(carts):
            if (y, x) not in carts:
                continue  # cart may have been removed due to collision
            direction, intersections = carts.pop((y, x))
            track = grid[x, y]

            if track == "+":
                track = {
                    "^": r"\|/",
                    "v": r"\|/",
                    ">": "/-\\",
                    "<": "/-\\",
                }[direction][intersections % 3]
                intersections += 1
            x, y, direction = {
                "|^": (x, y - 1, "^"),
                "|v": (x, y + 1, "v"),
                "->": (x + 1, y, ">"),
                "-<": (x - 1, y, "<"),
                "/^": (x + 1, y, ">"),
                "/<": (x, y + 1, "v"),
                "/>": (x, y - 1, "^"),
                "/v": (x - 1, y, "<"),
                r"\<": (x, y - 1, "^"),
                r"\>": (x, y + 1, "v"),
                r"\v": (x + 1, y, ">"),
                r"\^": (x - 1, y, "<"),
            }[f"{track}{direction}"]

            if (y, x) in carts:  # collision
                if first_crash:
                    yield f"{x},{y}"
                    first_crash = False
                del carts[(y, x)]
                if len(carts) == 1:
                    (y, x) = next(iter(carts))
                    yield f"{x},{y}"
                    return
            else:
                carts[y, x] = direction, intersections
    assert False


test_content = r"""/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
  """

assert next(solve(test_content)) == "7,3"

with open("13.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
