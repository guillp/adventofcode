content = """Player 1:
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

with open("22.txt") as f:
    content = f.read()

deck1, deck2 = (
    list(int(x) for x in lines.splitlines()[1:]) for lines in content.split("\n\n")
)


def game(deck1: list[int], deck2: list[int]) -> None:
    while deck1 and deck2:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))


def score(deck: list[int]) -> int:
    return sum(card * i for i, card in enumerate(reversed(deck), start=1))


game(deck1, deck2)
print(score(deck1 or deck2))

# part 2
deck1, deck2 = (
    list(int(x) for x in lines.splitlines()[1:]) for lines in content.split("\n\n")
)


def game2(deck1, deck2) -> int:
    states = set()
    while deck1 and deck2:
        state = (tuple(deck1), tuple(deck2))
        if state in states:
            return 1
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner = game2(deck1[:card1], deck2[:card2])
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


game2(deck1, deck2)
print(score(deck1 or deck2))
