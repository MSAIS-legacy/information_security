alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

text = input("Введите текст: ")
key = input("Введите ключ: ").lower()

if not key or any(c not in alphabet for c in key):
    print("Ошибка: ключ должен содержать только русские буквы!")
    exit()

result = ""
j = 0

for c in text:
    if c.lower() in alphabet:
        x = alphabet.index(c.lower())
        y = alphabet.index(key[j % len(key)])

        new = alphabet[(x + y) % len(alphabet)]
        result += new.upper() if c.isupper() else new

        j += 1
    else:
        result += c

with open("container.txt", "w", encoding="utf-8") as file:
    file.write(result)

print("Текст зашифрован и сохранён в container.txt")