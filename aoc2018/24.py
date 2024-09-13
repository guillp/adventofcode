from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from itertools import chain, count


class Team(Enum):
    IMMUNE = "immune"
    INFECTION = "infection"


@dataclass(frozen=True, slots=True)
class Group:
    id: int
    team: Team
    hit_points: int
    immune_to: tuple[str, ...]
    weak_to: tuple[str, ...]
    attack_points: int
    attack_type: str
    initiative: int

    def effective_power(self, nb_units: int, boost: int = 0) -> int:
        return nb_units * (self.attack_points + (boost if self.team == Team.IMMUNE else 0))

    def damage_multiplier(self, other: Group) -> int:
        if self.attack_type in other.immune_to:
            return 0
        if self.attack_type in other.weak_to:
            return 2
        return 1

    def damage_dealt(self, nb_self: int, other: Group, boost: int = 0) -> int:
        return self.effective_power(nb_self, boost) * self.damage_multiplier(other)

    def killed_units(self, nb_self: int, other: Group, nb_other: int, boost: int = 0) -> int:
        return min(nb_other, self.damage_dealt(nb_self, other, boost) // other.hit_points)

    def __repr__(self) -> str:
        return f"{self.team.value} {self.id}"


def iter_groups(part: str) -> Iterator[tuple[Group, int]]:
    team = Team.IMMUNE if "Immune System:" in part else Team.INFECTION
    for i, (nb_units, hit_points, immunities_and_weaknesses, attack_points, attack_type, initiative) in enumerate(
        re.findall(
            r"(\d+) units each with (\d+) hit points (.*?) ?with an attack that does (\d+) (.*?) damage at initiative (\d+)",
            part,
            re.MULTILINE,
        )
    ):
        immune_to: tuple[str, ...] = ()
        weak_to: tuple[str, ...] = ()
        for part in immunities_and_weaknesses.strip("()").split("; "):
            if part.startswith("immune to "):
                immune_to = tuple(part.removeprefix("immune to ").split(", "))
            if part.startswith("weak to "):
                weak_to = tuple(part.removeprefix("weak to ").split(", "))
        yield (
            Group(
                id=i + 1,
                team=team,
                hit_points=int(hit_points),
                immune_to=immune_to,
                weak_to=weak_to,
                attack_points=int(attack_points),
                attack_type=attack_type,
                initiative=int(initiative),
            ),
            int(nb_units),
        )


assert next(
    iter_groups("""\
Immune System:
18 units each with 729 hit points (weak to fire; immune to cold, slashing) with an attack that does 8 radiation damage at initiative 10""")
) == (
    Group(
        id=1,
        team=Team.IMMUNE,
        hit_points=729,
        immune_to=("cold", "slashing"),
        weak_to=("fire",),
        attack_points=8,
        attack_type="radiation",
        initiative=10,
    ),
    18,
)


def fight(groups: dict[Group, int], boost: int = 0) -> dict[Group, int]:
    for turn in count(1):
        # target selection
        targets: dict[Group, Group] = {}

        for group in sorted(groups, key=lambda g: (g.effective_power(groups[g], boost), g.initiative), reverse=True):
            nb_units = groups[group]
            if nb_units <= 0:
                continue

            target = max(
                (
                    other_group
                    for other_group in groups
                    if other_group.team != group.team  # attack only a group from the other team
                    and other_group not in targets.values()  # if that group is not already targeted
                    and group.damage_multiplier(other_group) > 0  # and damage can be dealt
                ),
                default=None,
                key=lambda other: (
                    group.damage_dealt(nb_units, other, boost),
                    other.effective_power(groups[other], boost),
                    other.initiative,
                ),
            )
            if target:
                targets[group] = target

        if not targets:  # if no one can attack,
            return groups

        # attack phase
        for group in sorted(groups, key=lambda g: g.initiative, reverse=True):
            nb_units = groups[group]
            target = targets.get(group)
            if target is None or nb_units is None:
                continue
            nb_killed = group.killed_units(nb_units, target, groups[target], boost)
            # print(f"{group} ({nb_units} units) attacks {target} ({groups[target]} units) killing {nb_killed} units")
            groups[target] -= nb_killed

        groups = {group: nb_units for group, nb_units in groups.items() if nb_units > 0}
        if all(group.team == Team.IMMUNE for group in groups) or all(group.team == Team.INFECTION for group in groups):
            return groups

    assert False


def solve(content: str) -> Iterator[int]:
    immune_part, infection_part = content.split("\n\n")

    groups = {g: n for g, n in chain(iter_groups(immune_part), iter_groups(infection_part))}

    yield sum(fight(dict(groups)).values())

    for boost in count(1):
        final_groups = fight(dict(groups), boost)
        if all(g.team == Team.IMMUNE for g in final_groups):
            yield sum(final_groups.values())
            break


test_content = """\
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

assert tuple(solve(test_content)) == (5216, 51)

with open("24.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
