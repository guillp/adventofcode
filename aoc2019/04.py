from collections.abc import Iterator
from itertools import pairwise


def solve(content: str) -> Iterator[int]:
    low, high = (int(x) for x in content.split("-"))
    number_range = range(low, high + 1)
    possible_passwords = set()
    for number in number_range:
        password = str(number)
        same_adjcent = False
        for a, b in pairwise(password):
            if b < a:
                break
            if a == b:
                same_adjcent = True
        else:
            if same_adjcent:
                possible_passwords.add(password)

    yield len(possible_passwords)
    yield (
        len(possible_passwords)
        - sum(not any(password.count(c) == 2 for c in password) for password in possible_passwords)
    )


for part in solve("273025-767253"):
    print(part)
