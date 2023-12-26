test_content = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

with open('25.txt') as f: content = f.read()

import networkx as nx
import matplotlib.pyplot as plt

def part1(content: str) -> int:
    G = nx.Graph()
    for line in content.splitlines():
        src, dsts = line.split(": ")
        for dst in dsts.split():
            G.add_edge(src, dst)

    nx.draw(G, with_labels=True)
    plt.show()

    for a,b in (("klk", "xgz"), ("nvf", "bvz"), ("cbl", "vmq")):
        G.remove_edge(a,b)

    g1, g2 = (G.subgraph(c) for c in nx.connected_components(G))
    return len(g1.nodes) * len(g2.nodes)


#assert part1(test_content) == 54
print(part1(content))