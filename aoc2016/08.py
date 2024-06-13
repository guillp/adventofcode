from collections import deque

Screen = dict[tuple[int, int], bool]

WIDTH = 50
HEIGHT = 6


def rect(width: int, height: int, screen: Screen) -> Screen:
    screen = screen.copy()
    for x in range(width):
        for y in range(height):
            screen[x, y] = True

    return screen


def rotate_row(row: int, shift: int, screen: Screen) -> Screen:
    screen = screen.copy()
    queue = deque([screen.get((x, row), False) for x in range(WIDTH)])
    queue.rotate(shift)
    for x in range(WIDTH):
        screen[x, row] = queue.popleft()
    return screen


def rotate_column(column: int, shift: int, screen: Screen) -> Screen:
    screen = screen.copy()
    queue = deque([screen.get((column, y), False) for y in range(HEIGHT)])
    queue.rotate(shift)
    for y in range(HEIGHT):
        screen[column, y] = queue.popleft()
    return screen


def display(screen: Screen) -> None:
    for y in range(HEIGHT):
        print("".join("#" if screen.get((x, y), False) else "." for x in range(WIDTH)))


def solve(content: str) -> tuple[int, Screen]:
    screen: Screen = {}
    for instruction in content.splitlines():
        match instruction.split():
            case "rect", ab:
                a, b = map(int, ab.split("x"))
                screen = rect(a, b, screen)
            case "rotate", "column", y, "by", b:
                a = int(y.split("=")[1])
                screen = rotate_column(a, int(b), screen)
            case "rotate", "row", x, "by", b:
                a = int(x.split("=")[1])
                screen = rotate_row(a, int(b), screen)
    return sum(screen.values()), screen


with open("08.txt") as f:
    content = f.read()

part1, part2 = solve(content)
print(part1)
display(part2)
