from stringparser import Parser
import pandas as pd

with open('16.txt', "rt") as finput:
    content = finput.read()

parser = Parser('Sue {}: {}: {:d}, {}: {:d}, {}: {:d}')

aunts = {}
for line in content.splitlines():
    name, c1, n1, c2, n2, c3, n3 = parser(line)
    aunts[name] = {c1: n1, c2: n2, c3: n3}

df = pd.DataFrame(aunts).transpose()

values = {}
for line in """children: 3
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

for c in ('cats', 'trees'):
    df = df[(df[c] > values.pop(c)) | df[c].isna()]

for c in ('pomeranians', 'goldfish'):
    df = df[(df[c] < values.pop(c)) | df[c].isna()]

for k, v in values.items():
    df = df[(df[k] == v) | df[k].isna()]

print(df.iloc[0].name)