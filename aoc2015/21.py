from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from operator import attrgetter


@dataclass
class Player:
    health: int
    equipment: Equipment

    def fight(self, damage, armor) -> bool:
        h = o = self.health
        while h > 0 and o > 0:
            o -= max(self.equipment.damage - armor, 1)
            h -= max(damage - self.equipment.defense, 1)
            if o <= 0:
                return True
            if h <= 0:
                return False


@dataclass
class Weapon:
    damage: int
    cost: int

    def __str__(self):
        return f'W:{self.damage}/{self.cost}'

@dataclass
class Armor:
    armor: int
    cost: int

    def __str__(self):
        return f'A:{self.armor}/{self.cost}'

@dataclass
class Ring:
    damage: int
    armor: int
    cost: int

    def __str__(self):
        return f'R:{self.damage}/{self.armor}/{self.cost}'


weapons = (Weapon(4, 8), Weapon(5, 10), Weapon(6, 25), Weapon(7, 40), Weapon(8, 74))
armors = (Armor(0, 0), Armor(1, 13), Armor(2, 31), Armor(3, 53), Armor(4, 75), Armor(5, 102))
rings = (Ring(1, 0, 25), Ring(2, 0, 50), Ring(3, 0, 100), Ring(0, 1, 20), Ring(0, 2, 40), Ring(0, 3, 80))


@dataclass
class Equipment:
    weapon: Weapon
    armor: Armor
    ring1: Ring|None = None
    ring2: Ring|None = None

    @property
    def damage(self) -> int:
        d = self.weapon.damage
        if self.ring1:
            d += self.ring1.damage
        if self.ring2:
            d += self.ring2.damage
        return d

    @property
    def defense(self) -> int:
        a = self.armor.armor
        if self.ring1:
            a += self.ring1.armor
        if self.ring2:
            a += self.ring2.armor
        return a

    @property
    def cost(self) -> int:
        c = self.armor.cost + self.weapon.cost
        if self.ring1:
            c += self.ring1.cost
        if self.ring2:
            c += self.ring2.cost
        return c

    def __str__(self):
        return f"{self.weapon} {self.armor} {self.ring1} {self.ring2} {self.cost}"

def equipments():
    for weapon in weapons:
        for armor in armors:
            yield Equipment(weapon, armor)
            for ring in rings:
                yield Equipment(weapon, armor, ring)
            for ring1, ring2 in combinations(rings, 2):
                yield Equipment(weapon, armor, ring1, ring2)




winning_equipments = []
for equipment in equipments():
    player = Player(100, equipment)
    if player.fight(8, 2):
        winning_equipments.append(equipment)

print(min(winning_equipments, key=attrgetter('cost')))

loosing_equipments = []
for equipment in equipments():
    player = Player(100, equipment)
    if not player.fight(8,2):
        loosing_equipments.append(equipment)

print(max(loosing_equipments, key=attrgetter('cost')))
