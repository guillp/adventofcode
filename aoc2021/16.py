from __future__ import annotations

import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self


def read_int(bits: bytes, offset: int, n: int) -> int:
    return int(bits[offset : offset + n].decode(), 2)


@dataclass
class Packet:
    version: int
    typeid: int
    length: int
    subpackets: tuple[Packet, ...] = ()
    literal: int | None = None

    @classmethod
    def from_bits(cls, bits: bytes, offset: int = 0) -> Self:
        version = read_int(bits, offset, 3)
        typeid = read_int(bits, offset + 3, 3)
        start = offset
        offset += 6
        subpackets = []
        match typeid:
            case 4:
                value = 0
                while read_int(bits, offset, 1) == 1:
                    value = value * 2**4 + read_int(bits, offset + 1, 4)
                    offset += 5
                value = value * 2**4 + read_int(bits, offset + 1, 4)
                offset += 5
                return cls(version=version, typeid=typeid, length=offset - start, literal=value)
            case _:
                match read_int(bits, offset, 1):
                    case 0:
                        length = read_int(bits, offset + 1, 15)
                        offset += 16
                        while length > 0:
                            subpacket = Packet.from_bits(bits, offset)
                            offset += subpacket.length
                            length -= subpacket.length
                            subpackets.append(subpacket)
                        assert length == 0
                    case 1:
                        nb_packets = read_int(bits, offset + 1, 11)
                        offset += 12
                        for _ in range(nb_packets):
                            subpacket = Packet.from_bits(bits, offset)
                            offset += subpacket.length
                            subpackets.append(subpacket)
                return cls(version=version, typeid=typeid, subpackets=tuple(subpackets), length=offset - start)

    @classmethod
    def from_hex(cls, hexa: str) -> Self:
        data = bytes.fromhex(hexa.strip())
        bits = format(int.from_bytes(data, "big", signed=False), "b").encode()
        if len(bits) % 8 != 0:
            bits = b"0" * (8 - (len(bits) % 8)) + bits
        return cls.from_bits(bits)

    @property
    def value(self) -> int:
        match self.typeid:
            case 0:
                return sum(sp.value for sp in self.subpackets)
            case 1:
                return math.prod(sp.value for sp in self.subpackets)
            case 2:
                return min(sp.value for sp in self.subpackets)
            case 3:
                return max(sp.value for sp in self.subpackets)
            case 4:
                assert self.literal is not None
                return self.literal
            case 5:
                assert len(self.subpackets) == 2
                return self.subpackets[0].value > self.subpackets[1].value
            case 6:
                assert len(self.subpackets) == 2
                return self.subpackets[0].value < self.subpackets[1].value
            case 7:
                assert len(self.subpackets) == 2
                return self.subpackets[0].value == self.subpackets[1].value
            case _:
                assert False

    @property
    def version_sum(self) -> int:
        return self.version + sum(p.version_sum for p in self.subpackets)


def solve(content: str) -> Iterator[int]:
    packet = Packet.from_hex(content)
    yield packet.version_sum
    yield packet.value


assert tuple(solve("CE00C43D881120")) == (11, 9)
assert tuple(solve("9C0141080250320F1802104A08")) == (20, 1)

with open("16.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
