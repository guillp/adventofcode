content = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

#with open('13.txt') as f: content = f.read()

patterns = content.split('\n\n')
# H = len(rows)
# W = len(rows[0])
# grid = {(x,y): c for y, row in enumerate(rows) for x, c in enumerate(row)}

def find_mirror(pattern: str):
    rows = pattern.splitlines()
    middle_row = len(rows)//2
    for y_mirror in range(middle_row):
        for y in range(middle_row - y_mirror):
            if rows[middle_row-y_mirror-y] != rows[middle_row-y_mirror+y+1]:
                break
        else:
            yield middle_row+y_mirror

        for y in range(middle_row - y_mirror):
            if rows[middle_row + y_mirror - y] != rows[middle_row + y_mirror + y + 1]:
                break
        else:
            yield middle_row + y_mirror

    columns = tuple(
        tuple(row[x] for row in rows)
        for x in range(len(rows))
    )
    middle_column = len(columns)//2
    for x_mirror in range(middle_column):
        for x in range(middle_column - x_mirror):
            if rows[middle_column-x_mirror-x] != rows[middle_column-x_mirror+x+1]:
                break
        else:
            yield middle_column+x_mirror

        for y in range(middle_column - x_mirror):
            if rows[middle_column + x_mirror - x] != rows[middle_column + x_mirror + x + 1]:
                break
        else:
            yield middle_column + x_mirror


for pattern in patterns:
    print(max(find_mirror(pattern))+1)
