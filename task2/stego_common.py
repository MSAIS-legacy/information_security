RU_TO_EN = {
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "у": "y",
    "х": "x",

    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "Х": "X",
}

EN_TO_RU = {english: russian for russian, english in RU_TO_EN.items()}


def bytes_to_bits(data: bytes) -> list[int]:
    bits = []

    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)

    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError("Количество битов должно быть кратно 8.")

    result = bytearray()

    for i in range(0, len(bits), 8):
        value = 0

        for bit in bits[i:i + 8]:
            value = (value << 1) | bit

        result.append(value)

    return bytes(result)

