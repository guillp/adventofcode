def part1(content: str, card: int = 2019, N: int = 10007) -> int:
    for line in content.splitlines():
        match line.split():
            case "deal", "into", "new", "stack":
                card = (-card - 1) % N
            case "cut", pos:
                card = (card - int(pos)) % N
            case "deal", "with", "increment", inc:
                card = (card * int(inc)) % N

    return card


def compose(a: int, b: int, c: int, d: int, m: int) -> tuple[int, int]:
    """Given the parameters from:
    - f(x) = a*x + b (mod m)
    - g(x) = c*x + d (mod m)
    Return the parameters from `f(g(x)) = (a*c)*x + (b*c + d) (mod m)`
    """
    return (a * c) % m, (b * c + d) % m


def part2(content: str, card: int = 2020, N: int = 119_315_717_514_047, shuffles: int = 101_741_582_076_661) -> int:
    """Modular arithmetic to the rescue!
    Since all operations are linear (in the form `f(x) = a*x + b (mod m)`),
    and applying a linear transformation to another linear transformation is also linear,
    we can reduce the whole shuffling process to a single linear transformation.
    We'll compute the single transformation for a single backward shuffle, then
    apply it `shuffles` times to get the initial position of the card we're looking for.
    """
    a, b = 1, 0  # start with the identity function parameters (f(x) = 1*x + 0))
    for line in reversed(content.splitlines()):  # apply all transformations backwards
        match line.split():
            case "deal", "into", "new", "stack":
                a, b = compose(a, b, -1, -1, N)
            case "cut", pos:
                a, b = compose(a, b, 1, int(pos), N)
            case "deal", "with", "increment", inc:
                a, b = compose(a, b, pow(int(inc), -1, N), 0, N)

    # We now have the parameters a and b from a single backward shuffling s(x) = a*x + b
    # (x being the card we look for). We need to apply it `shuffles-1` times to itself.
    # According to the same composition rules used above, the multiplier becomes a^shuffles,
    # and the constant term becomes:
    # - after 2 shuffles: b*a+b which equals b* (a+1)
    # - after 3 shuffles: b*(a+1) * a + b which equals b * (a^2 + a + 1)
    # - after 4 shuffles: b*(a^2+a+1) * a + b which equals to b * (a^3 + a^2 + a + 1)
    # - after n shuffles: b * (a^(n-1) + a^(n-2) + ... + a^2 + a + 1)
    # which is a finite geometric series and can be simplified to: b * (1 - a^n) / (1 - a)
    # dividing by (1-a) is the same as multiplying by the inverse of (1-a) which is (1-a)^-1
    # and we need to keep the modulo N in mind at all times.
    return (pow(a, shuffles, N) * card + b * (1 - pow(a, shuffles, N)) * pow(1 - a, -1, N)) % N


assert part1("deal into new stack", 3, 10) == 6
assert part1("deal into new stack", 0, 10) == 9
assert part1("cut 3", 0, 10) == 7
assert part1("cut 3", 3, 10) == 0
assert part1("cut -4", 3, 10) == 7
assert part1("deal with increment 3", 0, 10) == 0
assert part1("deal with increment 3", 1, 10) == 3
assert part1("deal with increment 3", 2, 10) == 6

with open("22.txt") as f:
    content = f.read()

print(part1(content, card=2019, N=10007))
print(part2(content, card=2020, N=119_315_717_514_047, shuffles=101_741_582_076_661))
