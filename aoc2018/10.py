import re
from collections.abc import Iterator
from itertools import count


def solve(content: str) -> Iterator[str | int]:
    xs, ys, dxs, dys = zip(*[[int(x) for x in re.findall(r"-?\d+", line)] for line in content.strip().splitlines()])

    for i in count():
        height = max(ys) - min(ys)
        xs = tuple(x + dx for x, dx in zip(xs, dxs))
        ys = tuple(y + dy for y, dy in zip(ys, dys))

        if max(ys) - min(ys) > height:
            stars = [(x - dx, y - dy) for x, y, dx, dy in zip(xs, ys, dxs, dys)]
            for y in range(min(ys), max(ys)):
                yield "".join("#" if (x, y) in stars else "." for x in range(min(xs), max(xs)))
            yield i
            return


test_content = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

with open("10.txt") as f:
    content = f.read()
for line in solve(content):
    print(line)
