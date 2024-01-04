
# this is the python equivalent code for my input
def python_equivalent(a: int):
    d = a + 643*4

    while True:
        a = d
        while a:
            a, c = divmod(a, 2)
            if c == 1:
                print(0, end='')
            else:
                print(1, end='')

def find_answer(n: int = 643*4) -> int:
    i = 0
    while i < n:
        i *= 2
        i += 1
        i *= 2
    return i - n

#python_equivalent(find_answer())
print(find_answer())