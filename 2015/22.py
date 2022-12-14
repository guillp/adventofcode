from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Spell:
    name: str
    cost: int
    damage: int = 0
    armor: int = 0
    health: int = 0
    mana: int = 0
    effect: int = 0

    def __eq__(self, other):
        return self.name == other.name


spells = (
    Spell("Magic Missile", 53, damage=4),
    Spell("Drain", 73, damage=2, health=2),
    Spell("Shield", 113, armor=7, effect=6),
    Spell("Poison", 173, damage=3, effect=6),
    Spell("Recharge", 229, mana=101, effect=5),
)


@dataclass(unsafe_hash=True)
class GameState:
    boss_health: int
    boss_damage: int
    health: int
    mana: int
    active_spells: tuple[Spell] = ()
    used_spells: tuple[Spell] = ()
    previous_states: tuple[GameState] = ()
    hard: bool = False

    @property
    def mana_spent(self) -> int:
        return sum(spell.cost for spell in self.used_spells)


# pool = [GameState(14, 8, 10, 250)]  # test
# pool = [GameState(51, 9, 50, 500)]  # part1
pool = [GameState(51, 9, 50, 500, hard=True)]  # part2

s: GameState | None = None
while pool:
    state = min(pool, key=lambda state: (state.boss_health, len(state.used_spells), -state.health, -state.mana))
    pool.remove(state)

    if s and state.mana_spent > s.mana_spent:
        continue

    if state.hard:
        state.health -= 1
        if state.health <= 0:
            continue

    # apply active effects
    for spell in state.active_spells[::]:
        state.health += spell.health
        state.mana += spell.mana
        state.boss_health -= spell.damage

        if spell.effect > 1:
            spell.effect -= 1
        else:
            state.active_spells = tuple(s for s in state.active_spells if s != spell)

    # cast all possible spells, leading to new states
    for spell in spells:
        if spell not in state.active_spells:
            if spell.cost < state.mana:
                new_state = deepcopy(state)
                new_state.mana -= spell.cost
                if spell.effect:
                    new_state.active_spells += (deepcopy(spell),)
                else:
                    new_state.boss_health -= spell.damage
                    new_state.health += spell.health

                new_state.used_spells += (spell,)
                new_state.previous_states += (deepcopy(new_state),)

                # boss turn, apply all active effects again
                armor = 0
                for spell in new_state.active_spells[::]:
                    new_state.health += spell.health
                    new_state.mana += spell.mana
                    new_state.boss_health -= spell.damage
                    armor += spell.armor

                    if spell.effect >= 1:
                        spell.effect -= 1
                    else:
                        new_state.active_spells = tuple(s for s in new_state.active_spells if s != spell)

                if new_state.boss_health <= 0:
                    if s is None or new_state.mana_spent < s.mana_spent:
                        s = new_state
                else:
                    new_state.health -= max(state.boss_damage - armor, 1)
                    if new_state.health > 0:
                        pool.append(new_state)

print(s)
print(s.mana_spent)
