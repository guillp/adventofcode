import stringparser

with open("04.txt", "rt") as finput:
    content = finput.read()

parser = stringparser.Parser("{:d}-{:d},{:d}-{:d}")
pairs = [parser(line) for line in content.splitlines()]

print(sum(a <= c and b >= d or c <= a and d >= b for a, b, c, d in pairs))
print(sum(b >= c >= a or b >= d and a <= c or b >= d >= a or d >= a >= c or d >= b and c <= a or d >= b >= c for a, b, c, d in pairs))
