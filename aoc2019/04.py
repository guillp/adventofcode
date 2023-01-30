possible_passwords = set()
for number in range(273025, 767253):
    password = str(number)
    same_adjcent = False
    for a, b in zip(password, password[1:]):
        if b < a:
            break
        if a == b:
            same_adjcent = True
    else:
        if same_adjcent:
            possible_passwords.add(password)

print(len(possible_passwords))
print(
    len(possible_passwords)
    - sum(
        not any(password.count(c) == 2 for c in password)
        for password in possible_passwords
    )
)
