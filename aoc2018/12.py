def solve(content: str, part2: bool = False) -> int:
    nb_generations: int = 50000000000 if part2 else 20
    initial_state, spreads = content.split("\n\n")
    rules = {
        tuple(c == "#" for c in llcrr): x == "#"
        for spread in spreads.splitlines()
        for llcrr, x in [spread.split(" => ")]
    }
    initial_state_str = initial_state.removeprefix("initial state: ")
    state = frozenset(i for i, c in enumerate(initial_state_str) if c == "#")
    states = {initial_state_str: (0, state)}
    for generation in range(nb_generations):
        state = frozenset(
            i
            for i in range(min(state) - 5, max(state) + 6)
            if rules.get(tuple(i + j in state for j in (-2, -1, 0, 1, 2)))
        )
        state_str = "".join("#" if i in state else "." for i in range(min(state), max(state) + 1))
        if state_str in states:
            loop_gen, loop_state = states[state_str]
            shift = sum(state) - sum(loop_state)
            # print(f"Loop at {state_str}, gen {loop_gen}, shift {shift}")
            return sum(loop_state) + (nb_generations - loop_gen - 1) * shift

        states[state_str] = generation, state

    return sum(state)


test_content = """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""


assert solve(test_content) == 325

with open("12.txt") as f:
    content = f.read()
print(solve(content))
print(solve(content, part2=True))
