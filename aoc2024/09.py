def solve(content: str) -> tuple[int, int]:
    files = {}
    freespace = {}
    blocks = 0
    for i, c in enumerate(map(int, content.strip())):
        if i % 2:
            freespace[blocks] = c
        else:
            files[blocks, c] = i // 2
        blocks += c

    while freespace:
        start_block, file_size = max(files)
        file_id = files.pop((start_block, file_size))

        new_start_block = min(freespace)
        space = freespace.pop(new_start_block)
        file_size -= space
        if file_size < 0:  # more free space than required
            freespace[new_start_block + space + file_size] = -file_size
            files[new_start_block, file_size + space] = file_id
        else:
            files[new_start_block, space] = file_id
        if file_size > 0:  # some data leftover
            files[start_block + space, file_size] = file_id

    files = {x: files[x] for x in sorted(files)}

    part1 = 0
    for (start_block, file_size), file_id in files.items():
        # print(str(file_id)*file_size,end="")
        for block in range(start_block, start_block + file_size):
            print(f"{block} * {file_id} = {block*file_id}")
            part1 += block * file_id

    return part1, 0


test_content = "2333133121414131402"

# assert tuple(solve(test_content)) == (1928, 0)

with open("09.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)
