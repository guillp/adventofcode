import re
from collections import Counter, defaultdict
from itertools import product


def part1(content: str) -> int:
    pos = [int(x) for x in re.findall(r"\d+$", content, re.MULTILINE)]
    scores = [0, 0]
    target = 1000
    turn = 0

    while True:
        player = turn % 2
        pos[player] = (pos[player] + 5 + 10 * player + 18 * turn // 2) % 10 + 1
        scores[player] += pos[player]
        turn += 1
        if max(scores) >= target:
            break

    return min(scores) * turn * 3


def part2(content: str) -> int:
    initial_pos1, initial_pos2 = (int(x) for x in re.findall(r"\d+$", content, re.MULTILINE))
    states = defaultdict(
        int,
        {(initial_pos1, initial_pos2, 0, 0, 0): 1},  # current state -> nb of universes leading to that state
    )
    target = 21
    wins = [0, 0]

    # possible sums of three dice rolls -> nb of ways to get that sum
    rolls_count = Counter(sum(dices) for dices in product((1, 2, 3), repeat=3))

    while states:
        (pos1, pos2, score1, score2, current_player), nb_universes = states.popitem()
        for roll, multiplier in rolls_count.items():
            new_pos = ((pos1, pos2)[current_player] + roll - 1) % 10 + 1
            new_score = ((score1, score2)[current_player]) + new_pos
            if new_score >= target:
                wins[current_player] += nb_universes * multiplier
            elif current_player == 0:
                states[(new_pos, pos2, new_score, score2, 1)] += nb_universes * multiplier
            elif current_player == 1:
                states[(pos1, new_pos, score1, new_score, 0)] += nb_universes * multiplier

    return max(wins)


with open("21.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
