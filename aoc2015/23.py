
content = '''inc a
jio a, +2
tpl a
inc a
'''

with open('23.txt', "rt") as finput:
    content = finput.read()

registers = {'a': 1, 'b': 0}

i = 0

instructions = content.splitlines()

while i < len(instructions):
    line = instructions[i]
    if line.startswith('hlf'):
        register = line.split()[1]
        registers[register] //= 2
    elif line.startswith('tpl'):
        register = line.split()[1]
        registers[register] *= 3
    elif line.startswith('inc'):
        register = line.split()[1]
        registers[register] += 1
    elif line.startswith('jmp'):
        offset = int(line.split()[1])
        i += offset -1
    elif line.startswith('jie'):
        register, offset = line.split()[1:3]
        register = register.strip(',')
        offset = int(offset)
        if registers[register] % 2 == 0:
            i += offset -1
    elif line.startswith('jio'):
        register, offset = line.split()[1:3]
        register = register.strip(',')
        offset = int(offset)
        if registers[register] == 1:
            i += offset - 1

    i+=1

print(registers)