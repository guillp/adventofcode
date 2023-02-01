from collections import defaultdict

with open("10.txt") as f:
    content = f.read()

from stringparser import Parser

bot_parser = Parser("bot {:d} gives low to {} {:d} and high to {} {:d}")
input_parser = Parser("value {:d} goes to bot {:d}")

bots = {}

G = defaultdict(set)

for line in sorted(content.splitlines(), reverse=True):
    if line.startswith("value"):
        val, bot = input_parser(line)
        G[bot].add(val)
    elif line.startswith("bot"):
        bot, low_type, low_num, high_type, high_num = bot_parser(line)
        bots[bot] = (low_type, low_num, high_type, high_num)

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
        print(next(bot for bot, inputs in G.items() if inputs == {61, 17}))

print(outputs[0] * outputs[1] * outputs[2])
