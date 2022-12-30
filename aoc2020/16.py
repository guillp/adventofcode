from functools import cache

content = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

with open("16.txt") as f:
    content = f.read()


class Rule:
    def __init__(self, rule: str):
        self.name, ranges = rule.split(": ")
        self.ranges = tuple(
            tuple(int(x) for x in r.split("-")) for r in ranges.split(" or ")
        )

    def __call__(self, number: int) -> bool:
        for bottom, top in self.ranges:
            if bottom <= number <= top:
                return True
        return False

    def __repr__(self):
        return f"{self.name}: {' or '.join(f'{bottom}-{top}' for bottom, top in self.ranges)}"


rules_str, my_ticket_str, nearby_tickets_str = content.split("\n\n")

rules = set(Rule(rule) for rule in rules_str.splitlines())
my_ticket = tuple(int(x) for x in my_ticket_str.splitlines()[1].split(","))
nearby_tickets = tuple(
    tuple(int(x) for x in ticket.split(","))
    for ticket in nearby_tickets_str.splitlines()[1:]
)

s = 0
invalid_tickets = set()
for ticket in nearby_tickets:
    for value in ticket:
        if not any(rule(value) for rule in rules):
            s += value
            invalid_tickets.add(ticket)

print(s)

valid_tickets = set(nearby_tickets) - invalid_tickets


@cache
def evaluate(rule: Rule, i: int) -> bool:
    return all(rule(ticket[i]) for ticket in valid_tickets)


pool = [()]

while pool:
    pool.sort(key=len)
    first_rules = pool.pop()
    i = len(first_rules)
    if i == len(rules):
        m = 1
        for i, rule in enumerate(first_rules):
            if rule.name.startswith("departure"):
                m *= my_ticket[i]
        print(m)
        break
    for rule in rules - set(first_rules):
        if evaluate(rule, i):
            pool.append(first_rules + (rule,))
