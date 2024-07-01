from collections.abc import Iterator

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

LOSE, DRAW, WIN = 1, 2, 3


def score(other: int, you: int) -> int:
    if you == other:
        return 3 + you
    if WINNERS[you] == other:
        return 6 + you
    return you


def score2(other: int, result: int) -> int:
    if result == LOSE:
        return WINNERS[other]
    if result == DRAW:
        return other + 3
    if result == WIN:
        for winner, looser in WINNERS.items():
            if other == looser:
                return winner + 6
    assert False, "Solution not found"


def solve(content: str) -> Iterator[int]:
    rounds = tuple(tuple(LETTERS[x] for x in line.split()) for line in content.splitlines())

    yield sum(score(other, you) for other, you in rounds)
    yield sum(score2(other, you) for other, you in rounds)


assert tuple(
    solve("""\
A Y
B X
C Z
""")
) == (15, 12)

with open("02.txt") as finput:
    content = finput.read()

for part in solve(content):
    print(part)
