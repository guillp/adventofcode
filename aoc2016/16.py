content = "11100010111110100"


def dragon_curve(content: str, length=272) -> str:
    if len(content) >= length:
        return content[:length]

    return dragon_curve(f'{content}0{"".join("01"[c=="0"] for c in content[::-1])}', length)


def checksum(content: str) -> str:
    if len(content) % 2 == 1:
        return content
    return checksum("".join("01"[a == b] for a, b in zip(content[::2], content[1::2])))


def solve(content: str, length: int = 272) -> str:
    return checksum(dragon_curve(content, length))

assert dragon_curve("10000", 23) == "10000011110010000111110"
assert checksum("10000011110010000111") == "01100"
assert solve("10000", 20) == "01100"

print(solve(content))
print(solve(content, 35651584))