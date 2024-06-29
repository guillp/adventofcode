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


class Computer:
    def __init__(self, pid: int, *instructions: str) -> None:
        self.instructions = instructions
        self.cursor = 0
        self.registers = defaultdict(int)
        self.registers["p"] = pid
        self.queue: deque[int] = deque()

    def get_value(self, x: str) -> int:
        return self.registers[x] if x.isalpha() else int(x)

    def next(self, i: int | None = None) -> int | None:
        if i is not None:
            self.queue.append(i)
        while True:
            match self.instructions[self.cursor].split():
                case "snd", x:
                    self.cursor += 1
                    return self.get_value(x)
                case "set", x, y:
                    self.registers[x] = self.get_value(y)
                case "add", x, y:
                    self.registers[x] += self.get_value(y)
                case "mul", x, y:
                    self.registers[x] *= self.get_value(y)
                case "mod", x, y:
                    self.registers[x] %= self.get_value(y)
                case "rcv", x if self.queue:
                    self.registers[x] = self.queue.popleft()
                case "rcv", x if len(self.queue) == 0:
                    return None
                case "jgz", x, y if self.get_value(x) != 0:
                    self.cursor += self.get_value(y) - 1
            self.cursor += 1


def part2(content: str) -> int:
    instructions = content.splitlines()
    c0 = Computer(0, *instructions)
    c1 = Computer(1, *instructions)

    next0: int | None
    next1: int | None
    next0 = next1 = None
    count = 0
    while True:
        next1 = c0.next(next0)
        next0 = c1.next(next1)
        if next0 is not None:
            count += 1
        if next0 is None and next1 is None:
            return count


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
