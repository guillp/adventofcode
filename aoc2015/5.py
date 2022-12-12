import pandas as pd

with open('5.txt', 'rt') as finput:
    content = finput.read()

df = pd.Series(content.splitlines()).to_frame('string')


def is_nice(s: str) -> bool:
    return (
            sum(letter in 'aeiou' for letter in s) >= 3
            and any(a == b for a, b in zip(s, s[1:]))
            and not any(seq in s for seq in ('ab', 'cd', 'pq', 'xy'))
    )


df['part1'] = df.string.apply(is_nice)

print(df.part1.sum())


def cond1(s: str) -> str:
    for i in range(len(s) - 1):
        if s[i:i + 2] in s[:i] or s[i:i + 2] in s[i + 2:]:
            return s[i:i + 2]


def cond2(s: str) -> str:
    for a, b in zip(s, s[2:]):
        if a == b:
            return a


df['cond1'] = df.string.apply(cond1)
df['cond2'] = df.string.apply(cond2)
df['part2'] = ~df.cond1.isna() & ~df.cond2.isna()

print(df.part2.sum())
