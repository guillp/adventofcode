import json
from collections.abc import Iterable
from typing import Any


def walk(doc: Any) -> Iterable[int]:
    if isinstance(doc, int):
        yield doc
    elif isinstance(doc, dict):
        for v in doc.values():
            yield from walk(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from walk(v)
    elif isinstance(doc, str):
        pass  # ignore strings
    else:
        assert False, doc


def part1(content: str) -> int:
    doc = json.loads(content)
    return sum(n for n in walk(doc))


def walk2(doc: Any) -> Iterable[int]:
    if isinstance(doc, int):
        yield doc
    elif isinstance(doc, dict):
        values = list(v for v in doc.values() if isinstance(v, str))
        if "red" not in values:
            for v in doc.values():
                yield from walk2(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from walk2(v)
    elif isinstance(doc, str):
        pass  # ignore strings
    else:
        assert False, doc


def part2(content: str) -> int:
    doc = json.loads(content)
    return sum(n for n in walk2(doc))


assert part1("[1,2,3]") == 6
assert part1('{"a":2,"b":4}') == 6
assert part1("[[[3]]]") == 3
assert part1('{"a":{"b":4},"c":-1}') == 3
assert part1('{"a":[-1,1]}') == 0
assert part1("[]") == 0
assert part1("{}") == 0

assert part2("[1,2,3]") == 6
assert part2('[1,{"c":"red","b":2},3]') == 4
assert part2('{"d":"red","e":[1,2,3,4],"f":5}') == 0
assert part2('[1,"red",5]') == 6

with open("12.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
