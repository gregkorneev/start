"""
open_links_windows.py
----------------------

Этот скрипт предназначен для запуска под Windows. Он подключается
к публичному файлу `links.txt` на Яндекс.Диске, считывает список URL‑адресов
и открывает каждую ссылку в новой вкладке браузера. Файл на диске можно
редактировать онлайн, и приложение будет периодически загружать его
содержимое, чтобы обнаруживать новые строки.

Используемый механизм:
* Яндекс.Диск предоставляет REST‑API для получения прямой ссылки на скачивание
  общедоступного файла. Мы обращаемся к эндпоинту
  ``https://cloud-api.yandex.net/v1/disk/public/resources/download``
  с параметром `public_key` равным публичной ссылке на файл. В ответ
  возвращается JSON с ключом ``href``, содержащим действительную ссылку на
  скачивание.
* После получения ``href`` мы загружаем содержимое файла, разбиваем его по
  строкам и открываем каждую непустую строку в браузере. Ссылки,
  которые уже были открыты, повторно не открываются.

Для создания исполняемого файла под Windows можно использовать PyInstaller:

.. code-block:: batch

   pyinstaller --onefile --noconsole open_links_windows.py

После сборки файлы будут находиться в каталоге ``dist``. Скопируйте
``open_links_windows.exe`` и запустите его — Python не потребуется.

"""

import json
import time
import urllib.parse
import urllib.request
import webbrowser
from typing import List

# Публичная ссылка на файл с перечнем URL‑адресов.
# Ранее программа использовала общедоступный файл на Яндекс.Диске, но теперь
# источником служит репозиторий на GitHub. Указываем прямую ссылку на
# соответствующий текстовый файл в репозитории. Для Windows это links_Win.txt.
# Используем raw‑ссылку, чтобы получить чистое содержимое файла без веб‑оболочки.
PUBLIC_LINK = "https://raw.githubusercontent.com/gregkorneev/start/main/links_Win.txt"

# Интервал в секундах между повторными опросами файла
POLL_INTERVAL = 300  # 5 минут

def get_remote_links(public_link: str) -> List[str]:
    """Скачивает список ссылок из удалённого текстового файла.

    Если ссылка указывает на ресурс Яндекс.Диска, используется REST‑API для
    получения прямой ссылки на скачивание. В противном случае скрипт
    предполагает, что ``public_link`` является прямой ссылкой на текстовый
    файл (например, raw‑ссылка GitHub) и скачивает его напрямую. В обоих
    случаях возвращается список непустых строк без комментариев.

    Args:
        public_link: URL или публичная ссылка, по которой доступен текстовый
            файл со списком URL‑адресов.

    Returns:
        Список строк (каждая строка — URL). Если произошла ошибка, возвращается
        пустой список.
    """
    try:
        content: str = ""
        # Проверяем, является ли ссылка ссылкой на Яндекс.Диск. В этом случае
        # необходимо получить временную ссылку на скачивание через API.
        if "disk.yandex" in public_link:
            api_endpoint = (
                "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
                + urllib.parse.urlencode({"public_key": public_link})
            )
            with urllib.request.urlopen(api_endpoint) as response:
                data = json.loads(response.read().decode("utf-8"))
            download_url = data.get("href")
            if not download_url:
                print("Не удалось получить прямую ссылку на скачивание файла")
                return []
            with urllib.request.urlopen(download_url) as f:
                content = f.read().decode("utf-8")
        else:
            # Ссылка указывает на файл напрямую (например, GitHub raw)
            with urllib.request.urlopen(public_link) as f:
                content = f.read().decode("utf-8")
        # Разбиваем текст по строкам и отбираем только непустые строки, игнорируя
        # комментарии (начинающиеся с '#').
        links: List[str] = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                links.append(stripped)
        return links
    except Exception as exc:
        print(f"Ошибка загрузки файла: {exc}")
        return []

def main() -> None:
    """Основная функция: периодически опрашивает файл и открывает новые ссылки."""
    opened: set[str] = set()
    while True:
        links = get_remote_links(PUBLIC_LINK)
        for url in links:
            if url not in opened:
                # Открываем ссылку в новой вкладке
                webbrowser.open_new_tab(url)
                opened.add(url)
                # небольшая пауза, чтобы предотвратить одновременное открытие многих вкладок
                time.sleep(0.5)
        # Ждём заданный интервал и повторяем
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
