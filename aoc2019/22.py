with open('22.txt') as f: content = f.read()


def part1(content: str, N: int = 10007, card: int = 2019) -> int:
    for line in content.splitlines():
        match line.split():
            case "deal", "into", "new", "stack":
                card = N - card - 1
            case "cut", _ as pos:
                pos = int(pos) % N
                card -= pos if card >= pos else pos - N
            case "deal", "with", "increment", _ as inc:
                card = (card * int(inc)) % N
            case _:
                assert False, line

    return card


assert part1("deal into new stack", 10, 3) == 6
assert part1("deal into new stack", 10, 0) == 9
assert part1("cut 3", 10, 0) == 7
assert part1("cut 3", 10, 3) == 0
assert part1("cut -4", 10, 3) == 7
assert part1("deal with increment 3", 10, 0) == 0
assert part1("deal with increment 3", 10, 1) == 3
assert part1("deal with increment 3", 10, 2) == 6

print(part1(content, 10007, 2019))
