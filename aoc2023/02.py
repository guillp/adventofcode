with open('02.txt') as f: content = f.read()

s = 0
for line in content.splitlines():
    game_part, balls_part = line.split(":")
    game_id = int(game_part.split(" ")[1])

    for subset in balls_part.split(";"):
        max_balls = {"red": 0, "blue": 0, "green": 0}
        for ball in subset.split(","):
            n, color = ball.strip().split(" ")
            max_balls[color] = int(n)

        if max_balls["red"] > 12 or max_balls["green"] > 13 or max_balls['blue'] > 14:
            break
    else:
        s += game_id

print(s)

p = 0
for line in content.splitlines():
    game_part, balls_part = line.split(":")
    game_id = int(game_part.split(" ")[1])
    min_balls = {"red": 0, "blue": 0, "green": 0}

    for subset in balls_part.split(";"):
        for ball in subset.split(","):
            n, color = ball.strip().split(" ")
            if min_balls[color] < int(n):
                min_balls[color] = int(n)
    p += min_balls["red"] * min_balls["green"] * min_balls['blue']

print(p)
