import re
from functools import cache


def solve(content: str) -> tuple[int, int]:
    rules_str, messages = content.split("\n\n")

    rules = dict(rule.split(": ") for rule in rules_str.splitlines())

    @cache
    def rule(n: int) -> str:
        r = rules[str(n)]
        if r.startswith('"'):
            return r.strip('"')
        splitted_rule = r.split()
        for i, m in enumerate(splitted_rule):
            if m != "|":
                splitted_rule[i] = rule(m)
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

    return s1, s1 + s2


with open("19.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
