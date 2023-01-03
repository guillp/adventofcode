# cups = tuple(int(x) for x in "389125467")
cups = tuple(int(x) for x in "123487596")


def crab(cups: tuple[int], n: int) -> tuple[int]:
    ring = {a: b for a, b in zip(cups, cups[1:] + cups[:1])}

    current_cup = cups[0]
    for i in range(n):
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

    def iter_ring(start):
        yield start
        n = ring[start]
        while n != start:
            yield n
            n = ring[n]

    return tuple(iter_ring(current_cup))


def part1(cups: tuple[int]) -> str:
    index1 = cups.index(1)
    return "".join(str(x) for x in cups[:index1] + cups[index1 + 1 :])


print(part1(crab(cups, 100)))


def part2(cups: tuple[int]) -> int:
    index1 = cups.index(1)
    return cups[index1 + 1] * cups[index1 + 2]


print(part2(crab(cups + tuple(range(max(cups) + 1, 1000000 + 1)), 10000000)))
