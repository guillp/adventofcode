# this is the python equivalent code for my input
def python_equivalent(a: int) -> None:
    d = a + 643 * 4

    while True:
        a = d
        while a:
            a, c = divmod(a, 2)
            if c == 1:
                print(0, end="")
            else:
                print(1, end="")


def solve(n: int) -> int:
    i = 0
    while i < n:
        i *= 2
        i += 1
        i *= 2
    return i - n


# python_equivalent(find_answer())
print(solve(643 * 4))
