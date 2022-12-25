from itertools import cycle

import numpy as np
import pandas as pd

content = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

with open("17.txt") as finput:
    content = finput.read().strip()


ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

rocks = [
    pd.Series(
        complex(x, y)
        for y, line in enumerate(rock_str.splitlines())
        for x, c in enumerate(line)
        if c == "#"
    )
    for rock_str in ROCKS.strip().split("\n\n")
]

jets = cycle(content)

chamber = pd.Series(complex(i) for i in range(7))


def print_chamber(rock=pd.Series()):
    c = {(k.real, k.imag): "#" if k.imag != 0 else "-" for k in chamber.values}
    top = min(
        int(chamber.apply(np.imag).min()),
        int(rock.apply(np.imag).min()) if rock.any() else 1,
    )
    for y in range(top, 1):
        print(
            "".join(
                c.get((x, y), "@" if complex(x, y) in rock.values else ".")
                for x in range(7)
            )
        )
    print()


for i in range(2022):
    rock = rocks[i % len(rocks)].copy()
    height = rock.apply(np.imag).max() - rock.apply(np.real).min() + 1
    top = chamber.apply(np.imag).min()
    rock += 2 + (top - 3 - height) * 1j

    while True:
        push = next(jets)
        if push == "<":
            pushed_rock = rock - 1
            if (
                pushed_rock.apply(np.real).min() >= 0
                and not pushed_rock.isin(chamber).any()
            ):
                rock = pushed_rock
        elif push == ">":
            pushed_rock = rock + 1
            if (
                pushed_rock.apply(np.real).max() < 7
                and not pushed_rock.isin(chamber).any()
            ):
                rock = pushed_rock

        fell_rock = rock + 1j
        if not fell_rock.isin(chamber).any():
            rock = fell_rock
        else:
            chamber = pd.concat((chamber, rock))
            break

# print_chamber()
print(-int(chamber.apply(np.imag).min()))
