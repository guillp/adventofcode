import re

with open("18.txt") as f:
    content = f.read()


def evaluate(operation: str, advanced: bool = False) -> int:
    operation = operation.replace(" ", "")
    while "(" in operation:
        operation = re.sub(
            r"\(([^\(]+?)\)",
            lambda m: str(evaluate(m.group(1), advanced)),
            operation,
            count=1,
        )
    while advanced and "+" in operation:
        operation = re.sub(
            r"\d+[+]\d+", lambda m: str(eval(m.group(0))), operation, count=1
        )
    while "+" in operation or "*" in operation:
        operation = re.sub(
            r"\d+[+*]\d+", lambda m: str(eval(m.group(0))), operation, count=1
        )
    return int(operation)


print(sum(evaluate(operation) for operation in content.splitlines()))
print(sum(evaluate(operation, True) for operation in content.splitlines()))
