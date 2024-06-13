import re
from collections.abc import Iterator


def abba(part: str) -> str | None:
    if len(part) >= 4:
        for a, b, c, d in zip(part, part[1:], part[2:], part[3:], strict=False):
            if a == d and b == c and a != b:
                return a + b
    return None


def supports_tls(addr: str) -> bool:
    for supernet in re.split(r"\[.*?\]", addr):
        if abba(supernet):
            for hypernet in re.findall(r"\[(.*?)\]", addr):
                if abba(hypernet):
                    return False
            return True
    return False


assert supports_tls("abba[mnop]qrst") is True
assert supports_tls("abcd[bddb]xyyx") is False
assert supports_tls("aaaa[qwer]tyui") is False
assert supports_tls("ioxxoj[asdfgh]zxcvbn") is True


def part1(content: str) -> int:
    return sum(supports_tls(line) for line in content.splitlines())


def aba(supernet: str) -> Iterator[str]:
    if len(supernet) >= 3:
        for a, b, c in zip(supernet, supernet[1:], supernet[2:], strict=False):
            if a == c and a != b:
                yield a + b


def supports_ssl(addr: str) -> bool:
    for supernet in re.split(r"\[.*?\]", addr):
        for ab in aba(supernet):
            for hypernet in re.findall(r"\[(.*?)\]", addr):
                if ab[1] + ab in hypernet:
                    return True
    return False


assert supports_ssl("aba[bab]xyz") is True
assert supports_ssl("xyx[xyx]xyx") is False
assert supports_ssl("aaa[kek]eke") is True
assert supports_ssl("zazbz[bzb]cdb") is True


def part2(content: str) -> int:
    return sum(supports_ssl(line) for line in content.splitlines())


with open("07.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
