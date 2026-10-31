import hashlib
import struct


MAGIC = b"GAMMA1"


def make_gamma(salt: bytes, length: int) -> bytes:
    """Создаёт псевдослучайную гамму нужной длины из соли."""
    gamma = bytearray()
    counter = 0

    while len(gamma) < length:
        block = hashlib.sha256(salt + counter.to_bytes(8, "big")).digest()
        gamma.extend(block)
        counter += 1

    return bytes(gamma[:length])


def main() -> None:
    input_name = input("Имя файла с текстом: ").strip()
    output_name = input("Имя зашифрованного файла [encrypted.bin]: ").strip()
    if not output_name:
        output_name = "encrypted.bin"

    salt_text = input("Введите соль: ")
    salt = salt_text.encode("utf-8")

    with open(input_name, "rb") as input_file:
        plain_text = input_file.read()

    gamma = make_gamma(salt, len(plain_text))
    encrypted_text = bytes(a ^ b for a, b in zip(plain_text, gamma))

    with open(output_name, "wb") as output_file:
        output_file.write(MAGIC)
        output_file.write(struct.pack(">I", len(salt)))
        output_file.write(salt)
        output_file.write(encrypted_text)

    print(f"Готово. Зашифрованные данные записаны в файл: {output_name}")


if __name__ == "__main__":
    main()
