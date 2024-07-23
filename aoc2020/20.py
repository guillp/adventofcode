from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import Enum
from functools import cache

TILE_SIZE = 10


class Direction(complex, Enum):
    UP = -1j
    RIGHT = 1
    DOWN = 1j
    LEFT = -1


class Rotation(complex, Enum):
    NULL = -1j
    CLOCKWISE = 1
    ANTICLOCKWISE = 1j
    HALFTURN = -1


@dataclass(frozen=True)
class Tile:
    id: int = field(hash=True)
    pixels: frozenset[complex] = field(hash=True)
    transformations: str = field(default="", compare=False)
    size: int = field(default=TILE_SIZE, compare=False)

    @classmethod
    def parse(cls, s: str) -> "Tile":
        lines = s.splitlines()
        tile_id = int(lines.pop(0).strip(":").split()[1])
        pixels = frozenset(
            complex(x, y)
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c == "#"
        )
        return Tile(tile_id, pixels)

    @cache
    def rotate(self, rotation: Rotation) -> "Tile":
        if rotation == Rotation.NULL:
            pixels = frozenset(self.pixels)
        if rotation == Rotation.CLOCKWISE:
            pixels = frozenset(coord * 1j + self.size - 1 for coord in self.pixels)
        elif rotation == Rotation.HALFTURN:
            pixels = frozenset(
                coord * -1 + (self.size - 1) * (1 + 1j) for coord in self.pixels
            )
        elif rotation == Rotation.ANTICLOCKWISE:
            pixels = frozenset(
                coord * -1j + (self.size - 1) * 1j for coord in self.pixels
            )

        return Tile(
            self.id,
            pixels,
            self.transformations + " Rot" + str(rotation),
            size=self.size,
        )

    @cache
    def flip(self, horizontal: bool = False, vertical: bool = False) -> "Tile":
        if vertical:
            pixels = frozenset(
                complex(self.size - pos.real - 1, pos.imag) for pos in self.pixels
            )
        elif horizontal:
            pixels = frozenset(
                complex(pos.real, self.size - pos.imag - 1) for pos in self.pixels
            )
        else:
            pixels = frozenset(self.pixels)
        return Tile(
            self.id,
            pixels,
            self.transformations + " Flip" + ("H" if horizontal else "V"),
            size=self.size,
        )

    @cache
    def border(self, side: Direction) -> str:
        if side == Direction.UP:
            return "".join(
                "#" if complex(x, 0) in self.pixels else "." for x in range(self.size)
            )
        if side == Direction.RIGHT:
            return "".join(
                "#" if complex(self.size - 1, y) in self.pixels else "."
                for y in range(self.size)
            )
        if side == Direction.DOWN:
            return "".join(
                "#" if complex(x, self.size - 1) in self.pixels else "."
                for x in range(self.size)
            )
        if side == Direction.LEFT:
            return "".join(
                "#" if complex(0, y) in self.pixels else "." for y in range(self.size)
            )

    def __repr__(self) -> str:
        return f"Tile {self.id}{self.transformations}"

    def __iter__(self) -> Iterator[tuple[bool, ...]]:
        for y in range(0, self.size):
            yield tuple(complex(x, y) in self.pixels for x in range(0, self.size))

    def __str__(self) -> str:
        return (
            repr(self)
            + ":\n"
            + "\n".join(
                "".join("#" if pixel else "." for pixel in line) for line in self
            )
        )


def solve(content: str) -> Iterator[int]:
    tiles = [Tile.parse(lines) for lines in content.strip().split("\n\n")]
    IMAGE_SIZE = int(len(tiles) ** 0.5)

    @cache
    def next_tile(tile: Tile, side: Direction) -> Tile | None:
        border = tile.border(side)
        other_side = -side  # joy of well-chosen complex numbers
        return next(
            (
                transformed_other_tile
                for other_tile in tiles
                if other_tile.id != tile.id
                for transformed_other_tile in (
                    other_tile.rotate(rotation).flip(h, v)
                    for rotation in Rotation
                    for h, v in ((False, False), (True, False), (False, True))
                )
                if transformed_other_tile.border(other_side) == border
            ),
            None,
        )

    def find_corners() -> Iterable[Tile]:
        for tile in tiles:
            up = next_tile(tile, Direction.UP)
            right = next_tile(tile, Direction.RIGHT)
            down = next_tile(tile, Direction.DOWN)
            left = next_tile(tile, Direction.LEFT)

            if sum(side is None for side in (up, right, down, left)) == 2:
                yield tile

    corners = list(find_corners())
    m = 1
    for tile in corners:
        m *= tile.id
    yield m

    def recompose_image() -> Tile:
        grid: dict[tuple[int, int], Tile] = {}
        tile: Tile | None = None
        for y in range(IMAGE_SIZE):
            for x in range(IMAGE_SIZE):
                if x == y == 0:
                    tile = corners[0]
                    while next_tile(tile, Direction.UP) or next_tile(
                        tile, Direction.LEFT
                    ):
                        tile = tile.rotate(Rotation.CLOCKWISE)
                elif x == 0:
                    tile = next_tile(grid[x, y - 1], Direction.DOWN)
                else:
                    tile = next_tile(grid[x - 1, y], Direction.RIGHT)
                assert tile is not None, (x, y)
                grid[(x, y)] = tile

        image = Tile(
            0,
            frozenset(
                pos - complex(1, 1) + complex(x * (TILE_SIZE - 2), y * (TILE_SIZE - 2))
                for x in range(IMAGE_SIZE)
                for y in range(IMAGE_SIZE)
                for pos in grid[x, y].pixels
                if pos.real not in (0, TILE_SIZE - 1)
                and pos.imag not in (0, TILE_SIZE - 1)
            ),
            size=(TILE_SIZE - 2) * IMAGE_SIZE,
        )
        return image

    image = recompose_image()
    # print(image.rotate(CLOCKWISE).flip(vertical=True))

    def find_sea_monsters(image: Tile) -> Iterator[tuple[complex, bool, bool, int, int]]:
        for rotation in (
            Rotation.NULL,
            Rotation.CLOCKWISE,
            Rotation.HALFTURN,
            Rotation.ANTICLOCKWISE,
        ):
            for hflip, vflip in ((False, False), (True, False), (False, True)):
                lines = list(image.rotate(rotation).flip(hflip, vflip))
                for y, (line1, line2, line3) in enumerate(
                    zip(lines, lines[1:], lines[2:])
                ):
                    for x in range(0, image.size - 20):
                        if all(
                            line1[x + 18 : x + 19]
                            + line2[x : x + 1]
                            + line2[x + 5 : x + 7]
                            + line2[x + 11 : x + 13]
                            + line2[x + 17 : x + 20]
                            + line3[x + 1 : x + 2]
                            + line3[x + 4 : x + 5]
                            + line3[x + 7 : x + 8]
                            + line3[x + 10 : x + 11]
                            + line3[x + 13 : x + 14]
                            + line3[x + 16 : x + 17]
                        ):
                            yield rotation, hflip, vflip, x, y

    nb_pixels = sum(sum(line) for line in image)

    for rotation, hflip, vflip, x, y in find_sea_monsters(image):
        # print(rotation, hflip, vflip, x, y)
        # print(image.rotate(rotation).flip(hflip, vflip))
        nb_pixels -= 15
    yield nb_pixels


test_content = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

assert tuple(solve(test_content)) == (20899048083289, 273)

with open("20.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
