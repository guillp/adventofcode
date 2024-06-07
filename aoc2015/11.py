def validate(password: str) -> bool:
    if "i" in password or "o" in password or "l" in password:
        return False
    for a, b, c in zip(password, password[1:], password[2:], strict=False):
        if ord(a) + 1 == ord(b) == ord(c) - 1:
            break
    else:
        return False
    for i, (a, b) in enumerate(zip(password, password[1:], strict=False)):
        if a == b:
            break
    else:
        return False
    for c, d in zip(password[i + 2 :], password[i + 3 :], strict=False):
        if c == d:
            break
    else:
        return False
    return True


assert not validate("hijklmmn")
assert not validate("abbceffg")
assert not validate("abbcegjk")
assert validate("abcdffaa")
assert validate("ghjaabcc")


def rotate(password: str) -> str:
    chars = list(password.encode()[::-1])
    for i, c in enumerate(chars):
        if c == 122:
            chars[i] = 97
        else:
            chars[i] = c + 1
            break
    return bytes(chars[::-1]).decode()


def solve(password: str) -> str:
    while not validate(password):
        password = rotate(password)

    return password


assert solve("abcdefgh") == "abcdffaa"
assert solve("ghijklmn") == "ghjaabcc"

password = "cqjxjnds"

part1 = solve(password)
part2 = solve(rotate(part1))

print(part1)
print(part2)
