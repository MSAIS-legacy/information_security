import hashlib
import struct


MAGIC = b"GAMMA1"


def make_gamma(salt: bytes, length: int) -> bytes:
    """Создаёт ту же гамму по соли, сохранённой в файле."""
    gamma = bytearray()
    counter = 0

    while len(gamma) < length:
        block = hashlib.sha256(salt + counter.to_bytes(8, "big")).digest()
        gamma.extend(block)
        counter += 1

    return bytes(gamma[:length])


def main() -> None:
    input_name = input("Имя зашифрованного файла [encrypted.bin]: ").strip()
    if not input_name:
        input_name = "encrypted.bin"

    with open(input_name, "rb") as input_file:
        if input_file.read(len(MAGIC)) != MAGIC:
            raise ValueError("Это не файл программы гаммирования")

        salt_length_data = input_file.read(4)
        if len(salt_length_data) != 4:
            raise ValueError("Зашифрованный файл повреждён")

        salt_length = struct.unpack(">I", salt_length_data)[0]
        salt = input_file.read(salt_length)
        if len(salt) != salt_length:
            raise ValueError("Зашифрованный файл повреждён")

        encrypted_text = input_file.read()

    gamma = make_gamma(salt, len(encrypted_text))
    decrypted_bytes = bytes(a ^ b for a, b in zip(encrypted_text, gamma))

    print("Соль:", salt.decode("utf-8"))
    print("Расшифрованный текст:")
    print(decrypted_bytes.decode("utf-8"))


if __name__ == "__main__":
    main()
