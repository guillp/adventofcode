def loop(value: int, subject: int) -> int:
    value *= subject
    value %= 20201227
    return value


def solve(content: str) -> int:
    public_keys = set(int(line) for line in content.splitlines())

    door_loop_size = 0
    door_candidate_public_key = 1
    while door_candidate_public_key not in public_keys:
        door_candidate_public_key = loop(door_candidate_public_key, 7)
        door_loop_size += 1

    card_public_key = (public_keys - {door_candidate_public_key}).pop()
    encryption_key = 1
    for _ in range(door_loop_size):
        encryption_key = loop(encryption_key, card_public_key)

    return encryption_key


with open("25.txt") as f:
    content = f.read()

print(solve(content))
