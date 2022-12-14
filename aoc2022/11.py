from operator import attrgetter
from dataclasses import dataclass

from stringparser import Parser

content = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

with open('11.txt', 'rt') as finput: content = finput.read()

parser = Parser("""Monkey {:d}:
  Starting items: {}
  Operation: new = {}
  Test: divisible by {:d}
    If true: throw to monkey {:d}
    If false: throw to monkey {:d}""")


@dataclass
class Monkey:
    items: list[int]
    operation: str
    diviser: int
    true_target: int
    false_target: int
    nb_inspections: int = 0


monkeys = {}
for monkey in content.split('\n\n'):
    monkey_no, starting_items, operation, diviser, true_target, false_target = parser(monkey)
    items = [int(x) for x in starting_items.split(', ')]
    monkeys[monkey_no] = Monkey(items, operation, diviser, true_target, false_target)

for i in range(20):
    for monkey_no, monkey in monkeys.items():
        while monkey.items:
            item = monkey.items.pop(0)
            item = eval(monkey.operation, None, {'old': item})
            item //= 3
            if item % monkey.diviser == 0:
                monkeys[monkey.true_target].items.append(item)
            else:
                monkeys[monkey.false_target].items.append(item)
            monkey.nb_inspections += 1

monkey1, monkey2 = sorted(monkeys.values(), key=attrgetter('nb_inspections'))[-2:]
print(monkey1.nb_inspections * monkey2.nb_inspections)


monkeys = {}
for monkey in content.split('\n\n'):
    monkey_no, starting_items, operation, diviser, true_target, false_target = parser(monkey)
    items = [int(x) for x in starting_items.split(', ')]
    monkeys[monkey_no] = Monkey(items, operation, diviser, true_target, false_target)

modulo = 223092870

for i in range(10000):
    for monkey_no, monkey in monkeys.items():
        while monkey.items:
            item = monkey.items.pop(0)
            item = eval(monkey.operation, None, {'old': item})
            item %= modulo
            if item % monkey.diviser == 0:
                monkeys[monkey.true_target].items.append(item)
            else:
                monkeys[monkey.false_target].items.append(item)
            monkey.nb_inspections += 1

monkey1, monkey2 = sorted(monkeys.values(), key=attrgetter('nb_inspections'))[-2:]
print(monkey1, monkey2)
print(monkey1.nb_inspections * monkey2.nb_inspections)
