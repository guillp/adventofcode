def game_part2(deck1: list[int], deck2: list[int]) -> int:
    states = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in states:
            return 1
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner = game_part2(deck1[:card1], deck2[:card2])
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))

        states.add(state)

    return 1 if deck1 else 2


def score(deck: list[int]) -> int:
    return sum(card * i for i, card in enumerate(reversed(deck), start=1))


def part1(content: str) -> int:
    deck1, deck2 = ([int(x) for x in lines.splitlines()[1:]] for lines in content.split("\n\n"))
    while deck1 and deck2:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))
    return score(deck1 or deck2)


def part2(content: str) -> int:
    deck1, deck2 = ([int(x) for x in lines.splitlines()[1:]] for lines in content.split("\n\n"))
    game_part2(deck1, deck2)
    return score(deck1 or deck2)


test_content = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

assert part1(test_content) == 306
assert part2(test_content) == 291

with open("22.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
