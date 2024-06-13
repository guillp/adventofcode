from collections import defaultdict
from collections.abc import Iterator


def parse(content: str) -> tuple[dict[int, set[int]], dict[int, tuple[str, int, str, int]]]:
    bots: dict[int, tuple[str, int, str, int]] = {}
    G: dict[int, set[int]] = defaultdict(set)
    for line in sorted(content.splitlines(), reverse=True):
        match line.split():
            case "bot", bot, "gives", "low", "to", low_type, low_num, "and", "high", "to", high_type, high_num:
                bots[int(bot)] = (low_type, int(low_num), high_type, int(high_num))
            case "value", val, "goes", "to", "bot", bot:
                G[int(bot)].add(int(val))
    return G, bots


def solve(content: str) -> Iterator[int]:
    G, bots = parse(content)
    outputs = {}

    while any(G.values()):
        for bot, inputs in list(G.items()):
            if len(inputs) == 2:
                low, high = sorted(inputs)
                low_type, low_num, high_type, high_num = bots[bot]
                if low_type == "bot":
                    G[low_num].add(low)
                else:
                    outputs[low_num] = low
                inputs.remove(low)
                if high_type == "bot":
                    G[high_num].add(high)
                else:
                    outputs[high_num] = high
                inputs.remove(high)

        if {61, 17} in G.values():
            yield next(bot for bot, inputs in G.items() if inputs == {61, 17})

    yield outputs[0] * outputs[1] * outputs[2]


with open("10.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
