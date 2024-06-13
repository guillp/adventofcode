import re
from collections import Counter


def solve(content: str, search: str = "") -> tuple[int, int]:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    part1 = part2 = 0
    for name, sector_id, checksum in re.findall(r"^(.+)-(\d+)\[(.+)]$", content, re.MULTILINE):
        sector_id = int(sector_id)
        count = Counter(name.replace("-", ""))
        most_common = "".join(l for l, n in sorted(count.most_common(), key=lambda ln: (-ln[1], ln[0]))[:5])
        if most_common == checksum:
            part1 += sector_id
            m = ""
            for c in name:
                if c == "-":
                    m += " "
                else:
                    m += ALPHABET[(ALPHABET.index(c) + sector_id) % 26]
            if search and search in m:
                part2 = sector_id
    return part1, part2


test_content = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

assert solve(test_content)[0] == 1514
assert solve("qzmt-zixmtkozy-ivhz-343[zimth]", "very encrypted name")[1] == 343


with open("04.txt") as f:
    content = f.read()
print(*solve(content, "north"), sep="\n")
