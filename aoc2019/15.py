from collections.abc import Iterator
from enum import Enum


class OutputSignal(RuntimeError):
    def __init__(self, value: int) -> None:
        self.value = value


class ParamMode(str, Enum):
    POSITION = "0"
    IMMEDIATE = "1"
    RELATIVE = "2"


class Computer:
    def __init__(self, instructions: str, *inputs: int) -> None:
        self.instructions = {i: int(x) for i, x in enumerate(instructions.split(","))}
        self.pointer = 0
        self.relative_base = 0
        self.inputs = list(inputs)

    def get_param(self, mode: ParamMode) -> int:
        value = self.instructions[self.pointer]
        self.pointer += 1
        if mode == ParamMode.IMMEDIATE:
            return value
        elif mode == ParamMode.POSITION:
            return self.instructions.get(value, 0)
        elif mode == ParamMode.RELATIVE:
            return self.instructions[self.relative_base + value]
        assert False, f"Unknown mode {mode}"

    def set_param(self, mode: ParamMode, value: int) -> None:
        dest = self.get_param(ParamMode.IMMEDIATE)
        if mode == ParamMode.POSITION:
            self.instructions[dest] = value
        elif mode == ParamMode.RELATIVE:
            self.instructions[dest + self.relative_base] = value
        else:
            assert False, f"Unknown mode {mode}"

    def jump(self, target: int, condition: bool = True) -> None:
        if condition:
            self.pointer = target

    def offset_relative_base(self, offset: int) -> None:
        self.relative_base += offset

    def output(self, value: int) -> None:
        raise OutputSignal(value)

    def stop(self) -> None:
        raise StopIteration()

    def get_instruction(self) -> tuple[int, str, tuple[ParamMode, ...]]:
        pointer = self.pointer
        instruction = f"{self.instructions[pointer]:05d}"
        assert not instruction.startswith("-")
        opcode = instruction[3:]
        modes = tuple(ParamMode(x) for x in instruction[:3][::-1])
        self.pointer += 1
        assert "-" not in modes
        return pointer, opcode, modes

    def next(self) -> None:
        _, opcode, modes = self.get_instruction()
        if opcode == "99":  # quit
            self.stop()
        elif opcode == "01":  # add
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], left + right)
        elif opcode == "02":  # mult
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], left * right)
        elif opcode == "03":  # get input
            value = self.inputs.pop(0) if self.inputs else 0
            self.set_param(modes[0], value)
        elif opcode == "04":  # output
            value = self.get_param(modes[0])
            self.output(value)
        elif opcode == "05":  # jump-if-true
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            self.jump(dest, test != 0)
        elif opcode == "06":  # jump-if-false
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            self.jump(dest, test == 0)
        elif opcode == "07":  # less than
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], 1 if left < right else 0)
        elif opcode == "08":  # equals
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], 1 if left == right else 0)
        elif opcode == "09":  # relative base offset
            offset = self.get_param(modes[0])
            self.offset_relative_base(offset)
        else:
            assert False, f"Unknown opcode {opcode}"

    def run(self, i: int | None = None) -> int:
        if i is not None:
            self.inputs.append(i)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value

    def run_until_halt(self, i: int | None = None) -> list[int]:
        if i:
            self.inputs.append(i)
        output = []
        while True:
            try:
                self.next()
            except OutputSignal as out:
                output.append(out.value)
            except StopIteration:
                return output

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


EMPTY = "."
WALL = "#"
DROID = "D"
OXYGEN = "O"
UNKNOWN = "?"

NORTH = -1j
SOUTH = 1j
EAST = 1
WEST = -1

MOVE_NORTH = 1
MOVE_SOUTH = 2
MOVE_WEST = 3
MOVE_EAST = 4

HIT_WALL = 0
MOVED = 1
FOUND_OXYGEN = 2


def print_grid(grid: dict[complex, str], pos: complex) -> None:
    x_min = int(min(p.real for p in grid))
    x_max = int(max(p.real for p in grid))
    y_min = int(min(p.imag for p in grid))
    y_max = int(max(p.imag for p in grid))

    for y in range(y_min, y_max + 1):
        print(
            "".join(
                grid.get(complex(x, y), UNKNOWN) if not x == y == 0 else DROID if complex(x, y) == pos else "@"
                for x in range(x_min, x_max + 1)
            )
        )


def solve(content: str) -> Iterator[int]:
    computer = Computer(content)
    grid: dict[complex, str] = {0: EMPTY}

    pos = 0j
    path: tuple[complex, ...] = (0j,)
    best_path: list[complex] | None = None
    while True:
        # explore unknown directions
        for direction in (NORTH, EAST, SOUTH, WEST):
            if grid.get(pos + direction) is None:
                output = computer.run(
                    {
                        NORTH: MOVE_NORTH,
                        SOUTH: MOVE_SOUTH,
                        WEST: MOVE_WEST,
                        EAST: MOVE_EAST,
                    }[direction]
                )
                if output == HIT_WALL:
                    grid[pos + direction] = WALL
                else:
                    grid[pos + direction] = {MOVED: EMPTY, FOUND_OXYGEN: OXYGEN}[output]
                    pos += direction
                    path += (pos,)
                    if output == FOUND_OXYGEN and (best_path is None or len(path) < len(best_path)):
                        best_path = list(path)
                break

        else:
            # if no adjacent area to explore, backtrack to previous location
            if len(path) == 1:
                break
            last_step = path[-1] - (path[-2] if path else 0)
            path = path[:-1]
            output = computer.run({NORTH: MOVE_SOUTH, SOUTH: MOVE_NORTH, EAST: MOVE_WEST, WEST: MOVE_EAST}[last_step])
            assert output == MOVED
            pos -= last_step

    # print_grid(grid, pos)
    oxygen_location = next(p for p, v in grid.items() if v == OXYGEN)

    assert best_path is not None, "Best track not found!"
    # try to enhance the best path (not necessary in my case since there is a single path)
    pool: list[tuple[complex, ...]] = [(0,)]
    while pool:
        pool.sort(key=len)
        path = pool.pop()
        pos = path[-1]

        if len(path) >= len(best_path):
            continue

        for direction in (NORTH, SOUTH, EAST, WEST):
            if grid[pos + direction] == WALL or pos + direction in path:
                continue
            elif grid[pos + direction] == OXYGEN:
                if len(path) + 2 < len(best_path):
                    best_path = list(path + (pos + direction,))
                    print(len(best_path))
            else:
                pool.append(path + (pos + direction,))

    yield len(best_path) - 1

    # Flood fill the grid
    oxygen = {oxygen_location}
    part2 = 0
    while EMPTY in grid.values():
        new_oxygen = set()
        for o in oxygen:
            for direction in (NORTH, SOUTH, EAST, WEST):
                if grid[o + direction] == EMPTY:
                    grid[o + direction] = OXYGEN
                    new_oxygen.add(o + direction)
        part2 += 1
        oxygen = new_oxygen

    yield part2


with open("15.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
