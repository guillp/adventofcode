import math
from collections import deque
from itertools import count

type Signal = bool
LOW = False
HIGH = True


def solve(content: str, part2: bool = False) -> int:
    flipflops: dict[str, bool] = {}
    conjuctions: dict[str, dict[str, Signal]] = {}
    sources: dict[str, tuple[str, ...]] = {}
    destinations: dict[str, tuple[str, ...]] = {}

    # init all modules
    source: str | None
    for line in content.splitlines():
        source, destination_names = line.split(" -> ")
        source_name = source.lstrip("%&")
        destinations[source_name] = tuple(destination_names.split(", "))
        for dest in destinations[source_name]:
            sources.setdefault(dest, ())
            sources[dest] += (source_name,)
        match source[0]:
            case "%":
                flipflops[source_name] = False
            case "&":
                conjuctions[source_name] = {}

    if part2:
        assert len(sources["rx"]) == 1
        rx_source = sources["rx"][0]
        assert rx_source in conjuctions
        rx_conj_sources: dict[str, list[int]] = {s: [] for s in sources[rx_source]}

    # push the button
    signals: deque[tuple[bool, str, str | None]] = deque()
    low_count = high_count = 0
    for i in count(1):
        signals.append((LOW, "broadcaster", None))

        while signals:
            signal, module, source = signals.popleft()
            # print(f"{source} -{['low', 'high'][signal]}-> {module}")
            if signal is HIGH:
                high_count += 1
            else:
                low_count += 1

            if part2 and signal is HIGH and source in rx_conj_sources:
                rx_conj_sources[source].append(i)
                if all(v for v in rx_conj_sources.values()):
                    return math.lcm(*(v[0] for v in rx_conj_sources.values()))

            if module == "broadcaster":
                new_signal = signal
            elif module in flipflops:
                if signal is HIGH:
                    continue
                if flipflops[module]:
                    flipflops[module] = False
                    new_signal = LOW
                else:
                    flipflops[module] = True
                    new_signal = HIGH
            elif module in conjuctions:
                inputs = conjuctions[module]
                assert source is not None
                inputs[source] = signal
                if all(inputs.get(s, LOW) == HIGH for s in sources[module]):
                    new_signal = LOW
                else:
                    new_signal = HIGH
            else:
                if part2 and module == "rx" and signal is LOW:
                    print("rx", i)
                continue
            for dest in destinations[module]:
                signals.append((new_signal, dest, module))

        if part2 is False and i == 1000:
            return low_count * high_count

    assert False


assert (
    solve("""\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""")
    == 32000000
)
assert (
    solve("""\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""")
    == 11687500
)

with open("20.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
