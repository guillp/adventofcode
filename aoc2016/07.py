import re


def abba(part: str) -> str | None:
    if len(part) >= 4:
        for a, b, c, d in zip(part, part[1:], part[2:], part[3:]):
            if a == d and b == c and a != b:
                return a + b


def supports_tls(addr: str) -> bool:
    for supernet in re.split("\[.*?\]", addr):
        if abba(supernet):
            for hypernet in re.findall("\[(.*?)\]", addr):
                if abba(hypernet):
                    return False
            return True
    return False


assert supports_tls("abba[mnop]qrst") is True
assert supports_tls("abcd[bddb]xyyx") is False
assert supports_tls("aaaa[qwer]tyui") is False
assert supports_tls("ioxxoj[asdfgh]zxcvbn") is True


with open("07.txt") as f:
    content = f.read()

print(sum(supports_tls(line) for line in content.splitlines()))


def aba(supernet: str) -> str | None:
    if len(supernet) >= 3:
        for a, b, c in zip(supernet, supernet[1:], supernet[2:]):
            if a == c and a != b:
                yield a + b


def supports_ssl(addr: str) -> bool:
    for supernet in re.split("\[.*?\]", addr):
        for ab in aba(supernet):
            for hypernet in re.findall("\[(.*?)\]", addr):
                if ab[1] + ab in hypernet:
                    return True
    return False


assert supports_ssl("aba[bab]xyz") is True
assert supports_ssl("xyx[xyx]xyx") is False
assert supports_ssl("aaa[kek]eke") is True
assert supports_ssl("zazbz[bzb]cdb") is True


print(sum(supports_ssl(line) for line in content.splitlines()))
