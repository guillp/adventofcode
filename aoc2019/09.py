import sys
from typing import Literal


class OutputSignal(RuntimeError):
    def __init__(self, value: int):
        self.value = value


POSITION, IMMEDIATE, RELATIVE = "0", "1", "2"


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


class Computer:
    def __init__(self, instructions: str, *inputs: int):
        self.instructions = {i: int(x) for i, x in enumerate(instructions.split(","))}
        self.pointer = 0
        self.relative_base = 0
        self.inputs = list(inputs)

    def get_param(self, mode: Literal[POSITION, IMMEDIATE, RELATIVE]) -> int:
        value = self.instructions[self.pointer]
        self.pointer += 1
        if mode == IMMEDIATE:
            return value
        elif mode == POSITION:
            return self.instructions.get(value, 0)
        elif mode == RELATIVE:
            return self.instructions[self.relative_base + value]
        assert False, f"Unknown mode {mode}"

    def set_param(self, mode: Literal[POSITION, RELATIVE], value) -> None:
        dest = self.get_param(IMMEDIATE)
        if mode == POSITION:
            self.instructions[dest] = value
        elif mode == RELATIVE:
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


assert Computer(
    "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
).run_until_halt() == [
    int(x)
    for x in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
]
assert Computer("1102,34915192,34915192,7,4,7,99,0").run() == 1219070632396864
assert Computer("104,1125899906842624,9").run() == 1125899906842624

assert Computer("109, -1, 4, 1, 99").run() == -1
assert Computer("109, -1, 104, 1, 99").run() == 1
assert Computer("109, -1, 204, 1, 99").run() == 109
assert Computer("109, 1, 9, 2, 204, -6, 99").run() == 204
assert Computer("109, 1, 109, 9, 204, -6, 99").run() == 204
assert Computer("109, 1, 209, -1, 204, -106, 99").run() == 204
assert Computer("109, 1, 3, 3, 204, 2, 99", 999).run() == 999
assert Computer("109, 1, 203, 2, 204, 2, 99", 999).run() == 999


with open("09.txt") as f:
    content = f.read()

print(Computer(content, 1).run_until_halt())
print(Computer(content, 2).run_until_halt())
