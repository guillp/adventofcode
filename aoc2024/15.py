def part1(content: str, *, debug: bool = False) -> int:
    map_part, movements_part = content.strip().split("\n\n")
    grid = {complex(x, y): c for y, line in enumerate(map_part.splitlines()) for x, c in enumerate(line)}
    robot = next(pos for pos, c in grid.items() if c == "@")

    for movement in "".join(movements_part.splitlines()):
        direction = {">": 1, "<": -1, "^": -1j, "v": 1j}[movement]
        pushed_boxes = 0
        while grid.get(robot + (pushed_boxes + 1) * direction) == "O":
            pushed_boxes += 1
        if grid[robot + direction + pushed_boxes * direction] == "#":
            continue

        grid[robot] = "."
        robot += direction
        grid[robot] = "@"
        for i in range(pushed_boxes):
            grid[robot + (i + 1) * direction] = "O"

        if debug:
            print("after movement", movement)
            for y in range(len(lines := map_part.splitlines())):
                print("".join(grid[complex(x, y)] for x in range(len(lines[0]))))
            print()

    return int(sum(100 * pos.imag + pos.real for pos, c in grid.items() if c == "O"))


def part2(content: str, *, debug: bool = False) -> int:
    map_part, movements_part = content.strip().split("\n\n")
    grid = {
        complex(x, y): c
        for y, line in enumerate(
            map_part.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.").splitlines(),
        )
        for x, c in enumerate(line)
    }
    robot = next(pos for pos, c in grid.items() if c == "@")

    for movement in "".join(movements_part.splitlines()):
        direction = {">": 1, "<": -1, "^": -1j, "v": 1j}[movement]
        pushes = set()
        new_pushes = {robot}
        while new_pushes:
            push = new_pushes.pop()
            pushes.add(push)
            match grid.get(push + direction):
                case "#":
                    break
                case "[" if push + direction not in pushes:
                    new_pushes |= {push + direction, push + direction + 1}
                case "]" if push + direction not in pushes:
                    new_pushes |= {push + direction, push + direction - 1}
        else:
            for push in sorted(pushes, key=lambda c: (c.real, c.imag) if movement in "<^" else (-c.real, -c.imag)):
                grid[push + direction] = grid[push]
                grid[push] = "."
            grid[robot] = "."
            robot += direction
            grid[robot] = "@"

        if debug:
            print("after movement", movement)
            for y in range(len(lines := map_part.splitlines())):
                print("".join(grid[complex(x, y)] for x in range(len(lines[0]) * 2)))
            print()

    return int(sum(100 * pos.imag + pos.real for pos, c in grid.items() if c == "["))


test_content = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

test_content2 = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

assert part1(test_content) == 2028
assert part1(test_content2) == 10092

test_content3 = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

part2(test_content3)
assert part2(test_content2) == 9021

with open("15.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
