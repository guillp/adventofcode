import sys

content = "1,9,10,3,2,3,11,0,99,30,40,50"

with open("05.txt") as f: content = f.read()

positions = tuple(int(x) for x in content.split(','))

def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)

class Computer:
    def __init__(self, instructions: tuple[int], inputs: list[int]):
        self.instructions = list(instructions)
        self.pointer = 0
        self.inputs = inputs
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
    def next(self):
        opcode, modes = self.get_instruction()
        if opcode == "99": # quit
            debug("HALT")
            raise StopIteration()
        if opcode == "01": # add
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            res = left + right
            self.store(res, dest)
            debug(f"ADD {left} + {right} -> {dest}")
        elif opcode == "02": # mult
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            res = left * right
            self.store(res, dest)
            debug(f"MULT {left} x {right} -> {dest}")
        elif opcode == "03": # store input
            assert modes[0] is False
            value = self.inputs.pop(0)
            dest = self.get_param(True)
            self.store(value, dest)
            debug(f"STORE {value} -> {dest}")
        elif opcode == "04": # output
            source = self.get_param(modes[0])
            self.outputs.append(source)
            debug(f"OUT {source}")
        elif opcode == "05": # jump-if-true
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            if test != 0:
                self.pointer = dest
            debug(f"JUMP {test} != 0 -> {dest}")
        elif opcode == "06": # jump-if-false
            test = self.get_param(modes[0])
            dest = self.get_param(modes[1])
            if test == 0:
                self.pointer = dest
            debug(f"JUMP {test} == 0 -> {dest}")
        elif opcode == "07": # less than
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            if left < right:
                self.store(1, dest)
            else:
                self.store(0, dest)
            debug(f"LT {left} < {right} -> {dest}")
        elif opcode == "08": # equals
            left = self.get_param(modes[0])
            right = self.get_param(modes[1])
            assert modes[2] is False
            dest = self.get_param(True)
            if left == right:
                self.store(1, dest)
            else:
                self.store(0, dest)
            debug(f"EQ {left} == {right} -> {dest}")

    def run(self) -> list[int]:
        try:
            while True:
                self.next()
        except StopIteration:
            return self.outputs
    def __repr__(self):
        return f"{self.pointer} -> {self.instructions[self.pointer]}"


assert Computer([int(x) for x in "3,9,8,9,10,9,4,9,99,-1,8".split(',')], [8]).run() == [1]
assert Computer([int(x) for x in "3,9,8,9,10,9,4,9,99,-1,8".split(',')], [141]).run() == [0]
assert Computer([int(x) for x in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")], [8]).run() == [1]
assert Computer([int(x) for x in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")], [0]).run() == [0]
assert Computer([int(x) for x in "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")], [-1]).run() == [1]
assert Computer([int(x) for x in "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")], [0]).run() == [0]
assert Computer([int(x) for x in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")], [0]).run() == [999]
assert Computer([int(x) for x in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")], [8]).run() == [1000]
assert Computer([int(x) for x in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")], [22]).run() == [1001]

c = Computer(positions, [1])
print(c.run())
c = Computer(positions, [5])
print(c.run())

