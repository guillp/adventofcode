def part1(content: str) -> int:
    files = {}
    freespace = {}
    blocks = 0
    for i, c in enumerate(map(int, content.strip())):
        if i % 2:
            if c > 0:
                freespace[blocks] = c
        else:
            files[blocks, c] = i // 2
        blocks += c

    while freespace:
        start_block, file_size = max(files)
        new_start_block = min(freespace)
        if new_start_block > start_block:
            break

        file_id = files.pop((start_block, file_size))
        space = freespace.pop(new_start_block)

        if file_size - space < 0:  # more free space than required
            freespace[new_start_block + file_size] = space - file_size
            files[new_start_block, file_size] = file_id
        else:  # file fits perfectly
            files[new_start_block, space] = file_id
        if file_size - space > 0:  # some data leftover
            files[start_block + space, file_size - space] = file_id
            freespace[start_block] = space
        else:
            freespace[start_block] = file_size

    # files = {x: files[x] for x in sorted(files)}
    return sum(
        block * file_id
        for (start_block, file_size), file_id in files.items()
        for block in range(start_block, start_block + file_size)
    )


def part2(content: str) -> int:
    files = {}
    freespace = {}
    blocks = 0
    for i, size in enumerate(map(int, content.strip())):
        if i % 2:
            if size > 0:
                freespace[blocks] = size
        else:
            files[i // 2] = blocks, size
        blocks += size

    for file_id in sorted(files, reverse=True):
        start_block, file_size = files[file_id]
        for new_start_block in sorted(freespace):
            free_space = freespace[new_start_block]
            if free_space >= file_size:
                break
        else:
            continue

        if new_start_block > start_block:
            continue

        files[file_id] = new_start_block, file_size
        freespace.pop(new_start_block)

        if file_size - free_space < 0:  # more free space than required
            freespace[new_start_block + file_size] = free_space - file_size

        # merge next free block into emptied space
        for free_block, size in freespace.items():
            if free_block == start_block + file_size:
                freespace[start_block] = size + file_size
                freespace.pop(free_block)
                break
        # merge previous free block into emptied space
        for free_block, size in freespace.items():
            if free_block + size == start_block:
                freespace[free_block] = size + freespace.pop(start_block, 0)
                break

    files = {x: files[x] for x in sorted(files)}
    return sum(
        block * file_id for file_id, (block, file_size) in files.items() for block in range(block, block + file_size)
    )


test_content = "2333133121414131402"

assert part1(test_content) == 1928
assert part2(test_content) == 2858

with open("09.txt") as f:
    content = f.read()

print(part1(content))
print(part2(content))
