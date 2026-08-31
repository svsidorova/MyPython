import io
import json
import requests
import os
from settings import token

# ввод текста
text = input('Ведите текст для картинки: ' )


# Ссылка на сайт с кошками
url = f'https://cataas.com/cat/says/{requests.utils.quote(text)}'
# Папка на Яндекс.Диске, куда сохранять картинки
YANDEX_FOLDER = 'AIEPYAPI-158'


# Читает с веб-страницы
response = requests.get(url)
if response.status_code == 200:
    with open(f"cats/{text}.jpg", "wb") as f:
        f.write(response.content)

# Создает папку на Яндекс диске
params = {'path': YANDEX_FOLDER}
headers = {'authorization': f'OAuth {token}'}
requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                        params=params,
                        headers=headers)

# Пишет файл на Яндекс диск
params = {'path': f'{YANDEX_FOLDER}/{text}'}
response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                        headers=headers,
                        params=params)
upload_link = response.json()['href']

with open(rf'C:\MyPython\cats\{text}.jpg', 'rb') as file:
    requests.put(upload_link, data = file)

# Получает характеристики файла
image_path = rf'C:\MyPython\cats\{text}.jpg'
file_size = os.path.getsize(image_path)

# Формирует словарь с данными
result_file = {
    "filename": image_path,
    "size_bytes": file_size
}

# Сохраняет данные в JSON-файл
with open("image_size.json", "a", encoding="utf-8") as f:
    json.dump(result_file, f, ensure_ascii=False, indent=4)
