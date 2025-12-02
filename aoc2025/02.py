def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for id_range in content.split(","):
        low, high = map(int, id_range.split("-"))
        for product_id in map(str, range(low, high + 1)):
            nb_digits = len(product_id)
            for nb_repeats in range(2, nb_digits + 1):
                if product_id[: nb_digits // nb_repeats] * nb_repeats == product_id:
                    if nb_repeats == 2:
                        part1 += int(product_id)
                    part2 += int(product_id)
                    break

    return part1, part2


test_content = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""

assert solve(test_content) == (1227775554, 4174379265)

with open("02.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
