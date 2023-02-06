m, n = (int(x) for x in input().split())
pixels = {complex(x, y) for y in range(m) for x, c in enumerate(input()) if c == "X"}

asteroids = 0

while pixels:
    open_list = {pixels.pop()}
    asteroid = set()
    while open_list:
        x = open_list.pop()
        for y in (x + 1, x - 1, x + 1j, x - 1j):
            if y in pixels:
                open_list.add(y)
                pixels.remove(y)
    asteroids += 1

print(asteroids)
