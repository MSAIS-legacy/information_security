alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

key = input("Введите ключ: ").lower()

if not key or any(c not in alphabet for c in key):
    print("Ошибка: ключ должен содержать только русские буквы!")
    exit()

with open("container.txt", "r", encoding="utf-8") as file:
    text = file.read()

result = ""
j = 0

for c in text:
    if c.lower() in alphabet:
        x = alphabet.index(c.lower())
        y = alphabet.index(key[j % len(key)])

        new = alphabet[(x - y) % len(alphabet)]
        result += new.upper() if c.isupper() else new

        j += 1
    else:
        result += c

print("Расшифрованный текст:", result)