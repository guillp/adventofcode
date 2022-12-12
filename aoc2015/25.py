def codes():
    code = 20151125
    while True:
        yield code
        code *= 252533
        code %= 33554393

row = 2947
column = 3029

target = sum(n for n in range(row + column-1)) + column -1

for i, code in enumerate(codes()):
    if i == target:
        print(code)
        break