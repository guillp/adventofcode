from collections.abc import Iterator
from dataclasses import dataclass
from typing import Literal, Self


def parse(
    content: str,
) -> tuple[dict[str, tuple[tuple[str, Literal["<", ">"], int, str] | str, ...]], list[dict[str, int]]]:
    workflows_chunk, parts_chunk = content.split("\n\n")
    parts: list[dict[str, int]] = [
        {k: int(v) for score in p[1:-1].split(",") for k, v in (score.split("="),)} for p in parts_chunk.splitlines()
    ]

    workflows: dict[str, tuple[tuple[str, Literal["<", ">"], int, str] | str, ...]] = {}
    for w in workflows_chunk.splitlines():
        name, flowstr = w[:-1].split("{")
        tasks: list[str | tuple[str, Literal["<", ">"], int, str]] = []
        for task in flowstr.split(","):
            if ":" in task:
                cond, res = task.split(":")
                if ">" in cond:
                    k, v = cond.split(">")
                    tasks.append((k, ">", int(v), res))
                elif "<" in cond:
                    k, v = cond.split("<")
                    tasks.append((k, "<", int(v), res))
                else:
                    assert False
            else:
                tasks.append(task)
        workflows[name] = tuple(tasks)

    return workflows, parts


def part1(content: str) -> int:
    workflows, parts = parse(content)
    accepted = []
    refused = []
    for part in parts:
        workflow = "in"
        while workflow not in "AR":
            for task in workflows[workflow]:
                match task:
                    case str(k), "<", int(v), str(res):
                        if part[k] < v:
                            workflow = res
                            break
                    case str(k), ">", int(v), str(res):
                        if part[k] > v:
                            workflow = res
                            break
                    case str(wf):
                        workflow = wf
                        break
        match workflow:
            case "A":
                accepted.append(part)
            case "R":
                refused.append(part)
            case _:
                assert False

    return sum(sum(part.values()) for part in accepted)


@dataclass(frozen=True)
class Range:
    xmin: int = 1
    xmax: int = 4000
    mmin: int = 1
    mmax: int = 4000
    amin: int = 1
    amax: int = 4000
    smin: int = 1
    smax: int = 4000

    def split(self, k: str, sign: Literal["<", ">"], value: int) -> tuple[Self, Self]:
        valid = {
            "xmin": self.xmin,
            "xmax": self.xmax,
            "mmin": self.mmin,
            "mmax": self.mmax,
            "amin": self.amin,
            "amax": self.amax,
            "smin": self.smin,
            "smax": self.smax,
        }
        defaults = dict(valid)
        match sign:
            case "<":
                valid[f"{k}max"] = value - 1
                defaults[f"{k}min"] = value
            case ">":
                valid[f"{k}min"] = value + 1
                defaults[f"{k}max"] = value

        return self.__class__(**valid), self.__class__(**defaults)

    def product(self) -> int:
        return (
            (self.xmax - self.xmin + 1)
            * (self.mmax - self.mmin + 1)
            * (self.amax - self.amin + 1)
            * (self.smax - self.smin + 1)
        )


def part2(content: str) -> int:
    workflows, _ = parse(content)

    def dp(wf: str, state: Range) -> Iterator[int]:
        if wf == "R":
            return
        if wf == "A":
            yield state.product()
        else:
            default_range: Range = state
            *branches, default_workflow = workflows[wf]
            assert isinstance(default_workflow, str)
            for k, sign, v, res in branches:  # type: ignore[misc]
                valid, default_range = default_range.split(k, sign, v)
                yield from dp(res, valid)
            yield from dp(default_workflow, default_range)

    return sum(dp("in", Range()))


test_content = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


assert (part1(test_content)) == 19114
assert part2(test_content) == 167409079868000

with open("19.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
