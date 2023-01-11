from collections import Counter

from stringparser import Parser

parser = Parser("{}-{:d}[{}]")

content = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

with open("04.txt") as f: content = f.read()

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
s = 0
for line in content.splitlines():
    name, sector_id, checksum = parser(line)
    count = Counter(name.replace("-",""))
    most_common = "".join(l for l, n in sorted(count.most_common(), key=lambda ln: (-ln[1], ln[0]))[:5])
    if most_common == checksum:
        s += sector_id
        shift = sector_id % 26
        m = ""
        for c in name:
            if c == "-":
                m += " "
            else:
                m += ALPHABET[(ALPHABET.index(c)+sector_id)%26]
        #print(m)
        if 'north' in m:
            print(m, sector_id)

print(s)

