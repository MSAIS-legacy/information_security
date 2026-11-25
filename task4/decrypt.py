import random


with open("encrypted.txt", "r", encoding="utf-8") as file:
    salt = file.readline().rstrip("\n")
    encrypted = bytes.fromhex(file.read())

generator = random.Random(salt)
decrypted = bytes(byte ^ generator.randrange(256) for byte in encrypted)

print("Соль:", salt)
print("Расшифрованный текст:")
print(decrypted.decode("utf-8"))
