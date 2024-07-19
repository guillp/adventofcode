from collections.abc import Iterator
from enum import Enum


class OutputSignal(RuntimeError):
    def __init__(self, value: int) -> None:
        self.value = value


class InputSignal(RuntimeError):
    pass


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
            return self.instructions.get(self.relative_base + value, 0)
        assert False, f"Unknown mode {mode}"

    def set_param(self, mode: ParamMode, value: int) -> None:
        dest = self.get_param(ParamMode.IMMEDIATE)
        if mode == ParamMode.RELATIVE:
            dest += self.relative_base
        elif mode != ParamMode.POSITION:
            assert False, f"Unknown mode {mode}"
        self.instructions[dest] = value

    def jump(self, target: int, condition: bool = True) -> None:
        if condition:
            self.pointer = target

    def offset_relative_base(self, offset: int) -> None:
        self.relative_base += offset

    def output(self, value: int) -> None:
        raise OutputSignal(value)

    def stop(self) -> None:
        raise StopIteration()

    def get_instruction(self) -> tuple[int, str, tuple[str, ...]]:
        pointer = self.pointer
        instruction = f"{self.instructions[pointer]:05d}"
        assert not instruction.startswith("-")
        opcode = instruction[3:]
        modes = tuple(x for x in instruction[:3][::-1])
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
            if not self.inputs:
                raise InputSignal()
            value = self.inputs.pop(0)
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

    def run(self, *i: int) -> int | None:
        self.inputs.extend(i)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value
        except InputSignal:
            return None

    def run_until_halt(self, *inputs: int) -> list[int]:
        self.inputs.extend(inputs)
        output = []
        while True:
            try:
                self.next()
            except OutputSignal as out:
                output.append(out.value)
            except StopIteration:
                return output
            except InputSignal:
                return output

    def run_until_input(self, *i: int) -> list[int]:
        self.inputs.extend(i)

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


def solve(content: str) -> Iterator[int]:
    computer = Computer(content)

    output = computer.run_until_halt()

    img = bytes(output).decode().strip()
    # print(img)
    lines = img.splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "."}

    intersections = set()

    UP = -1j
    DOWN = 1j
    LEFT = -1
    RIGHT = 1

    s = 0
    for pos in grid:
        if all(grid.get(pos + d) == "#" for d in (UP, DOWN, RIGHT, LEFT)):
            s += int(pos.real) * int(pos.imag)
            intersections.add(pos)

    yield s

    TURN_RIGHT = "R"
    TURN_LEFT = "L"

    def dfs() -> tuple[str | int]:
        positions = next(p for p, c in grid.items() if c in "^v<>")
        directions = {"^": UP, "v": DOWN, ">": RIGHT, "<": LEFT}.get(grid[positions])
        pool = [(positions, directions, set(grid) - {positions}, ())]
        while pool:
            pool.sort(key=lambda x: len(x[2]))
            positions, directions, remaining, path = pool.pop()
            if remaining:
                for action, turn in {TURN_RIGHT: 1j, TURN_LEFT: -1j}.items():
                    if grid.get(positions + turn * directions) == "#" and positions + turn * directions in remaining:
                        pool.append((positions, turn * directions, remaining, path + (action,)))

                steps = 0
                new_remaining = set(remaining)
                while grid.get(positions + steps * directions + directions) == "#":
                    steps += 1
                    new_remaining -= {positions + steps * directions}
                    if grid[positions + steps * directions] in intersections:
                        pool.append(
                            (
                                positions + steps * directions,
                                directions,
                                new_remaining,
                                path + (steps,),
                            )
                        )
                if steps > 0:
                    pool.append(
                        (
                            positions + steps * directions,
                            directions,
                            new_remaining,
                            path + (steps,),
                        )
                    )
            else:
                return path

    path = ",".join(str(x) for x in dfs())
    print(path)
    # MANUALLY INSPECT FOR REPEATING FUNCTIONS

    A = "R,10,R,8,L,10,L,10"
    B = "R,8,L,6,L,6"
    C = "L,10,R,10,L,6"

    main = "A,B,B,A,C,B,C,C,B,A"

    instructions = f"{main}\n{A}\n{B}\n{C}\nn\n"
    # print(instructions)
    inputs = [ord(c) for c in instructions]
    computer2 = Computer(content)
    computer2.instructions[0] = 2

    output = computer2.run_until_halt(*inputs)
    yield output[-1]


with open("17.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
