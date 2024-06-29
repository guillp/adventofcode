def solve(content: str) -> tuple[str, int]:
    lines = content.splitlines()
    W = len(lines[0])
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != " "}
    start_pos = next(complex(x, 0) for x in range(W) if complex(x, 0) in grid)
    d = 1j
    path: tuple[complex, ...] = (start_pos,)
    letters = ""
    while True:
        current_pos = path[-1]
        next_pos = current_pos + d
        match grid.get(next_pos):
            case None:
                return letters, len(path)
            case "|" | "-":
                pass
            case "+":
                match next_pos + d * 1j in grid, next_pos + d * -1j in grid:
                    case True, False:
                        d = d * 1j
                    case False, True:
                        d = d * -1j
                    case _:  # either can turn to both directions, or to no directions
                        assert False
            case _ as c if c.isalpha():
                letters += c
        path += (next_pos,)


assert solve("""\
     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

""") == ("ABCDEF", 38)

with open("19.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
