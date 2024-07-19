class Computer:
    def __init__(self, instructions: str, *inputs: int) -> None:
        self.instructions = list(int(x) for x in instructions.split(","))
        self.pointer = 0
        self.inputs = list(inputs)
        self.outputs = []

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
            self.outputs.append(source)
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

    def run(self) -> list[int]:
        try:
            while True:
                self.next()
        except StopIteration:
            return self.outputs

    def __repr__(self) -> str:
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


assert Computer("3,9,8,9,10,9,4,9,99,-1,8", [8]).run() == [1]
assert Computer("3,9,8,9,10,9,4,9,99,-1,8", [141]).run() == [0]
assert Computer("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [8]).run() == [1]
assert Computer("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0]).run() == [0]
assert Computer("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [-1]).run() == [1]
assert Computer("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0]).run() == [0]
assert Computer(
    "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
    [0],
).run() == [999]
assert Computer(
    "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
    [8],
).run() == [1000]
assert Computer(
    "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
    [22],
).run() == [1001]


def part1(content: str) -> int:
    c = Computer(content, [1])
    return c.run()[-1]


def part2(content: str) -> int:
    c = Computer(content, [5])
    return c.run()[-1]


with open("05.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
