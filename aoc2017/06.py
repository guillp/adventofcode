def solve(content: str) -> tuple[int, int]:
    blocks = tuple(int(x) for x in content.split())
    no_blocks = len(blocks)
    states = {blocks: 0}
    while True:
        m = max(blocks)
        i = blocks.index(m)
        div, mod = divmod(m, no_blocks)
        blocks = tuple(
            a
            + div  # distribute evenly
            + (n in ((i + j + 1) % no_blocks for j in range(mod)))  # add the remainder to the next banks
            - m * (n == i)  # remove from the redistributed bank
            for n, a in enumerate(blocks)
        )
        if blocks in states:
            return len(states), len(states) - states[blocks]
        states[blocks] = len(states)


assert solve("0 2 7 0") == (5, 4)

with open("06.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
