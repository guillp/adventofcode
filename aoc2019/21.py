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

    def add_input(self, *inputs: int) -> None:
        self.waiting_for_input = False
        self.inputs.extend(inputs)

    def add_ascii_input(self, text: str) -> None:
        self.add_input(*map(ord, text))

    def get_input(self) -> int:
        if self.inputs:
            return self.inputs.pop(0)
        self.waiting_for_input = True
        return -1

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
            value = self.get_input()
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
        self.add_input(*inputs)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value
        except StopIteration as out:
            return out.value

    def next_output(self) -> int | None:
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value
        else:
            return None

    def run_until_halt(self, *inputs: int) -> list[int]:
        self.add_input(*inputs)
        output = []
        while True:
            try:
                self.next()
            except OutputSignal as out:
                output.append(out.value)
            except StopIteration:
                return output

    def run_until_prompt(self, prompt: str) -> str:
        history = ""
        while True:
            c = self.next_output()
            history += chr(c)
            if history.endswith(prompt):
                return history

    def run_until_big_int(self) -> str:
        history = ""
        while True:
            try:
                c = self.next_output()
                if c > 128:
                    return c
                else:
                    history += chr(c)
            except StopIteration:
                return history

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


def part1(content: str) -> int:
    computer = Computer(content)
    computer.run_until_prompt("Input instructions:")
    computer.add_ascii_input("""\
NOT C J
AND D J
NOT B T
AND D T
OR T J
NOT A T
AND D T
OR T J
WALK
""")
    return computer.run_until_big_int()


def part2(content: str) -> int:
    computer = Computer(content)
    computer.run_until_prompt("Input instructions:")
    computer.add_ascii_input("""\
NOT A J
NOT B T
AND D T
OR T J
NOT C T
AND D T
AND H T
OR T J
RUN
""")
    return computer.run_until_big_int()


with open("21.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
