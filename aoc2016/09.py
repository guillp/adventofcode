import re
from typing import Iterable


def decompress(data: str) -> Iterable[str]:
    while data:
        match = re.search(r"^(.*?)\((\d+)x(\d+)\)(.*)$", data)
        if match:
            left, width, repeats, right = match.groups()
            width = int(width)
            repeats = int(repeats)
            yield left
            yield right[:width] * repeats
            data = right[width:]
        else:
            yield data
            data = ""


assert "".join(decompress("ADVENT")) == "ADVENT"
assert "".join(decompress("A(1x5)BC")) == "ABBBBBC"
assert "".join(decompress("(3x3)XYZ")) == "XYZXYZXYZ"
assert "".join(decompress("A(2x2)BCD(2x2)EFG")) == "ABCBCDEFEFG"
assert "".join(decompress("(6x1)(1x3)A")) == "(1x3)A"
assert "".join(decompress("X(8x2)(3x3)ABCY")) == "X(3x3)ABC(3x3)ABCY"

with open("09.txt") as f:
    content = f.read()

message = "".join(decompress(content))
print(len(message))


# TODO: there is a better and faster way to do this...
def decompress2(data: str) -> Iterable[int]:
    while data:
        match = re.search(r"^(.*?)\((\d+)x(\d+)\)(.*)$", data)
        if match:
            left, width, repeats, right = match.groups()
            width = int(width)
            repeats = int(repeats)
            yield len(left)
            yield from decompress2(right[:width] * repeats)
            data = right[width:]
        else:
            yield len(data)
            data = ""


assert (
    sum(decompress2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")) == 445
)

print(sum(decompress2(content)))
