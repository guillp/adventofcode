from collections.abc import Iterator


class Board:
    def __init__(self, s: str) -> None:
        self.numbers = tuple(tuple(int(x) for x in line.split()) for line in s.splitlines())

    def iter_lines(self) -> Iterator[set[int]]:
        for i in range(5):
            yield set(self.numbers[i])
            yield {self.numbers[r][i] for r in range(5)}

    def all_numbers(self) -> set[int]:
        return {n for numbers in self.numbers for n in numbers}


def solve(content: str) -> Iterator[int]:
    numbers_part, *boards_part = content.strip().split("\n\n")
    numbers = tuple(int(x) for x in numbers_part.split(","))

    boards = {Board(b) for b in boards_part}
    picked = set()
    part1_found = False
    for number in numbers:
        picked.add(number)
        for board in tuple(boards):
            if any(not (line - picked) for line in board.iter_lines()):
                if not part1_found:
                    yield sum(board.all_numbers() - picked) * number
                    part1_found = True
                if len(boards) == 1:
                    yield sum(boards.pop().all_numbers() - picked) * number
                    return
                boards.remove(board)


assert tuple(
    solve("""\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""),
) == (4512, 1924)
with open("04.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
