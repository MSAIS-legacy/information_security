import random


input_name = input("Имя файла с текстом [text.txt]: ").strip()
if not input_name:
    input_name = "text.txt"

salt = input("Введите соль: ")

with open(input_name, "rb") as file:
    text = file.read()

generator = random.Random(salt)
encrypted = bytes(byte ^ generator.randrange(256) for byte in text)

with open("encrypted.txt", "w", encoding="utf-8") as file:
    file.write(salt + "\n")
    file.write(encrypted.hex())

print("Готово. Результат записан в encrypted.txt")
