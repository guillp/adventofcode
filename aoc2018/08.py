test_content = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def read_nodes(nums: list[int]) -> tuple[int, int, list[int]]:
    nb_nodes, nb_metadata, *nums = nums
    part1 = 0
    scores = []
    for _ in range(nb_nodes):
        total, score, nums = read_nodes(nums)
        part1 += total
        scores.append(score)
    metadata, nums = nums[:nb_metadata], nums[nb_metadata:]
    value = sum(metadata)
    part1 += value

    if nb_nodes == 0:
        return part1, value, nums

    return part1, sum(scores[m - 1] for m in metadata if 0 < m <= nb_nodes), nums


def solve(content: str) -> tuple[int, int]:
    nums = [int(x) for x in content.strip().split()]
    part1, part2, leftover = read_nodes(nums)
    assert not leftover
    return part1, part2


assert solve(test_content) == (138, 66)

with open("08.txt") as f:
    content = f.read()
for part in solve(content):
    print(part)
