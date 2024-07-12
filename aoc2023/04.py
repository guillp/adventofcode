def score_card(card: str) -> tuple[int, int]:
    card_part, number_part = card.split(":")
    card_id = int(card_part.split()[1])
    winning_part, played_part = number_part.split("|")
    winning = set(int(x) for x in winning_part.split())
    played = set(int(x) for x in played_part.split())
    common = winning & played
    return card_id, len(common)


def part1(content: str) -> int:
    s = 0
    for line in content.splitlines():
        _, matches = score_card(line)
        if matches:
            s += 2 ** (matches - 1)
    return s


def part2(content: str) -> int:
    cards = dict(score_card(line) for line in content.splitlines())
    cards_qty = {card_id: 1 for card_id in cards}

    for card_id, matches in cards.items():  # cards dict is already sorted
        qty = cards_qty[card_id]
        for i in range(card_id + 1, card_id + matches + 1):
            cards_qty[i] += qty

    return sum(cards_qty.values())


test_content = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
assert part1(test_content) == 13
assert part2(test_content) == 30

with open("04.txt") as f:
    content = f.read()


print(part1(content))
print(part2(content))
