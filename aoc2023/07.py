from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum
from typing import ClassVar


class Rank(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF__KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


@dataclass(frozen=True, slots=True, order=True)
class Hand:
    cards: str = field(compare=False)
    rank: Rank = field(init=False)
    order: tuple[int] = field(init=False)

    cards_order: ClassVar[str] = "23456789TJQKA"

    @property
    def counts(self) -> Counter[str]:
        return Counter(self.cards)

    def __post_init__(self) -> None:
        match self.counts.most_common():
            case ((_, 5),):
                rank = Rank.FIVE_OF_A_KIND
            case ((_, 4), (_, 1)):
                rank = Rank.FOUR_OF_A_KIND
            case ((_, 3), (_, 2)):
                rank = Rank.FULL_HOUSE
            case ((_, 3), (_, 1), (_, 1)):
                rank = Rank.THREE_OF__KIND
            case ((_, 2), (_, 2), (_, 1)):
                rank = Rank.TWO_PAIR
            case ((_, 2), *_):
                rank = Rank.PAIR
            case _:
                rank = Rank.HIGH_CARD
        object.__setattr__(self, "rank", rank)
        object.__setattr__(self, "order", tuple(self.cards_order.index(card) for card in self.cards))


def part1(content: str) -> int:
    hand2bid = {Hand(card): int(x) for line in content.splitlines() for card, x in [line.split()]}
    return sum((rank) * hand2bid[hand] for rank, hand in enumerate(sorted(hand2bid), start=1))


@dataclass(frozen=True)
class JokerHand(Hand):
    cards_order: ClassVar[str] = "J23456789TQKA"

    @property
    def counts(self) -> Counter[str]:
        counts = Counter(self.cards)
        jokers = counts["J"]
        if jokers != 5:  # add jokers to the most frequent other card
            del counts["J"]
            most_frequent_card, _ = counts.most_common(1)[0]
            counts[most_frequent_card] += jokers
        return counts


def part2(content: str) -> int:
    jokerhand2bid = {JokerHand(card): int(x) for line in content.splitlines() for card, x in [line.split()]}
    return sum((rank) * jokerhand2bid[hand] for rank, hand in enumerate(sorted(jokerhand2bid), start=1))


test_content = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


assert part1(test_content) == 6440
assert part2(test_content) == 5905


with open("07.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
