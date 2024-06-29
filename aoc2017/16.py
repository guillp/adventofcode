def part1(content: str, programs: str = "abcdefghijklmnop") -> str:
    for move in content.split(","):
        match move[0], *move[1:].split("/"):
            case "s", x_:
                x = int(x_)
                programs = programs[-x:] + programs[:-x]
            case "x", a_, b_:
                a, b = int(a_), int(b_)
                programs = "".join(
                    programs[a] if i == b else programs[b] if i == a else c for i, c in enumerate(programs)
                )
            case "p", a, b:
                programs = "".join(a if c == b else b if c == a else c for c in programs)
    return programs


def part2(content: str) -> str:
    history = []
    programs = "abcdefghijklmnop"
    for i in range(1_000_000_000):
        history.append(programs)
        programs = part1(content, programs)
        if programs in history:
            loop = history.index(programs)
            mod = 1_000_000_000 % (i - loop + 1)
            return history[loop + mod]
    assert False, "Solution not found"


assert part1("s1,x3/4,pe/b", "abcde") == "baedc"

with open("16.txt") as f:
    content = f.read().strip()

print(part1(content))
print(part2(content))
