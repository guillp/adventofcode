import json

with open('12.txt', "rt") as finput:
    content = finput.read()

doc = json.loads(content)

print(json.dumps(doc, indent=2))

def walk(doc) -> int:
    if isinstance(doc, int):
        yield doc
    elif isinstance(doc, dict):
        for v in doc.values():
            yield from walk(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from walk(v)
    elif isinstance(doc, str):
        pass
    else:
        assert False, doc

s = 0

for i in walk(doc):
    s += i

print(s)


def walk2(doc) -> int:
    if isinstance(doc, int):
        yield doc
    elif isinstance(doc, dict):
        values = list(v for v in doc.values() if isinstance(v, str))
        if "red" not in values:
            for v in doc.values():
                yield from walk2(v)
    elif isinstance(doc, list):
        for v in doc:
            yield from walk2(v)
    elif isinstance(doc, str):
        pass
    else:
        assert False, doc

s2 = 0

for i in walk2(doc):
    s2 += i

print(s2)
