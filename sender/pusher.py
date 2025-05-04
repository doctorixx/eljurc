import requests

TOKEN = "..."
DOMAIN = "..."

def push_file(filename):
    url = f"https://edu-storage-1.gounn.ru/storage/upload?token={TOKEN}&domain={DOMAIN}"

    payload = {}
    files = [
        ('userfile',
         ('123.bin', open(filename, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://edu.gounn.ru',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://edu.gounn.ru/',
        'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.json()
