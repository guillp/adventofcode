from collections import defaultdict
from collections.abc import Iterator
from enum import Enum
from itertools import product


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
            return self.instructions.setdefault(self.relative_base + value, 0)
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

    def run(self, *inputs: int) -> int:
        self.inputs.extend(inputs)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value
        except StopIteration as out:
            assert isinstance(out.value, int)
            return out.value

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

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


PULLED = 1


def solve(content: str) -> Iterator[int]:
    pulled = set()
    for x, y in product(range(50), repeat=2):
        computer = Computer(content)
        if computer.run(x, y) == PULLED:
            pulled.add((x, y))

    yield len(pulled)

    # the tractor beam is delimited by 2 lines passing by origin
    # get the 2 quotients that define the line slopes
    low = min(y / x for x, y in pulled if x > 0)
    high = max(y / x for x, y in pulled if x > 0)

    # TODO: some trigonometry to delimit the area to search for such a diagonal

    def search() -> set[tuple[int, int]]:
        x = 50
        s = defaultdict(set)
        while True:
            for y in range(int(low * x - 2), int(high * x + 3)):
                computer = Computer(content)
                if computer.run(x, y) == PULLED:
                    pulled.add((x, y))
                    s[x + y].add((x, y))
                    if len(s[x + y]) == 100:
                        return s[x + y]
            x += 1

    diagonal = search()
    xmin = min(x for x, y in diagonal)

    ymin = min(y for x, y in diagonal)
    yield xmin * 10000 + ymin

    # xmax = xmin + 100
    # ymax = ymin + 100
    # for y in range(ymin - 50, ymax + 50):
    #     print(
    #         "".join(
    #             "X" if (x, y) in diagonal else "#" if (x, y) in pulled else "." for x in range(xmin - 50, xmax + 50)
    #         )
    #     )


with open("19.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
