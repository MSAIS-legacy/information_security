import os
import json
import sys

HASH_FILE_NAME = ".disk_hashes.json"


def calculate_hash(file_path):
    result = 0

    with open(file_path, "rb") as file:
        while True:
            block = file.read(2)

            if not block:
                break

            if len(block) == 1:
                block += b"\x00"

            value = int.from_bytes(block, byteorder="little")

            result ^= value

    return result


def scan_directory(root_directory):
    hashes = {}

    for current_directory, _, files in os.walk(root_directory):
        for file_name in files:

            if file_name == HASH_FILE_NAME:
                continue

            full_path = os.path.join(current_directory, file_name)

            relative_path = os.path.relpath(full_path, root_directory)

            try:
                file_hash = calculate_hash(full_path)
                hashes[relative_path] = file_hash
            except (PermissionError, OSError) as error:
                print(f"Не удалось прочитать файл: {relative_path}")
                print(f"Причина: {error}")
    return hashes


def save_hashes(root_directory, hashes):
    hash_file_path = os.path.join(root_directory, HASH_FILE_NAME)

    with open(hash_file_path, "w", encoding="utf-8") as file:
        json.dump(hashes, file, ensure_ascii=False, indent=4)


def load_hashes(root_directory):
    hash_file_path = os.path.join(root_directory, HASH_FILE_NAME)

    with open(hash_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_integrity(old_hashes, new_hashes):
    old_files = set(old_hashes.keys())
    new_files = set(new_hashes.keys())

    added_files = new_files - old_files
    deleted_files = old_files - new_files

    common_files = old_files & new_files

    changed_files = []

    for file_path in common_files:
        if old_hashes[file_path] != new_hashes[file_path]:
            changed_files.append(file_path)

    return (
        sorted(added_files),
        sorted(deleted_files),
        sorted(changed_files),
    )


def print_results(added, deleted, changed):
    if not added and not deleted and not changed:
        print("Изменений не обнаружено.")
        print("Целостность каталога не нарушена.")
        return

    if added:
        print("Добавленные файлы:")
        for file_path in added:
            print(f"  + {file_path}")

    if deleted:
        print("\nУдалённые файлы:")
        for file_path in deleted:
            print(f"  - {file_path}")

    if changed:
        print("\nИзменённые файлы:")
        for file_path in changed:
            print(f"  * {file_path}")


def main():
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = os.getcwd()

    root_directory = os.path.abspath(root_directory)

    if not os.path.isdir(root_directory):
        print(f"Ошибка: каталог не существует: {root_directory}")
        return

    print(f"Проверяемый каталог: {root_directory}")

    hash_file_path = os.path.join(root_directory, HASH_FILE_NAME)

    if not os.path.exists(hash_file_path):
        print("Файл ХЭШ-кодов не найден.")
        print("Выполняется первоначальное сканирование...")

        hashes = scan_directory(root_directory)
        save_hashes(root_directory, hashes)

        print(f"\nПросканировано файлов: {len(hashes)}")
        print(f"Файл ХЭШ-кодов создан:")
        print(hash_file_path)

        return

    print("Файл ХЭШ-кодов найден.")
    print("Выполняется проверка целостности...")

    try:
        old_hashes = load_hashes(root_directory)
    except (json.JSONDecodeError, OSError) as error:
        print("Ошибка чтения файла ХЭШ-кодов.")
        print(error)
        return

    new_hashes = scan_directory(root_directory)

    added, deleted, changed = check_integrity(
        old_hashes,
        new_hashes,
    )

    print_results(added, deleted, changed)


if __name__ == "__main__":
    main()