import hashlib

secret = b"ckczppom"


def md5(secret, i) -> str:
    return hashlib.md5(secret + str(i).encode()).hexdigest()


i = 0
while not md5(secret, i).startswith("0" * 5):
    i += 1

print(i)

while not md5(secret, i).startswith("0" * 6):
    i += 1

print(i)
