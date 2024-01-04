from collections import deque


def part1(passwd: str, content: str) -> str:
    passwd = list(passwd)
    for line in content.splitlines():
        #print("".join(passwd), line)
        match line.split():
            case "swap", "position", x, "with", "position", y:
                passwd[int(x)], passwd[int(y)] = passwd[int(y)], passwd[int(x)]
            case "swap", "letter", x, "with", "letter", y:
                passwd = [y if c == x else x if c == y else c for c in passwd]
            case "rotate", direction, x, "steps" | "step":
                s = int(x) % len(passwd)
                if direction == "right":
                    passwd = passwd[-s:] + passwd[:-s]
                else:
                    passwd = passwd[s:] + passwd[:s]
            case "rotate", "based", "on", "position", "of", "letter", x:
                i = passwd.index(x)
                passwd = passwd[-1:] + passwd[:-1]
                if i > 0:
                    passwd = passwd[-i:] + passwd[:-i]
                if i >= 4:
                    passwd = passwd[-1:] + passwd[:-1]

            case "reverse", "positions", x, "through", y:
                new_passwd = passwd[: int(x)]
                for i in range(int(y) - int(x) + 1):
                    new_passwd.append(passwd[int(y) - i])
                new_passwd.extend(passwd[int(y) + 1 :])
                passwd = new_passwd
            case "move", "position", x, "to", "position", y:
                c = passwd.pop(int(x))
                passwd.insert(int(y), c)
            case _:
                assert False

    return "".join(passwd)


assert part1("abcde", "swap position 4 with position 0") == "ebcda"
assert part1("ebcda", "swap letter d with letter b") == "edcba"
assert part1("edcba", "reverse positions 0 through 4") == "abcde"
assert part1("abcde", "rotate left 1 step") == "bcdea"
assert part1("bcdea", "move position 1 to position 4") == "bdeac"
assert part1("bdeac", "move position 3 to position 0") == "abdec"
assert part1("abdec", "rotate based on position of letter b") == "ecabd"
assert part1("ecabd", "rotate based on position of letter d") == "decab"

with open("21.txt") as f:
    content = f.read()
print(part1("abcdefgh", content))


def part2(passwd: str, content: str) -> str:
    passwd = list(passwd)
    for line in reversed(content.splitlines()):
        #print("".join(passwd), line)
        match line.split():
            case "swap", "position", x, "with", "position", y:
                passwd[int(x)], passwd[int(y)] = passwd[int(y)], passwd[int(x)]
            case "swap", "letter", x, "with", "letter", y:
                passwd = [y if c == x else x if c == y else c for c in passwd]
            case "rotate", direction, x, "steps" | "step":
                s = int(x) % len(passwd)
                if direction == "left":
                    passwd = passwd[-s:] + passwd[:-s]
                else:
                    passwd = passwd[s:] + passwd[:s]
            case "rotate", "based", "on", "position", "of", "letter", x:
                i = passwd.index(x)
                for _ in range({0: 1, 1:1, 2: 6, 3:2, 4: 7, 5: 3, 6: 0, 7:4, 8: 4}[i]):
                    passwd = passwd[1:]+passwd[:1]
            case "reverse", "positions", x, "through", y:
                new_passwd = passwd[: int(x)]
                for i in range(int(y) - int(x) + 1):
                    new_passwd.append(passwd[int(y) - i])
                new_passwd.extend(passwd[int(y) + 1 :])
                passwd = new_passwd
            case "move", "position", x, "to", "position", y:
                c = passwd.pop(int(y))
                passwd.insert(int(x), c)
            case _:
                assert False

    return "".join(passwd)


for line in content.splitlines():
    assert part2(part1("abcdefgh", line), line) == "abcdefgh", line

print(part2("fbgdceah", content))
