from itertools import permutations


class OutputSignal(RuntimeError):
    def __init__(self, value: int ):
        self.value = value


class Computer:
    def __init__(self, instructions: str, *inputs: int):
        self.instructions = [int(x) for x in instructions.split(",")]
        self.pointer = 0
        self.inputs = list(inputs)

    def get_param(self, immediate: bool = False) -> int:
        value = self.instructions[self.pointer]
        self.pointer += 1
        if immediate:
            return value
        return self.instructions[value]

    def get_instruction(self) -> tuple[str, tuple[bool, ...]]:
        instruction = f"{self.instructions[self.pointer]:05d}"
        opcode = instruction[3:]
        modes = tuple(x == "1" for x in instruction[:3][::-1])
        self.pointer += 1
        return opcode, modes

    def store(self, value: int, pos: int) -> None:
        self.instructions[pos] = value

    def next(self):
        opcode, modes = self.get_instruction()
        if opcode == "99":  # quit
            raise StopIteration()
        if opcode == "01":  # add
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            res = left + right
            self.store(res, dest)
        elif opcode == "02":  # mult
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            res = left * right
            self.store(res, dest)
        elif opcode == "03":  # store input
            assert modes[0] is False
            value = self.inputs.pop(0)
            dest = self.get_param(True)
            self.store(value, dest)
        elif opcode == "04":  # output
            source = self.get_param(modes[0])
            raise OutputSignal(source)
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
            assert modes[2] is False
            dest = self.get_param(True)
            if left < right:
                self.store(1, dest)
            else:
                self.store(0, dest)
        elif opcode == "08":  # equals
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            if left == right:
                self.store(1, dest)
            else:
                self.store(0, dest)

    def run(self, i: int|None = None) -> int:
        if i is not None:
            self.inputs.append(i)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value

    def __repr__(self):
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


content = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
with open("07.txt") as f: content = f.read()


res: tuple[int, tuple[int, ...]] = (0, None)
for phases in permutations(range(5)):
    n = 0
    for phase in phases:
        n = Computer(content, phase).run(n)
    if n > res[0]:
        res = n, phases

print(res)

res = (0, None)
for phases in permutations(range(5, 10)):
    n = 0
    computers = [Computer(content, phase) for phase in phases]

    while True:
        try:
            for computer in computers:
                n = computer.run(n)
        except StopIteration:
            break
    if n > res[0]:
        res = n, phases

print(res)