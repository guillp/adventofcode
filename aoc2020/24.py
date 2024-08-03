from collections.abc import Iterable, Iterator
from enum import Enum
from functools import cache


class Direction(complex, Enum):
    e = -2
    w = 2
    ne = -1 - 1j
    nw = 1 - 1j
    se = -1 + 1j
    sw = 1 + 1j


def iter_path(path: str) -> Iterable[str]:
    while path:
        for n in Direction:
            if path.startswith(n.name):
                yield n.name
                path = path.removeprefix(n.name)


def solve(content: str) -> Iterator[int]:
    black_tiles: set[complex] = set()
    for line in content.splitlines():
        pos = 0j
        for tile in iter_path(line):
            pos += Direction[tile]
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)

    yield len(black_tiles)

    @cache
    def tiles_at(day: int) -> set[complex]:
        if day == 0:
            return black_tiles

        previous_tiles = tiles_at(day - 1)
        new_tiles = set()
        for black_tile in previous_tiles:
            nb_adjacent_black_tiles = sum(black_tile + direction in previous_tiles for direction in Direction)
            if 0 < nb_adjacent_black_tiles <= 2:
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
                if sum(tile + direction in previous_tiles for direction in Direction) == 2:
                    new_tiles.add(tile)

        return new_tiles

    yield len(tiles_at(100))


test_content = """\
sesenwnenenewseeswwswswwnenewsewsw
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

assert tuple(solve(test_content)) == (10, 2208)

with open("24.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
