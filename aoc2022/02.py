with open("02.txt", "rt") as finput:
    content = finput.readlines()

ROCK, PAPER, SCISSORS = 1, 2, 3

LETTERS = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

WINNERS = {ROCK: SCISSORS, SCISSORS: PAPER, PAPER: ROCK}


def score(round) -> int:
    other, you = round
    if you == other:
        return 3 + you
    if WINNERS[you] == other:
        return 6 + you
    return you


rounds = tuple(tuple(LETTERS[x] for x in line.split()) for line in content)

print(sum((score(round) for round in rounds)))

LOSE, DRAW, WIN = 1, 2, 3


def score2(round) -> int:
    other, result = round
    if result == LOSE:
        return WINNERS[other]
    if result == DRAW:
        return other + 3
    if result == WIN:
        for winner, looser in WINNERS.items():
            if other == looser:
                return winner + 6


print(sum((score2(round) for round in rounds)))
