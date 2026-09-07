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
    file_content = response.content

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
put_response = requests.put(upload_link, data=file_content)


# Получает длину файла
file_size = len(file_content)

# Формирует словарь с данными
result_file = {
    "filename": text,
    "size_bytes": file_size}

# Сохраняет данные в JSON-файл
with open("image_size.json", "a", encoding="utf-8") as f:
    json.dump(result_file, f, ensure_ascii=False, indent=4)
