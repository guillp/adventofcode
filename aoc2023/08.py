import math
import re
from itertools import cycle

content = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

with open('08.txt') as f: content = f.read()

instructions, _, *nodes = content.splitlines()

G = {}
for node in nodes:
    name, left, right = re.findall(r'\w{3}', node)
    G[name] = (left, right)

pos = "AAA"
for i, instruction in enumerate(cycle(instructions), start=1):
    pos = G[pos][instruction == 'R']  # indexing on boolean is the same as on 0/1
    if pos == "ZZZ":
        print(i)
        break

positions = {pos: (pos, None, None) for pos in G if pos[-1] == 'A'}

for i, instruction in enumerate(cycle(instructions), start=1):
    for start_pos, (current_pos, ttz, loop) in positions.items():
        if loop is None or ttz is None:
            next_pos = G[current_pos][instruction == 'R']
            if next_pos[-1] == 'Z':  # reach destination
                if ttz is not None:
                    loop = i - ttz
                else:
                    ttz = i
            positions[start_pos] = (next_pos, ttz, loop)
    if all(None not in v for v in positions.values()):
        break

for start_pos, (dest_pos, first_seen, loop) in positions.items():
    assert first_seen == loop  # this is verified on I guess all inputs
print(math.lcm(*(v[1] for v in positions.values())))
