from itertools import permutations


class OutputSignal(RuntimeError):
    def __init__(self, value: int) -> None:
        self.value = value


class Computer:
    def __init__(self, instructions: str, *inputs: int) -> None:
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

    def next(self) -> None:
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

    def run(self, i: int | None = None) -> int:
        if i is not None:
            self.inputs.append(i)
        try:
            while True:
                self.next()
        except OutputSignal as out:
            return out.value

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


def part1(content: str) -> int:
    res: tuple[int, tuple[int, ...]] = (0, None)
    for phases in permutations(range(5)):
        n = 0
        for phase in phases:
            n = Computer(content, phase).run(n)
        if n > res[0]:
            res = n, phases

    return res[0]


def part2(content: str) -> int:
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
    return res[0]


assert part1("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0") == 43210
assert part1("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0") == 54321
assert (
    part1("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    == 65210
)


assert part2("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5") == 139629729
assert (
    part2(
        "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    )
    == 18216
)

with open("07.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
