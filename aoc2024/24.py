import re
from collections.abc import Iterator


def run(gates: dict[str, tuple[str, str, str]], values: dict[str, int]) -> dict[str, int]:
    gates = gates.copy()
    values = values.copy()
    while gates:
        for output, (left, genre, right) in gates.copy().items():
            if left not in values or right not in values:
                continue
            match genre:
                case "AND":
                    value = values[left] and values[right]
                case "OR":
                    value = values[left] or values[right]
                case "XOR":
                    value = values[left] ^ values[right]
            values[output] = value
            gates.pop(output)

    return values


def to_binary(values: dict[str, int]) -> str:
    return "".join(str(values[gate]) for gate in sorted(values, reverse=True) if gate[0] == "z")


def solve(content: str) -> Iterator[int | str]:
    values_part, gates_part = content.strip().split("\n\n")

    values = {wire: int(value) for wire, value in re.findall(r"^(.{3}): (0|1)$", values_part, re.MULTILINE)}
    gates = {
        output: (left, genre, right)
        for left, genre, right, output in re.findall(
            r"^(.{3}) (AND|OR|XOR) (.{3}) -> (.{3})$",
            gates_part,
            re.MULTILINE,
        )
    }

    binary = to_binary(run(gates, values))
    yield int(binary, 2)

    # The circuit for doing additions is known:
    # see https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif

    wrong_wires = set()
    for output, (left, genre, right) in gates.items():
        if genre == "XOR" and output != "z00":
            # XOR gates must either be connected to outputs but not inputs
            if (output[0] == "z" and (left[0] in "xy" or right[0] in "xy")) or (
                output[0] != "z" and {left[0], right[0]} != {"x", "y"}
            ):
                wrong_wires |= {output}
        elif genre == "OR" and output != "z45":
            # OR gates are never connected to outputs
            if output[0] == "z":
                wrong_wires |= {output}
            # but they must have 2 AND gates as inputs
            if gates[left][1] != "AND":
                wrong_wires |= {left}
            if gates[right][1] != "AND":
                wrong_wires |= {right}
        elif genre == "AND":
            # AND gates are never connected to outputs
            if output[0] == "z":
                wrong_wires |= {output}
            # AND gates must either be connected to both inputs or to none
            if (left[0] == "x" and right[0] != "y") or (left[0] == "y" and right[0] != "x"):
                wrong_wires |= {output}
            # AND gates always outputs to an OR gate (excepted first one)
            if left != "x00":
                for l, g, r in gates.values():
                    if output in {l, r} and g != "OR":
                        wrong_wires |= {output}

    assert len(wrong_wires) == 8
    yield ",".join(sorted(wrong_wires))


test_content = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

assert next(solve(test_content)) == 2024

with open("24.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
