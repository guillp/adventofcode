def part1(content: str) -> int:
    for i in range(len(content) - 4):
        if len(set(content[i : i + 4])) == 4:
            return i + 4
    assert False, "Solution not found"


def part2(content: str) -> int:
    for i in range(len(content) - 14):
        if len(set(content[i : i + 14])) == 14:
            return i + 14
    assert False, "Solution not found"


assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert part1("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

assert part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
assert part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
assert part2("nppdvjthqldpwncqszvftbrmjlhg") == 23
assert part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
assert part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26


with open("06.txt") as finput:
    content = finput.read()

print(part1(content))
print(part2(content))
