from collections import deque


def solve(content: str) -> tuple[int, int]:
    stack = deque(tuple(content))
    score = chars_in_garbage = level = 0
    garbage = False
    while stack:
        match stack.popleft():
            case "{" if not garbage:
                level += 1
                score += level
            case "}" if not garbage:
                level -= 1
            case "!" if garbage:
                stack.popleft()
            case "<" if not garbage:
                garbage = True
            case ">" if garbage:
                garbage = False
            case _ if garbage:
                chars_in_garbage += 1
    return score, chars_in_garbage


assert solve("{}") == (1, 0)
assert solve("{{{}}}") == (6, 0)
assert solve("{{},{}}") == (5, 0)
assert solve("{{{},{},{{}}}}") == (16, 0)
assert solve("{<a>,<a>,<a>,<a>}") == (1, 4)
assert solve("{{<ab>},{<ab>},{<ab>},{<ab>}}") == (9, 8)
assert solve("{{<!!>},{<!!>},{<!!>},{<!!>}}") == (9, 0)
assert solve("{{<a!>},{<a!>},{<a!>},{<ab>}}") == (3, 17)


with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
