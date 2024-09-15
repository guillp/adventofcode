from collections.abc import Iterator


def calc_row_id(seat: str) -> int:
    front = 0
    back = 127
    left = 0
    right = 7
    for char in seat:
        depth = back - front + 1
        width = right - left + 1
        match char:
            case "F":
                back -= depth // 2
            case "B":
                front += depth // 2
            case "L":
                right -= width // 2
            case "R":
                left += width // 2
            case _:
                assert False, "unknown input"
    assert front == back
    assert left == right
    return front * 8 + left


def solve(content: str) -> Iterator[int]:
    seats = {calc_row_id(line) for line in content.strip().splitlines()}
    yield max(seats)
    yield next(
        seat
        for seat in range(min(seats), max(seats) + 1)
        if seat not in seats and seat - 1 in seats and seat + 1 in seats
    )


assert calc_row_id("FBFBBFFRLR") == 357
assert calc_row_id("BFFFBBFRRR") == 567
assert calc_row_id("FFFBBBFRRR") == 119

with open("05.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
