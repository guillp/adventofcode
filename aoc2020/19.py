import re
from functools import cache

content = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

with open("19.txt") as f:
    content = f.read()

rules_str, messages = content.split("\n\n")

rules = dict(rule.split(": ") for rule in rules_str.splitlines())


@cache
def rule(n: int):
    r = rules[str(n)]
    if r.startswith('"'):
        return r.strip('"')
    splitted_rule = r.split()
    for i, n in enumerate(splitted_rule):
        if n != "|":
            splitted_rule[i] = rule(n)
    return "(?:" + "".join(splitted_rule) + ")"


s1 = s2 = 0
for message in messages.splitlines():
    if re.fullmatch(rule(0), message):
        s1 += 1
    else:
        for i in range(1, 100):
            match = re.search(
                f"^{rule(42)}+?{rule(42)}{{{i}}}{rule(31)}{{{i}}}$",
                message,
            )
            if match:
                s2 += 1
                break

print(s1, s1 + s2)
