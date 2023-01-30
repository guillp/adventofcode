from functools import cache
from typing import Iterable

content = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

with open("24.txt") as f:
    content = f.read()


def iter_path(path: str) -> Iterable[str]:
    while path:
        for n in ("nw", "ne", "sw", "se", "e", "w"):
            if path.startswith(n):
                yield n
                path = path.removeprefix(n)


black_tiles = set()
for line in content.splitlines():
    pos = 0
    for tile in iter_path(line):
        pos += {
            "e": -2,
            "w": 2,
            "ne": -1 - 1j,
            "nw": 1 - 1j,
            "se": -1 + 1j,
            "sw": 1 + 1j,
        }.get(tile)
    if pos in black_tiles:
        black_tiles.remove(pos)
    else:
        black_tiles.add(pos)

print(len(black_tiles))


@cache
def tiles_at(day: int) -> set[complex]:
    if day == 0:
        return black_tiles

    previous_tiles = tiles_at(day - 1)
    new_tiles = set()
    for black_tile in previous_tiles:
        if (
            0
            < sum(
                black_tile + dir in previous_tiles
                for dir in (-2, 2, -1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j)
            )
            <= 2
        ):
            new_tiles.add(black_tile)

    min_real = int(min(pos.real for pos in previous_tiles) - 1)
    max_real = int(max(pos.real for pos in previous_tiles) + 1)
    min_imag = int(min(pos.imag for pos in previous_tiles) - 1)
    max_imag = int(max(pos.imag for pos in previous_tiles) + 1)

    for real in range(min_real, max_real + 1):
        for imag in range(min_imag, max_imag + 1):
            if (real + imag) % 2:
                continue
            tile = complex(real, imag)
            if tile in previous_tiles:
                continue
            if (
                sum(
                    tile + dir in previous_tiles
                    for dir in (-2, 2, -1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j)
                )
                == 2
            ):
                new_tiles.add(tile)

    return new_tiles


print(len(tiles_at(100)))
