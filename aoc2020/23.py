#cups = tuple(int(x) for x in "389125467")
cups = tuple(int(x) for x in "123487596")


def move(cups: tuple[int]) -> tuple[int]:
    current_cup = cups[0:1]
    pickedup_cups = cups[1:4]
    destination_cup = (
        sorted(cup for cup in cups[4:] if cup < current_cup[0])
        or sorted(cup for cup in cups[4:] if cup > current_cup[0])
    )[-1]
    if destination_cup == cups[4]:
        return cups[4:5] + pickedup_cups + cups[5:] + current_cup
    else:
        i = cups.index(destination_cup)
        return cups[4 : i + 1] + pickedup_cups + cups[i + 1 :] + current_cup


cups1 = tuple(cups)
for i in range(100):
    cups1 = move(cups1)

index1 = cups1.index(1)
print("".join(str(c) for c in cups1[index1 + 1 :] + cups1[:index1]))


cups2 = cups + tuple(range(max(cups) + 1, 1000000))

for i in range(100):
    index1 = cups2.index(1)
    print(cups2[0:10], cups2[index1 : index1 + 3], cups2[-5:])
    cups2 = move(cups2)
