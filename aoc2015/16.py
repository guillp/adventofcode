import re

import pandas as pd


def solve(content: str, part2: bool = False) -> int:
    aunts = {
        name: {c1: int(n1), c2: int(n2), c3: int(n3)}
        for name, c1, n1, c2, n2, c3, n3 in re.findall(
            r"^Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)$", content, re.MULTILINE
        )
    }

    df = pd.DataFrame(aunts).transpose()

    values = {}
    for line in """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1""".splitlines():
        obj, q = line.split(": ")
        values[obj] = int(q)

    if part2:
        for c in ("cats", "trees"):
            df = df[(df[c] > values.pop(c)) | df[c].isna()]

        for c in ("pomeranians", "goldfish"):
            df = df[(df[c] < values.pop(c)) | df[c].isna()]

    for k, v in values.items():
        df = df[(df[k] == v) | df[k].isna()]

    return int(df.iloc[0].name)  # type: ignore[call-overload, no-any-return]


with open("16.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
