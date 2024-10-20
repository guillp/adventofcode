from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from heapq import heappop, heappush


@dataclass(kw_only=True, order=True)
class State:
    boss_health: int = field(compare=True)
    boss_damage: int = field(compare=True)
    mana_spent: int = 0
    player_health: int = 50
    player_mana: int = 500
    shield_turns: int = 0
    poison_turns: int = 0
    recharge_turns: int = 0
    armor: int = 0
    parent: State | None = None

    def apply_active_spells(self) -> None:
        self.armor = 0
        if self.shield_turns > 0:
            self.armor = 7
            self.shield_turns -= 1
        if self.poison_turns > 0:
            self.poison_turns -= 1
            self.boss_health -= 3
        if self.recharge_turns > 0:
            self.recharge_turns -= 1
            self.player_mana += 101

    def player_turns(self) -> Iterator[State]:
        self.apply_active_spells()
        if self.player_mana >= 53:
            yield replace(
                self,
                boss_health=self.boss_health - 4,
                mana_spent=self.mana_spent + 53,
                player_mana=self.player_mana - 53,
                parent=self,
            )
        if self.player_mana >= 73:
            yield replace(
                self,
                boss_health=self.boss_health - 2,
                mana_spent=self.mana_spent + 73,
                player_health=self.player_health + 2,
                player_mana=self.player_mana - 73,
                parent=self,
            )
        if self.player_mana >= 113 and self.shield_turns == 0:
            yield replace(
                self,
                mana_spent=self.mana_spent + 113,
                player_mana=self.player_mana - 113,
                shield_turns=6,
                parent=self,
            )
        if self.player_mana >= 173 and self.poison_turns == 0:
            yield replace(
                self,
                mana_spent=self.mana_spent + 173,
                player_mana=self.player_mana - 173,
                poison_turns=6,
                parent=self,
            )
        if self.player_mana >= 229 and self.recharge_turns == 0:
            yield replace(
                self,
                mana_spent=self.mana_spent + 229,
                player_mana=self.player_mana - 229,
                recharge_turns=5,
                parent=self,
            )

    def boss_turn(self) -> None:
        self.apply_active_spells()

        if self.boss_health > 0:
            self.player_health -= max(self.boss_damage - self.armor, 1)


def solve(content: str, *, part2: bool = False, initial_player_health: int = 50, initial_player_mana: int = 500) -> int:
    boss_health, damage = map(int, re.findall(r"\d+", content, re.MULTILINE))
    pool = [
        State(
            boss_health=boss_health,
            boss_damage=damage,
            player_health=initial_player_health,
            player_mana=initial_player_mana,
        ),
    ]

    best_state: State | None = None
    while pool:
        state = heappop(pool)

        if best_state is not None and state.mana_spent > best_state.mana_spent:
            continue

        if part2:
            state.player_health -= 1
            if state.player_health <= 0:
                continue

        for next_state in state.player_turns():
            if next_state.boss_health <= 0:
                if best_state is None or next_state.mana_spent < best_state.mana_spent:
                    best_state = next_state
                continue

            next_state.boss_turn()
            if next_state.player_health <= 0:
                continue

            if next_state.boss_health <= 0:
                if best_state is None or next_state.mana_spent < best_state.mana_spent:
                    best_state = next_state
                continue

            heappush(pool, next_state)

    assert best_state is not None, "Solution not found!"
    return best_state.mana_spent


assert (
    solve(
        """\
        Hit Points: 13
        Damage: 8
        """,
        initial_player_health=10,
        initial_player_mana=250,
    )
    == 226
)

assert (
    solve(
        """\
        Hit Points: 14
        Damage: 8
        """,
        initial_player_health=10,
        initial_player_mana=250,
    )
    == 641
)

with open("22.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
