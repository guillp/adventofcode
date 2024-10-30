def solve(content: str) -> tuple[int, int]:
    part1 = 0
    scores = []
    for line in content.strip().splitlines():
        stack = []
        for char in line:
            match char:
                case "(" | "[" | "{" | "<":
                    stack.append(char)
                case ")" if stack[-1] != "(":
                    part1 += 3
                    break
                case "]" if stack[-1] != "[":
                    part1 += 57
                    break
                case "}" if stack[-1] != "{":
                    part1 += 1197
                    break
                case ">" if stack[-1] != "<":
                    part1 += 25137
                    break
                case ")" | "]" | "}" | ">":
                    stack.pop()
        else:
            score = 0
            for char in stack[::-1]:
                score *= 5
                score += {"(": 1, "[": 2, "{": 3, "<": 4}[char]
            scores.append(score)

    part2 = sorted(scores)[len(scores) // 2]

    return part1, part2


assert solve("""\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""") == (26397, 288957)

with open("10.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
