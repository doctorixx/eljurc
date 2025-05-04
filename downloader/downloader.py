import json

import requests



with open("debian-12.10.0-amd64-netinst_metadata.json", encoding="utf-8") as f:
    data = json.loads(f.read())

# Шаг 1: Скачать все части
for url, part_name in zip(data["links"], data["parts"]):
    print(f"Скачивание {part_name} из {url}")
    response = requests.get(url, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}, data={})
    # print(response.text)
    response.raise_for_status()
    with open(part_name, 'wb') as f:
        f.write(response.content)

# Шаг 2: Объединить части в оригинальный файл
with open(data["original_file"], 'wb') as outfile:
    for part_name in data["parts"]:
        print(f"Добавление {part_name} в {data['original_file']}")
        with open(part_name, 'rb') as infile:
            outfile.write(infile.read())

print("Сборка завершена.")
