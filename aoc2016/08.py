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


screen = {}

with open("08.txt") as f:
    content = f.read()

for instruction in content.splitlines():
    if instruction.startswith("rect"):
        a, b = (int(x) for x in instruction.split(" ")[1].split("x"))
        screen = rect(a, b, screen)
    elif instruction.startswith("rotate column"):
        a, b = (int(x) for x in instruction.split("=")[1].split(" by "))
        screen = rotate_column(a, b, screen)
    elif instruction.startswith("rotate row"):
        a, b = (int(x) for x in instruction.split("=")[1].split(" by "))
        screen = rotate_row(a, b, screen)


print(sum(screen.values()))
display(screen)
