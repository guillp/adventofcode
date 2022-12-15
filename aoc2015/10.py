content = "1321131112"

import re


def look_and_say(s: str) -> str:
    groups = re.findall(r"1+|2+|3+", s)
    return "".join(f"{len(group)}{group[0]}" for group in groups)


for i in range(40):
    content = look_and_say(content)

print(len(content))


for i in range(10):
    content = look_and_say(content)

print(len(content))
