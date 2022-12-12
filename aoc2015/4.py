import hashlib

secret = b'ckczppom'
i = 0

def md5(secret, i) -> str:
    return hashlib.md5(secret+str(i).encode()).hexdigest()

while not md5(secret, i).startswith('000000'):
    i += 1

print(i)