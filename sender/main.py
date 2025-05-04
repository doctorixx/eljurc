import argparse
import json
import os

from pusher import push_file


def split_file(input_file, chunk_size=50 * 1024 * 1024, output_dir=None):
    """
    Разбивает файл на чанки указанного размера

    Args:
        input_file (str): Путь к исходному файлу
        chunk_size (int): Размер чанка в байтах (по умолчанию 50 MB)
        output_dir (str): Директория для сохранения чанков

    Returns:
        list: Список имен созданных файлов
    """
    # Получаем имя файла без пути
    base_name = os.path.basename(input_file)
    file_name, file_ext = os.path.splitext(base_name)

    # Если output_dir не указан, используем текущую директорию
    if output_dir is None:
        output_dir = os.path.dirname(input_file) or '.'

    # Создаем директорию, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Список для хранения имен созданных файлов
    chunk_files = []

    with open(input_file, 'rb') as f:
        chunk_num = 0

        while True:
            # Читаем чанк данных
            chunk_data = f.read(chunk_size)

            # Если данных больше нет, выходим из цикла
            if not chunk_data:
                break

            # Создаем имя файла для чанка
            chunk_filename = f"{file_name}_part{chunk_num:03d}{file_ext}"
            chunk_path = os.path.join(output_dir, chunk_filename)

            # Записываем данные в файл
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk_data)

            # Добавляем имя файла в список
            chunk_files.append(chunk_filename)

            # Увеличиваем счетчик чанков
            chunk_num += 1

    return chunk_files


def create_metadata_json(chunk_files, output_dir, original_filename):
    """
    Создает JSON с информацией о разбитом файле

    Args:
        chunk_files (list): Список имен чанков
        output_dir (str): Директория для сохранения JSON
        original_filename (str): Имя исходного файла
    """
    metadata = {
        "original_file": original_filename,
        "total_parts": len(chunk_files),
        "parts": chunk_files,
        "links": [],
    }

    for part in chunk_files:
        resp = push_file(part)
        metadata['links'].append(resp['url'])

    json_filename = os.path.join(output_dir,
                                 f"{os.path.splitext(os.path.basename(original_filename))[0]}_metadata.json")

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    return json_filename


def main():
    parser = argparse.ArgumentParser(description='Разбить файл на чанки указанного размера и создать JSON-метаданные')
    parser.add_argument('input_file', help='Путь к исходному файлу')
    parser.add_argument('-s', '--size', type=int, default=50, help='Размер чанка в МБ (по умолчанию 50)')
    parser.add_argument('--create', '--create', type=int, default=50, help='Размер чанка в МБ (по умолчанию 50)')
    parser.add_argument('-o', '--output', help='Директория для сохранения результатов')

    args = parser.parse_args()

    # Переводим МБ в байты
    chunk_size = args.size * 1024 * 1024

    print(f"Разбиваем файл {args.input_file} на чанки по {args.size} МБ...")

    # Разбиваем файл на чанки
    chunk_files = split_file(args.input_file, chunk_size, args.output)

    print(f"Файл разбит на {len(chunk_files)} чанков")

    # Создаем JSON с метаданными
    json_file = create_metadata_json(chunk_files, args.output or os.path.dirname(args.input_file) or '.',
                                     args.input_file)

    print(f"Метаданные сохранены в файл {json_file}")

    # Выводим общую информацию
    print(f"\nИнформация о разбиении:")
    print(f"Исходный файл: {args.input_file}")
    print(f"Размер чанка: {args.size} МБ")
    print(f"Количество чанков: {len(chunk_files)}")
    print(f"Файл метаданных: {json_file}")


if __name__ == "__main__":
    main()
