with open("04.txt") as f:
    content = f.read()


def score_card(card: str) -> tuple[int, int]:
    card_part, number_part = card.split(":")
    card_id = int(card_part.split()[1])
    winning_part, played_part = number_part.split("|")
    winning = set(int(x) for x in winning_part.split())
    played = set(int(x) for x in played_part.split())
    common = winning & played
    return card_id, len(common)


s = 0
for line in content.splitlines():
    card_id, matches = score_card(line)
    if matches:
        s += 2 ** (matches - 1)

print("PART1:", s)

cards = dict(score_card(line) for line in content.splitlines())
cards_qty = {card_id: 1 for card_id in cards}

for card_id, matches in cards.items():  # cards dict is already sorted
    qty = cards_qty[card_id]
    for i in range(card_id + 1, card_id + matches + 1):
        cards_qty[i] += qty

print("PART2:", sum(cards_qty.values()))
