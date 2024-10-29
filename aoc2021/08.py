def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for line in content.strip().splitlines():
        signals, digits = (
            [frozenset(segment for segment in segments) for segments in part.split()] for part in line.split(" | ")
        )
        for digit in digits:
            if len(digit) in (2, 3, 4, 7):
                part1 += 1
        signals.sort(key=len)
        one = signals[0]
        seven = signals[1]
        four = signals[2]
        two_or_three_or_five = set(signals[3:6])  # digits with 5 segments
        zero_or_six_or_nine = set(signals[6:9])  # digits with 6 segments
        eight = signals[9]

        three = next(digit for digit in two_or_three_or_five if one < digit)  # 3 fully contains 1
        nine = next(digit for digit in zero_or_six_or_nine if four < digit)  # 9 fully contains 4
        five = next(digit for digit in two_or_three_or_five - {three} if digit < nine)  # 9 fully contains 5

        two = (two_or_three_or_five - {three, five}).pop()
        zero = next(digit for digit in zero_or_six_or_nine - {nine} if one < digit)  # 0 fully contains 1
        six = (zero_or_six_or_nine - {zero, nine}).pop()

        decoded = (zero, one, two, three, four, five, six, seven, eight, nine)
        output = "".join(str(decoded.index(digit)) for digit in digits)
        part2 += int(output)

    return part1, part2


assert solve("""\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""") == (26, 61229)

with open("08.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
