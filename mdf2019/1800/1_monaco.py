pos = list(range(21))

p = int(input())
for _ in range(int(input())):
    i_, e = input().split()
    i = int(i_)
    if e == "D":
        previous = pos.index(pos[i] - 1)
        pos[previous], pos[i] = pos[i], pos[previous]
    elif e == "I":
        if i == p:
            print("KO")
            break
        else:
            pos = pos[:i] + [p - 1 for p in pos[i:]]
else:
    print(pos[p])
