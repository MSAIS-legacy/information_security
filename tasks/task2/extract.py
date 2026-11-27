import argparse
from pathlib import Path

from tasks.task2.stego_common import (
    RU_TO_EN,
    EN_TO_RU,
    bits_to_bytes,
)


SECRET_ENCODING = "cp1251"
CONTAINER_ENCODING = "utf-8"


def get_encoded_bit(char: str) -> int | None:
    if char in RU_TO_EN:
        return 0

    if char in EN_TO_RU:
        return 1

    return None


def extract_message(
    container_path: str,
    output_path: str,
) -> None:
    container_path = Path(container_path)
    output_path = Path(output_path)

    secret_bytes = bytearray()
    byte_bits: list[int] = []

    with container_path.open(encoding=CONTAINER_ENCODING) as container:
        while True:
            char = container.read(1)

            bit = get_encoded_bit(char)
            if bit is None:
                continue

            byte_bits.append(bit)
            if len(byte_bits) < 8:
                continue

            byte = bits_to_bytes(byte_bits)
            if byte == b"\x00":
                break

            secret_bytes.extend(byte)
            byte_bits.clear()

    try:
        secret_text = secret_bytes.decode(SECRET_ENCODING)
    except UnicodeDecodeError as error:
        raise ValueError(
            "Не удалось декодировать извлеченное сообщение "
            "как Windows-1251. Возможно, контейнер поврежден."
        ) from error

    output_path.write_text(
        secret_text,
        encoding=SECRET_ENCODING,
    )

    print("Сообщение успешно извлечено.")
    print(f"Размер сообщения: {len(secret_bytes)} байт")
    print(f"Прочитано битов сообщения: {len(secret_bytes) * 8}")
    print(f"Результат сохранен в: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Извлечение скрытого текста из "
            "текстового контейнера."
        )
    )

    parser.add_argument(
        "container",
        help="Заполненный файл-контейнер",
    )

    parser.add_argument(
        "output",
        help="Файл для извлеченного сообщения",
    )

    args = parser.parse_args()

    extract_message(
        args.container,
        args.output,
    )


if __name__ == "__main__":
    main()
