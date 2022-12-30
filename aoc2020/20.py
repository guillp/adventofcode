from dataclasses import dataclass
from functools import cache
from typing import Iterable, Literal

content = """Tile 2311:
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

with open("20.txt") as f:
    content = f.read()

TILE_SIZE = 10

UP, RIGHT, DOWN, LEFT = -1j, 1, 1j, -1
NULL, CLOCKWISE, ANTICLOCKWISE, HALFTURN = 1, 1j, -1j, -1


@dataclass
class Tile:
    id: int
    pixels: frozenset[complex]
    transformations: str = ""
    size: int = TILE_SIZE

    def __hash__(self):
        return hash((self.id, self.pixels))

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
    def rotate(
        self, rotation: Literal[NULL, CLOCKWISE, ANTICLOCKWISE, HALFTURN]
    ) -> "Tile":
        if rotation == NULL:
            pixels = frozenset(self.pixels)
        if rotation == CLOCKWISE:
            pixels = frozenset(coord * 1j + self.size - 1 for coord in self.pixels)
        elif rotation == HALFTURN:
            pixels = frozenset(
                coord * -1 + (self.size - 1) * (1 + 1j) for coord in self.pixels
            )
        elif rotation == ANTICLOCKWISE:
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
    def border(self, side: Literal[UP, RIGHT, DOWN, LEFT]) -> str:
        if side == UP:
            return "".join(
                "#" if complex(x, 0) in self.pixels else "." for x in range(self.size)
            )
        if side == RIGHT:
            return "".join(
                "#" if complex(self.size - 1, y) in self.pixels else "."
                for y in range(self.size)
            )
        if side == DOWN:
            return "".join(
                "#" if complex(x, self.size - 1) in self.pixels else "."
                for x in range(self.size)
            )
        if side == LEFT:
            return "".join(
                "#" if complex(0, y) in self.pixels else "." for y in range(self.size)
            )

    def __repr__(self):
        return f"Tile {self.id}{self.transformations}"

    def __iter__(self) -> tuple[bool]:
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


tiles = [Tile.parse(lines) for lines in content.strip().split("\n\n")]
IMAGE_SIZE = int(len(tiles) ** 0.5)


@cache
def next_tile(tile: Tile, side: Literal[UP, DOWN, LEFT, RIGHT]) -> set[complex]:
    border = tile.border(side)
    other_side = -side  # joy of well-chosen complex numbers
    return next(
        (
            transformed_other_tile
            for other_tile in tiles
            if other_tile.id != tile.id
            for transformed_other_tile in (
                other_tile.rotate(rotation).flip(h, v)
                for rotation in (NULL, CLOCKWISE, HALFTURN, ANTICLOCKWISE)
                for h, v in ((False, False), (True, False), (False, True))
            )
            if transformed_other_tile.border(other_side) == border
        ),
        None,
    )


def find_corners() -> Iterable[int]:
    for tile in tiles:
        up = next_tile(tile, UP)
        right = next_tile(tile, RIGHT)
        down = next_tile(tile, DOWN)
        left = next_tile(tile, LEFT)

        if sum(side is None for side in (up, right, down, left)) == 2:
            yield tile


corners = list(find_corners())
m = 1
for tile in corners:
    m *= tile.id
print(m)


def recompose_image() -> set[complex]:
    grid = {}
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            if x == y == 0:
                tile = corners[0]
                while next_tile(tile, UP) or next_tile(tile, LEFT):
                    tile = tile.rotate(CLOCKWISE)
            elif x == 0:
                tile = next_tile(grid[x, y - 1], DOWN)
            else:
                tile = next_tile(grid[x - 1, y], RIGHT)
            assert tile, (x, y)
            grid[(x, y)] = tile

    image = Tile(
        0,
        frozenset(
            pos - complex(1, 1) + complex(x * (TILE_SIZE - 2), y * (TILE_SIZE - 2))
            for x in range(IMAGE_SIZE)
            for y in range(IMAGE_SIZE)
            for pos in grid[x, y].pixels
            if pos.real not in (0, TILE_SIZE - 1) and pos.imag not in (0, TILE_SIZE - 1)
        ),
        size=(TILE_SIZE - 2) * IMAGE_SIZE,
    )
    return image


image = recompose_image()
print(image.rotate(CLOCKWISE).flip(vertical=True))


def find_sea_monsters(image: Tile):
    for rotation in (NULL, CLOCKWISE, HALFTURN, ANTICLOCKWISE):
        for hflip, vflip in ((False, False), (True, False), (False, True)):
            lines = list(image.rotate(rotation).flip(hflip, vflip))
            for y, (line1, line2, line3) in enumerate(zip(lines, lines[1:], lines[2:])):
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
    print(rotation, hflip, vflip, x, y)
    # print(image.rotate(rotation).flip(hflip, vflip))
    nb_pixels -= 15
print(nb_pixels)
