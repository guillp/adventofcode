from functools import cache

with open("07.txt", "rt") as finput:
    content = finput.read()

gates = dict(connection.split(" -> ")[::-1] for connection in content.splitlines())


@cache
def evaluate(gate):
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


print(evaluate("a"))

gates["b"] = str(evaluate("a"))
evaluate.cache_clear()
print(evaluate("a"))
