import re
from dataclasses import dataclass
from operator import attrgetter


@dataclass
class Monkey:
    items: list[int]
    operation: str
    diviser: int
    true_target: int
    false_target: int
    nb_inspections: int = 0


def solve(content: str, part2: bool = False) -> int:
    monkeys: dict[int, Monkey] = {}
    for monkey_no, starting_items, operation, diviser, true_target, false_target in re.findall(
        r"""^Monkey (\d+):
 +Starting items: (.*)
 +Operation: new = (.*)
 +Test: divisible by (\d+)
 +If true: throw to monkey (\d+)
 +If false: throw to monkey (\d+)$""",
        content,
        re.MULTILINE,
    ):
        items = [int(x) for x in starting_items.split(", ")]
        monkeys[int(monkey_no)] = Monkey(items, operation, int(diviser), int(true_target), int(false_target))

    modulo = 223092870

    for _ in range(10000 if part2 else 20):
        for monkey_no, monkey in monkeys.items():
            while monkey.items:
                item = monkey.items.pop(0)
                item = eval(monkey.operation, None, {"old": item})
                if part2:
                    item %= modulo
                else:
                    item //= 3
                if item % monkey.diviser == 0:
                    monkeys[monkey.true_target].items.append(item)
                else:
                    monkeys[monkey.false_target].items.append(item)
                monkey.nb_inspections += 1

    monkey1, monkey2 = sorted(monkeys.values(), key=attrgetter("nb_inspections"))[-2:]
    return monkey1.nb_inspections * monkey2.nb_inspections


test_content = """Monkey 0:
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

assert solve(test_content) == 10605
assert solve(test_content, part2=True) == 2713310158

with open("11.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
