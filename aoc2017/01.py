def solve(content: str, offset: int = 1) -> int:
    return sum(
        int(a) for a, b in zip(content, content[offset:] + content[:offset]) if a == b
    )


assert solve("1122") == 3
assert solve("1111") == 4
assert solve("1234") == 0
assert solve("91212129") == 9

assert solve("1212", 2) == 6
assert solve("1221", 2) == 0
assert solve("123425", 3) == 4
assert solve("123123", 3) == 12
assert solve("12131415", 4) == 4

with open("01.txt") as f:
    content = f.read().strip()

print(solve(content))
print(solve(content, len(content) // 2))
