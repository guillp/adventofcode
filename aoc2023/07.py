from collections import Counter

content = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
#with open('07.txt') as f: content = f.read()

HIGH_CARD, PAIR, TWO_PAIR, THREE_OF__KIND, FULL_HOUSE, FOUR_OF_A_KIND, FIVE_OF_A_KIND = 1,2,3,4,5,6,7
class Hand:
    def __init__(self, cards: str):
        self.cards = cards
        counts = Counter(cards)
        if len(counts) == 1:
            rank = FIVE_OF_A_KIND
        elif len(counts) == 2:
            top = max(counts.values())
            if top == 4:
                rank = FOUR_OF_A_KIND
            elif top == 3:
                rank = FULL_HOUSE
        elif len(counts) == 3:
            top = max(counts.values())
            if top == 3:
                rank = THREE_OF__KIND
            elif top == 2:
                rank = TWO_PAIR
        elif len(counts) == 4:
            rank = PAIR
        else:
            rank = HIGH_CARD
        self.rank = rank
        self.order = tuple("23456789TJQKA".index(card) for card in cards)

    def __gt__(self, other) -> bool:
        if self.rank == other.rank:
            return self.order > other.order
        return self.rank > other.rank

    def __repr__(self):
        return f'{self.cards} ({self.rank})'

hand2bid = {
    Hand(card): int(x) for line in content.splitlines() for card, x in [line.split()]
}

s = 0
print(sorted(hand2bid))
for rank, hand in enumerate(sorted(hand2bid)):
    s += (rank+1) * hand2bid[hand]

print(s)

class Hand2:
    def __init__(self, cards: str):
        self.cards = cards
        counts = Counter(cards)
        jokers = counts['J']
        if jokers != 5:
            del counts['J']
            most_frequent_card, most_frequent_count = counts.most_common(1)[0]
            counts[most_frequent_card] += jokers
        if len(counts) == 1:
            rank = FIVE_OF_A_KIND
        elif len(counts) == 2:
            top = max(counts.values())
            if top == 4:
                rank = FOUR_OF_A_KIND
            elif top == 3:
                rank = FULL_HOUSE
        elif len(counts) == 3:
            top = max(counts.values())
            if top == 3:
                rank = THREE_OF__KIND
            elif top == 2:
                rank = TWO_PAIR
        elif len(counts) == 4:
            rank = PAIR
        else:
            rank = HIGH_CARD
        self.rank = rank
        self.order = tuple("J23456789TQKA".index(card) for card in cards)

    def __gt__(self, other) -> bool:
        if self.rank == other.rank:
            return self.order > other.order
        return self.rank > other.rank

    def __repr__(self):
        return f'{self.cards} ({self.rank})'

hand2bid = {
    Hand2(card): int(x) for line in content.splitlines() for card, x in [line.split()]
}

s = 0
print(sorted(hand2bid))
for rank, hand in enumerate(sorted(hand2bid)):
    s += (rank+1) * hand2bid[hand]

print(s)