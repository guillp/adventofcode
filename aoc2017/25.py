import re
from collections.abc import Iterator


def part1(content: str) -> int:
    parts = content.split("\n\n")

    state = re.search(r"Begin in state (\w)", parts[0]).group(1)  # type: ignore[union-attr]
    steps_before_checksum = int(re.search(r"Perform a diagnostic checksum after (\d+) steps.", parts[0]).group(1))  # type: ignore[union-attr]

    def iter_states() -> Iterator[tuple[str, tuple[tuple[int, int, str], tuple[int, int, str]]]]:
        for instate, write_value0, direction0, next_state0, write_value1, direction1, next_state1 in re.findall(
            r"""In state (\w):
  If the current value is 0:
    - Write the value (\d).
    - Move one slot to the (left|right).
    - Continue with state (\w).
  If the current value is 1:
    - Write the value (\d).
    - Move one slot to the (left|right).
    - Continue with state (\w).""",
            content,
            re.MULTILINE,
        ):
            yield (
                str(instate),
                (
                    (int(write_value0), -1 if direction0 == "left" else 1, str(next_state0)),
                    (int(write_value1), -1 if direction1 == "left" else 1, str(next_state1)),
                ),
            )

    states = dict(iter_states())

    tape: dict[int, int] = {}
    cursor = 0
    for step in range(steps_before_checksum):
        value, direction, state = states[state][tape.get(cursor, 0)]
        if value == 1:
            tape[cursor] = value
        else:
            tape.pop(cursor, None)
        cursor += direction

    return sum(tape.values())


test_content = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

assert part1(test_content) == 3

with open("25.txt") as f:
    content = f.read()

print(part1(content))
