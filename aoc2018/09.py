from collections import defaultdict, deque


def solve(nb_players: int, max_marble: int) -> int:
    marbles = deque([0])
    scores: dict[int, int] = defaultdict(int)
    for marble in range(1, max_marble + 1):
        if marble % 23 != 0:
            marbles.rotate(-1)
            marbles.append(marble)
        else:
            player = marble % nb_players
            scores[player] += marble
            marbles.rotate(7)
            scores[player] += marbles.pop()
            marbles.rotate(-1)

    return max(scores.values())


assert solve(9, 25) == 32
assert solve(10, 1618) == 8317
assert solve(13, 7999) == 146373
assert solve(17, 1104) == 2764
assert solve(21, 6111) == 54718
assert solve(30, 5807) == 37305

print(solve(435, 71184))
print(solve(435, 71184 * 100))
