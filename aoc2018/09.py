from collections import deque, defaultdict


def part1(nb_players: int, max_marble: int) -> int:
    marbles = deque([0])
    scores = defaultdict(int)
    for marble in range(1, max_marble+1):
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

assert part1(9, 25) == 32
assert part1(10, 1618) == 8317
assert part1(13, 7999) == 146373
assert part1(17, 1104) == 2764
assert part1(21, 6111) == 54718
assert part1(30, 5807) == 37305

print(part1(435, 71184))
print(part1(435, 71184*100))