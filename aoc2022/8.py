import math
from itertools import accumulate

content = """30373
25512
65332
33549
35390
"""

with open("8.txt", "rt") as finput:
    content = finput.read()

lines = content.splitlines()
grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

s = 0
W, H = len(lines[0]), len(lines)

visibility = {}


def find_visibles(row: str):
    if len(row) == 0:
        return 1
    if len(row) == 1:
        return 1
    m = max(row)
    parts = row.split(m)
    return find_visibles(parts[0]) + find_visibles(parts[-1])


for x in range(W):
    for y in range(H):
        h = grid[(x, y)]
        if x in (0, W - 1) or max(grid[(X, y)] for X in range(x)) < h:
            visibility[(x, y)] = True
        if x in (0, W - 1) or max(grid[(X, y)] for X in range(x + 1, W)) < h:
            visibility[(x, y)] = True
        if y in (0, H - 1) or max(grid[(x, Y)] for Y in range(y)) < h:
            visibility[(x, y)] = True
        if y in (0, H - 1) or max(grid[(x, Y)] for Y in range(y + 1, H)) < h:
            visibility[(x, y)] = True

print(len(visibility))

scores = {}

for y in range(H):
    for x in range(W):
        h = grid[(x, y)]
        left_score = 0
        for i in range(1, x+1):
            left_score += 1
            if grid[(x - i, y)] >= h:
                break
        right_score = 0
        for i in range(1, W - x):
            right_score += 1
            if grid[(x + i, y)] >= h:
                break
        top_score = 0
        for i in range(1, y + 1):
            top_score += 1
            if grid[(x, y - i)] >= h:
                break
        bottom_score = 0
        for i in range(1, H - y):
            bottom_score += 1
            if grid[(x, y + i)] >= h:
                break
        scores[(x, y)] = left_score * right_score * top_score * bottom_score

print(max(scores.values()))
