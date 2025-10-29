"""
open_links_macos.py
--------------------

Эта версия скрипта предназначена для macOS. Она похожа на
`open_links_windows.py`, но использует другую публичную ссылку на файл
`links.txt` и создаётся обычной программой, которую можно собрать через
PyInstaller под macOS. Скрипт регулярно скачивает текстовый файл с
Яндекс.Диска, читает строки и открывает новые URL‑адреса в браузере.

Чтобы получить прямую ссылку на скачивание файла, используется REST‑API
Яндекс.Диска, описанный в документации. Мы формируем запрос

    https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=<публичная_ссылка>

получаем JSON с полем ``href`` и скачиваем содержимое файла. Эта функция
работает без авторизации для публичных ресурсов.

Собрать приложение под macOS можно так (при установленном PyInstaller):

.. code-block:: bash

   pyinstaller --clean --onedir --windowed --name "Open Links" open_links_macos.py

Полученный бандл `.app` будет находиться в каталоге ``dist``. Обратите
внимание, что при передаче `.app` через некоторые мессенджеры macOS может
добавлять расширенный атрибут quarantine. В этом случае нужно снять
quarantine командой `xattr -rd com.apple.quarantine <путь к приложению>`【291185687737797†L31-L41】【291185687737797†L86-L90】.

"""

import json
import time
import urllib.parse
import urllib.request
import webbrowser
from typing import List

# Публичная ссылка на файл с перечнем URL‑адресов.
# В прошлом приложение использовало общедоступный файл на Яндекс.Диске, но
# для macOS новой точкой загрузки служит репозиторий на GitHub. Здесь
# указываем прямую ссылку (raw) на файл links_MacOS.txt в репозитории.
PUBLIC_LINK = "https://raw.githubusercontent.com/gregkorneev/start/main/links_MacOS.txt"

# Интервал опроса (секунды)
POLL_INTERVAL = 300  # 5 минут

def get_remote_links(public_link: str) -> List[str]:
    """Загружает список URL из удалённого текстового файла.

    Если ``public_link`` содержит домен Яндекс.Диска, то используется REST‑API
    для получения прямой ссылки на скачивание. В ином случае функция
    предполагает, что передана прямая ссылка на файл (например, raw‑ссылка
    GitHub), и скачивает содержимое напрямую. Возвращает список непустых
    строк без комментариев.

    Args:
        public_link: URL или публичная ссылка, по которой доступен текстовый
            файл со списком URL‑адресов.

    Returns:
        Список строк (URL). При ошибке — пустой список.
    """
    try:
        content: str = ""
        if "disk.yandex" in public_link:
            api_endpoint = (
                "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
                + urllib.parse.urlencode({"public_key": public_link})
            )
            with urllib.request.urlopen(api_endpoint) as response:
                data = json.loads(response.read().decode("utf-8"))
            href = data.get("href")
            if not href:
                print("Не удалось получить прямую ссылку на файл")
                return []
            with urllib.request.urlopen(href) as f:
                content = f.read().decode("utf-8")
        else:
            # Ссылка указывает на файл напрямую (например, GitHub raw)
            with urllib.request.urlopen(public_link) as f:
                content = f.read().decode("utf-8")
        links: List[str] = []
        for line in content.splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                links.append(s)
        return links
    except Exception as exc:
        print(f"Ошибка загрузки: {exc}")
        return []

def main() -> None:
    opened: set[str] = set()
    while True:
        for url in get_remote_links(PUBLIC_LINK):
            if url not in opened:
                webbrowser.open_new_tab(url)
                opened.add(url)
                time.sleep(0.5)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
