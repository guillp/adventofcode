from enum import Enum


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

    def next(self):
        pointer, opcode, modes = self.get_instruction()
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

    def __repr__(self):
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


def part1(content: str) -> int:
    computer = Computer(content)

    output = computer.run_until_halt()
    assert len(output) % 3 == 0

    screen = {}
    for i in range(0, len(output), 3):
        x, y, z = output[i : i + 3]
        screen[int(x), int(y)] = z
    return sum(v == 2 for v in screen.values())


def part2(content: str) -> int:
    # let's add some walls all around the paddle
    content_cheated = content.replace(
        "1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1",
        "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
    )
    computer = Computer(content_cheated)
    computer.instructions[0] = 2
    output = computer.run_until_halt(0)
    screen = {}
    for i in range(0, len(output), 3):
        x, y, z = output[i : i + 3]
        screen[x, y] = z
    return screen.pop((-1, 0))


with open("13.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
