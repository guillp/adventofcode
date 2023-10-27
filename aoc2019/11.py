import sys
from enum import Enum


with open("11.txt") as f:
    content = f.read()

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1


class OutputSignal(RuntimeError):
    def __init__(self, value: int):
        self.value = value


class ParamMode(str, Enum):
    POSITION = "0"
    IMMEDIATE = "1"
    RELATIVE = "2"


class Computer:
    def __init__(self, instructions: str, *inputs: int):
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

    def set_param(self, mode: ParamMode, value) -> None:
        dest = self.get_param(ParamMode.IMMEDIATE)
        if mode == ParamMode.POSITION:
            self.instructions[dest] = value
        elif mode == ParamMode.RELATIVE:
            self.instructions[dest + self.relative_base] = value
        else:
            assert False, f"Unknown mode {mode}"

    def get_instruction(self) -> tuple[str, tuple[str, ...]]:
        instruction = f"{self.instructions[self.pointer]:05d}"
        opcode = instruction[3:]
        modes = tuple(x for x in instruction[:3][::-1])
        self.pointer += 1
        # nb_params = {"01": 3, "02": 3, "03": 2, "04": 1, "05": 2, "06": 2, "07": 3, "08": 3, "09": 1}.get(opcode, 0)
        return opcode, modes

    def next(self):
        opcode, modes = self.get_instruction()
        if opcode == "99":  # quit
            raise StopIteration()
        if opcode == "01":  # add
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], left + right)
        elif opcode == "02":  # mult
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            self.set_param(modes[2], left * right)
        elif opcode == "03":  # store input
            value = self.inputs.pop(0)
            self.set_param(modes[0], value)
        elif opcode == "04":  # output
            value = self.get_param(modes[0])
            raise OutputSignal(value)
        elif opcode == "05":  # jump-if-true
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            if test != 0:
                self.pointer = dest
        elif opcode == "06":  # jump-if-false
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            if test == 0:
                self.pointer = dest
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
            self.relative_base += offset

    def run(self, i: int | None = None) -> int:
        if i is not None:
            self.inputs.append(i)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value

    def run_until_halt(self) -> list[int]:
        output = []
        while True:
            try:
                self.next()
            except OutputSignal as out:
                output.append(out.value)
            except StopIteration:
                return output

    def __repr__(self):
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


pos, heading = 0, 1j
hull = {}
computer = Computer(content)
while True:
    try:
        paint = computer.run(hull.get(pos, BLACK))
    except StopIteration:
        break
    hull[pos] = paint  # paint hull
    turn = computer.run()
    heading *= 1j if turn == 0 else -1j  # turn
    pos += heading  # move forward

print(len(hull))

pos, heading = 0, -1j
hull2 = {}
computer = Computer(content)
while True:
    try:
        paint = computer.run(hull2.get(pos, WHITE))
    except StopIteration:
        break
    hull2[pos] = paint  # paint hull
    turn = computer.run()
    heading *= 1j if turn == RIGHT else -1j  # turn
    pos += heading  # move forward

x_min = min(int(pos.real) for pos in hull2)
x_max = max(int(pos.real) for pos in hull2)
y_min = min(int(pos.imag) for pos in hull2)
y_max = max(int(pos.imag) for pos in hull2)

for y in range(y_min, y_max + 1):
    print(
        " ".join(
            " " if hull2.get(complex(x, y), BLACK) == BLACK else "#"
            for x in range(x_min, x_max + 1)
        )
    )
