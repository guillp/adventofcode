from collections import Counter

content = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
# with open('07.txt') as f: content = f.read()

(
    HIGH_CARD,
    PAIR,
    TWO_PAIR,
    THREE_OF__KIND,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    FIVE_OF_A_KIND,
) = (1, 2, 3, 4, 5, 6, 7)


class Hand:
    def __init__(self, cards: str):
        self.cards = cards
        match Counter(cards).most_common():
            case ((_, 5)):
                rank = FIVE_OF_A_KIND
            case ((_, 4), (_, 1)):
                rank = FOUR_OF_A_KIND
            case ((_, 3), (_, 2)):
                rank = FULL_HOUSE
            case ((_, 3), (_, 1), (_, 1)):
                rank = THREE_OF__KIND
            case ((_, 2), (_, 2), (_, 1)):
                rank = TWO_PAIR
            case ((_, 2), *_):
                rank = PAIR
            case _:
                rank = HIGH_CARD
        self.rank = rank
        self.order = tuple("23456789TJQKA".index(card) for card in cards)

    def __gt__(self, other) -> bool:
        if self.rank == other.rank:
            return self.order > other.order
        return self.rank > other.rank

    def __repr__(self):
        return f"{self.cards} ({self.rank})"


hand2bid = {
    Hand(card): int(x) for line in content.splitlines() for card, x in [line.split()]
}

print(
    sum(
        (rank + 1) * hand2bid[hand]
        for rank, hand in enumerate(sorted(hand2bid))
    )
)


class JokerHand(Hand):
    def __init__(self, cards: str) -> None:
        self.cards = cards
        counts = Counter(cards)
        jokers = counts["J"]
        if jokers != 5:  # add jokers to the most frequent other card
            del counts["J"]
            most_frequent_card, most_frequent_count = counts.most_common(1)[0]
            counts[most_frequent_card] += jokers
        match counts.most_common():
            case ((_, 5)):
                rank = FIVE_OF_A_KIND
            case ((_, 4), (_, 1)):
                rank = FOUR_OF_A_KIND
            case ((_, 3), (_, 2)):
                rank = FULL_HOUSE
            case ((_, 3), (_, 1), (_, 1)):
                rank = THREE_OF__KIND
            case ((_, 2), (_, 2), (_, 1)):
                rank = TWO_PAIR
            case ((_, 2), *_):
                rank = PAIR
            case _:
                rank = HIGH_CARD
        self.rank = rank
        self.order = tuple("J23456789TQKA".index(card) for card in cards)


jokerhand2bid = {
    JokerHand(card): int(x)
    for line in content.splitlines()
    for card, x in [line.split()]
}

print(
    sum(
        (rank + 1) * jokerhand2bid[hand]
        for rank, hand in enumerate(sorted(jokerhand2bid))
    )
)
