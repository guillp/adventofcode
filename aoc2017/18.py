from collections import defaultdict, deque


def part1(content: str) -> int:
    instructions = content.splitlines()
    cursor = 0
    registers: dict[str, int] = defaultdict(int)
    sounds = []

    def get_value(x: str) -> int:
        return registers[x] if x.isalpha() else int(x)

    while True:
        match instructions[cursor].split():
            case "snd", x:
                sounds.append(get_value(x))
            case "set", x, y:
                registers[x] = get_value(y)
            case "add", x, y:
                registers[x] += get_value(y)
            case "mul", x, y:
                registers[x] *= get_value(y)
            case "mod", x, y:
                registers[x] %= get_value(y)
            case "rcv", x if get_value(x) != 0:
                return sounds[-1]
            case "jgz", x, y if get_value(x) != 0:
                cursor += get_value(y)
                continue
        cursor += 1


class Send(Exception):
    def __init__(self, value: int) -> None:
        self.value = value


class Part2Computer:
    def __init__(self, instructions: list[str], p: int) -> None:
        self.instructions = instructions
        self.registers = {"p": p}
        self.queue: deque[int] = deque()
        self.pointer = 0
        self.nb_sent = 0
        self.waiting = False

    def get_value(self, val: str) -> int:
        if val in self.registers:
            return self.registers[val]
        return int(val)

    def process_instruction(self) -> None:
        instruction = self.instructions[self.pointer]
        self.pointer += 1
        match instruction.split():
            case "jgz", x, y:
                if self.get_value(x) > 0:
                    self.pointer += self.get_value(y) - 1
            case "snd", x:
                self.nb_sent += 1
                raise Send(self.get_value(x))
            case "rcv", x:
                if len(self.queue) > 0:
                    self.registers[x] = self.queue.popleft()
                    self.waiting = False
                else:
                    self.waiting = True
                    self.pointer -= 1
            case "set", x, y:
                self.registers[x] = self.get_value(y)
            case "add", x, y:
                self.registers[x] += self.get_value(y)
            case "mul", x, y:
                self.registers[x] *= self.get_value(y)
            case "mod", x, y:
                self.registers[x] %= self.get_value(y)
            case _:
                assert False


def part2(content: str) -> int:
    instructions = content.splitlines()

    computer0 = Part2Computer(instructions, p=0)
    computer1 = Part2Computer(instructions, p=1)

    while not computer0.waiting or not computer1.waiting:
        try:
            computer0.process_instruction()
        except Send as exc:
            computer1.queue.append(exc.value)
        try:
            computer1.process_instruction()
        except Send as exc:
            computer0.queue.append(exc.value)

    return computer1.nb_sent


test_content1 = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""

assert part1(test_content1) == 4

test_content2 = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""

assert part2(test_content2) == 3

with open("18.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
