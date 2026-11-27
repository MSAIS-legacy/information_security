import argparse
from pathlib import Path

from tasks.task2.stego_common import RU_TO_EN, EN_TO_RU, bytes_to_bits


SECRET_ENCODING = "cp1251"
CONTAINER_ENCODING = "utf-8"


def hide_message(
    container_path: str,
    secret_path: str,
    output_path: str,
) -> None:
    container_path = Path(container_path)
    secret_path = Path(secret_path)
    output_path = Path(output_path)

    if container_path.resolve() == output_path.resolve():
        raise ValueError(
            "Исходный контейнер и заполненный контейнер "
            "должны быть разными файлами."
        )

    container_text = container_path.read_text(
        encoding=CONTAINER_ENCODING
    )

    secret_text = secret_path.read_text(
        encoding=SECRET_ENCODING
    )

    try:
        secret_bytes = secret_text.encode(SECRET_ENCODING)
    except UnicodeEncodeError as error:
        raise ValueError(
            "Секретный текст содержит символы, "
            "которые нельзя представить в кодировке Windows-1251."
        ) from error

    if b"\x00" in secret_bytes:
        raise ValueError("Сообщение не должно содержать нулевой байт.")

    if any(char in EN_TO_RU for char in container_text):
        raise ValueError(
            "Исходный контейнер не должен содержать латинские буквы-аналоги."
        )

    message_bits = bytes_to_bits(secret_bytes)

    result = []
    bit_index = 0

    for char in container_text:
        if bit_index >= len(message_bits):
            result.append(char)
            continue

        if char not in RU_TO_EN:
            result.append(char)
            continue

        bit = message_bits[bit_index]

        if bit == 1:
            result.append(RU_TO_EN[char])
        else:
            result.append(char)

        bit_index += 1

    output_path.write_text(
        "".join(result),
        encoding=CONTAINER_ENCODING,
    )

    print("Сообщение успешно скрыто.")
    print(f"Размер сообщения: {len(secret_bytes)} байт")
    print(f"Количество битов сообщения: {len(message_bits)}")
    print(f"Всего использовано символов контейнера: {len(message_bits)}")
    print(f"Результат: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Скрытие текстовой информации в текстовом "
            "контейнере методом замены русских букв "
            "на визуально похожие латинские."
        )
    )

    parser.add_argument(
        "container",
        help="Файл исходного текстового контейнера",
    )

    parser.add_argument(
        "secret",
        help="Файл со скрываемым сообщением",
    )

    parser.add_argument(
        "output",
        help="Новый файл заполненного контейнера",
    )

    args = parser.parse_args()

    hide_message(
        args.container,
        args.secret,
        args.output,
    )


if __name__ == "__main__":
    main()
