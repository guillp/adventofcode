from collections.abc import Iterable


def fft_sum(signal: tuple[int, ...], i: int) -> int:
    s = 0
    for j in range(i + 1):
        s += sum(signal[i + j :: (i + 1) * 4])
        s -= sum(signal[i + (i + 1) * 2 + j :: (i + 1) * 4])
    return s


def fft_phase(signal: tuple[int, ...]) -> Iterable[int]:
    n = len(signal)
    for i in range(n):
        yield abs(fft_sum(signal, i)) % 10


def part1(signal: str, n: int = 100) -> str:
    digits = tuple(int(x) for x in signal)
    for _ in range(n):
        digits = tuple(fft_phase(digits))

    return "".join(str(x) for x in digits[:8])


def part2(content: str, phases: int = 100) -> str:
    offset = int(content[:7])
    signal = content * 10000

    assert offset > len(signal) / 2
    # for any offset > len(signal)/2, the pattern is just offset 0 and the rest of 1
    # so calculating next phase value for such offset is just the sum of all next values
    r = [int(x) for x in signal[offset:]]
    for _ in range(phases):
        # to make it even faster, well sum each value from the end back to offset
        s = 0
        for i in range(1, len(signal) - offset + 1):
            s += r[-i]
            r[-i] = abs(s) % 10
    return "".join(str(x) for x in r[:8])


assert part1("12345678", 4) == "01029498"

with open("16.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
