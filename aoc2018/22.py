from __future__ import annotations

import heapq
import re
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from functools import cache


class RegionType(str, Enum):
    ROCKY = "."
    WET = "="
    NARROW = "|"


class Equipment(str, Enum):
    CLIMBING_GEAR = "C"
    TORCH = "T"
    NEITHER = "N"


@dataclass(unsafe_hash=True)
class Grid:
    depth: int
    target_x: int
    target_y: int

    @cache
    def geologic_index(self, x: int, y: int) -> int:
        match x, y:
            case 0, 0:
                return 0
            case self.target_x, self.target_y:
                return 0
            case x, 0:
                return x * 16807
            case 0, y:
                return y * 48271
            case x, y:
                return self.erosion_level(x - 1, y) * self.erosion_level(x, y - 1)
            case _:
                assert False

    @cache
    def erosion_level(self, x: int, y: int) -> int:
        return (self.geologic_index(x, y) + self.depth) % 20183

    @cache
    def region_type(self, x: int, y: int) -> RegionType:
        match self.erosion_level(x, y) % 3:
            case 0:
                return RegionType.ROCKY
            case 1:
                return RegionType.WET
            case 2:
                return RegionType.NARROW
        assert False

    def draw(self, width: int, height: int, *path: tuple[int, int]) -> None:
        for y in range(height):
            print("".join(self.region_type(x, y) if (x, y) not in path else "X" for x in range(width)))
        print()

    def risk_level(self) -> int:
        return sum(self.erosion_level(x, y) % 3 for x in range(self.target_x + 1) for y in range(self.target_y + 1))

    @cache
    def possible_equipments(self, x: int, y: int) -> set[Equipment]:
        return {
            RegionType.ROCKY: {Equipment.CLIMBING_GEAR, Equipment.TORCH},
            RegionType.WET: {Equipment.CLIMBING_GEAR, Equipment.NEITHER},
            RegionType.NARROW: {Equipment.TORCH, Equipment.NEITHER},
        }[self.region_type(x, y)]

    def best_time(self, target_x: int, target_y: int) -> int:
        pool = [
            (
                target_x + target_y,  # estimate dist to target
                0,  # duration
                0,  # x
                0,  # y
                Equipment.TORCH,  # current equipment
            ),
        ]
        best_times = dict[tuple[int, int, Equipment], int]()
        while pool:
            _, time, x, y, equipment = heapq.heappop(pool)
            for xn, yn in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not 0 <= xn < target_x + 100 or not 0 <= yn <= target_y + 100:
                    continue
                if equipment not in self.possible_equipments(xn, yn):
                    continue
                if time + 1 < best_times.get((xn, yn, equipment), time + 2):
                    heapq.heappush(
                        pool,
                        (
                            time + abs(target_x - xn) + abs(target_y - yn) + 1 + 7 * (equipment != Equipment.TORCH),
                            time + 1,
                            xn,
                            yn,
                            equipment,
                        ),
                    )
                    best_times[(xn, yn, equipment)] = time + 1
            for next_equipment in self.possible_equipments(x, y) - {equipment}:
                if best_times.get((x, y, next_equipment), target_x * target_y) > time + 7:
                    heapq.heappush(
                        pool,
                        (
                            time + abs(x - target_x) + abs(y - target_y) + 7 + 7 * (next_equipment != Equipment.TORCH),
                            time + 7,
                            x,
                            y,
                            next_equipment,
                        ),
                    )
                    best_times[(x, y, next_equipment)] = time + 7

        return best_times[target_x, target_y, Equipment.TORCH]


def solve(content: str) -> Iterator[int]:
    depth, target_x, target_y = (int(x) for x in re.findall(r"\d+", content, re.MULTILINE))
    grid = Grid(depth=depth, target_x=target_x, target_y=target_y)
    yield grid.risk_level()
    yield grid.best_time(target_x, target_y)


assert tuple(
    solve("""\
depth: 510
target: 10,10
"""),
) == (114, 45)

with open("22.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
