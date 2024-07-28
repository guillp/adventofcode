from collections.abc import Iterator


def crab(cups: tuple[int, ...], n: int) -> tuple[int, ...]:
    ring = {a: b for a, b in zip(cups, cups[1:] + cups[:1])}

    current_cup = cups[0]
    for _ in range(n):
        pickedup_cups = (a := ring[current_cup], b := ring[a], c := ring[b])
        destination_cup = current_cup
        while destination_cup == current_cup or destination_cup in pickedup_cups:
            destination_cup -= 1
            if destination_cup == 0:
                destination_cup = len(cups)
        next_current_cup = ring[c]
        ring[current_cup] = next_current_cup
        ring[c] = ring[destination_cup]
        ring[destination_cup] = a
        current_cup = next_current_cup

    def iter_ring(start: int) -> Iterator[int]:
        yield start
        n = ring[start]
        while n != start:
            yield n
            n = ring[n]

    return tuple(iter_ring(current_cup))


def part1(content: str) -> str:
    init_cups = tuple(int(x) for x in content)
    cups = crab(init_cups, 100)
    index1 = cups.index(1)
    return "".join(str(x) for x in cups[:index1] + cups[index1 + 1 :])


def part2(content: str) -> int:
    init_cups = tuple(int(x) for x in content)
    cups = crab(init_cups + tuple(range(max(init_cups) + 1, 1000000 + 1)), 10000000)
    index1 = cups.index(1)
    return cups[index1 + 1] * cups[index1 + 2]


test_content = "389125467"

assert part1(test_content) == "67384529"
assert part2(test_content) == 149245887792

content = "123487596"


print(part1(content))
print(part2(content))
