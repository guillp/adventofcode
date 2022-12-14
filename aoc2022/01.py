with open("01.txt", 'rt') as finput: content = finput.read()

calories = [sum(int(x) for x in elf.split()) for elf in content.split("\n\n")]
print(sum(sorted(calories)[-3:]))
