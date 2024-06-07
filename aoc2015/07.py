from functools import cache


def solve(content: str, part2: bool = False) -> int:
    gates = dict(connection.split(" -> ")[::-1] for connection in content.splitlines())

    @cache
    def evaluate(gate: str) -> int:
        try:
            return int(gate)
        except ValueError:
            op: str = gates[gate]
            if " AND " in op:
                a, b = op.split(" AND ")
                return evaluate(a) & evaluate(b)
            elif " OR " in op:
                a, b = op.split(" OR ")
                return evaluate(a) | evaluate(b)
            elif " LSHIFT " in op:
                a, b = op.split(" LSHIFT ")
                return evaluate(a) << evaluate(b)
            elif " RSHIFT " in op:
                a, b = op.split(" RSHIFT ")
                return evaluate(a) >> evaluate(b)
            elif "NOT" in op:
                a = op.removeprefix("NOT ")
                return ~evaluate(a)
            else:
                return evaluate(op)

    if part2:
        gates["b"] = str(evaluate("a"))
    evaluate.cache_clear()
    return evaluate("a")


with open("07.txt") as f:
    content = f.read()

print(solve(content))
print(solve(content, part2=True))
