from enum import StrEnum


class OutputSignal(RuntimeError):
    def __init__(self, value: int) -> None:
        self.value = value


class ParamMode(StrEnum):
    POSITION = "0"
    IMMEDIATE = "1"
    RELATIVE = "2"


class Computer:
    def __init__(self, instructions: str, *inputs: int) -> None:
        self.instructions = {i: int(x) for i, x in enumerate(instructions.split(","))}
        self.pointer = 0
        self.relative_base = 0
        self.inputs = list(inputs)
        self.waiting_for_input = False

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

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


def part1(content: str) -> int:
    computers = [Computer(content, address) for address in range(50)]
    queues = [[] for _ in range(50)]
    while True:
        for i, computer in enumerate(computers):
            try:
                computer.next()
            except OutputSignal as out:
                val = out.value
                queues[i].append(val)
                if len(queues[i]) == 3:
                    dest, x, y = queues[i]
                    queues[i].clear()

                    if dest == 255:
                        return y
                    elif 0 <= dest < 50:
                        computers[dest].add_input(x, y)


def part2(content: str) -> int:
    computers = [Computer(content, address) for address in range(50)]
    queues = [[] for _ in range(50)]
    nat: tuple[int, int] | None = None
    nat_history = []

    while True:
        if nat is not None and all(computer.waiting_for_input for computer in computers):
            computers[0].add_input(*nat)
            x, y = nat
            if nat_history and nat_history[-1] == y:
                return y
            nat_history.append(y)
            nat = None
        for i, computer in enumerate(computers):
            try:
                computer.next()
            except OutputSignal as out:
                val = out.value
                queues[i].append(val)
                if len(queues[i]) == 3:
                    dest, x, y = queues[i]
                    queues[i].clear()

                    if dest == 255:
                        nat = x, y
                    elif 0 <= dest < 50:
                        computers[dest].add_input(x, y)


with open("23.txt") as f:
    content = f.read()
print(part1(content))
print(part2(content))
