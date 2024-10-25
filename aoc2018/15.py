from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum


class Team(Enum):
    GOBLIN = "G"
    ELF = "E"


@dataclass(slots=True)
class Unit:
    position: complex
    type: Team
    attack_power: int = 3
    hp: int = 200

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def fight(self, grid: dict[complex, str], units: list[Unit]) -> None:
        if not self.is_alive:
            return
        self.move(grid, units)
        self.attack(units)

    def move(self, grid: dict[complex, str], units: list[Unit]) -> None:
        to_visit = deque[tuple[complex, ...]]([(self.position,)])
        visited = dict[complex, tuple[tuple[int, int], ...]]()

        while True:
            next_to_visit = deque[tuple[complex, ...]]()
            targets = list[tuple[complex, ...]]()
            while to_visit:
                path = to_visit.popleft()
                pos = path[-1]
                path_tuple = tuple((int(p.imag), int(p.real)) for p in path)
                if pos in visited and visited[pos] < path_tuple:
                    continue
                visited[pos] = path_tuple
                for next_pos in (pos - 1j, pos - 1, pos + 1, pos + 1j):
                    if next_pos in path:
                        continue
                    match grid.get(next_pos):
                        case None:  # walking out of grid
                            continue
                        case _ if not any(
                            u.position == next_pos for u in units if u.is_alive
                        ):  # walking to a free cell
                            next_to_visit.append((*path, next_pos))
                        case _ if any(
                            u.position == next_pos for u in units if u.type != self.type and u.is_alive
                        ):  # walking to a foe
                            targets.append(path)
            if targets:
                target = min(targets, key=lambda p: (p[-1].imag, p[-1].real))
                if len(target) > 1:
                    self.position = target[1]
                return
            if not next_to_visit:
                break
            to_visit = next_to_visit

    def attack(self, units: list[Unit]) -> None:
        targets = [
            u
            for u in units
            if u.is_alive
            and u.type != self.type
            and u.position in (self.position - 1j, self.position - 1, self.position + 1, self.position + 1j)
        ]
        if not targets:
            return
        target = min(targets, key=lambda u: (u.hp, u.position.imag, u.position.real))
        target.hp -= self.attack_power


def solve(content: str) -> Iterator[int]:
    lines = content.splitlines()
    grid = {complex(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line) if c != "#"}
    rounds, units = fight(grid)
    yield rounds * sum(u.hp for u in units if u.is_alive)

    for elf_attack_power in range(30, 100):
        rounds, units = fight(grid, elf_attack_power, part2=True)
        if all(u.is_alive for u in units if u.type == Team.ELF):
            yield rounds * sum(u.hp for u in units if u.is_alive)
            break


def fight(grid: dict[complex, str], elf_attack_power: int = 3, *, part2: bool = False) -> tuple[int, list[Unit]]:
    units = [Unit(p, Team(c), elf_attack_power if c == "E" else 3) for p, c in grid.items() if c in "EG"]
    rounds = 0
    while True:
        units = sorted(filter(lambda u: u.is_alive, units), key=lambda u: (u.position.imag, u.position.real))
        for unit in units:
            unit.fight(grid, units)
            if part2 and any(u.type == Team.ELF and not u.is_alive for u in units):
                return rounds, units
            if all(not u.is_alive for u in units if u.type == Team.ELF) or all(
                not u.is_alive for u in units if u.type == Team.GOBLIN
            ):
                if unit == units[-1]:  # if it is the last unit to play, this is considered as a full round
                    rounds += 1
                return rounds, units
        rounds += 1


assert tuple(
    solve("""\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
"""),
) == (18740, 1140)


with open("15.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
