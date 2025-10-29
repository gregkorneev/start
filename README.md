# 🚀 start

Простое кроссплатформенное приложение для открытия набора ссылок (например, избранных сайтов или рабочих страниц) одним кликом.  
Поддерживаются **Windows** и **macOS** версии, каждая со своим набором ссылок.

---

## 📂 Структура репозитория

| Файл / Папка | Назначение |
|---------------|------------|
| `open_links_windows.py` | Скрипт для Windows — открывает ссылки из `links_Win.txt` |
| `open_links_macos.py` | Скрипт для macOS — открывает ссылки из `links_MacOS.txt` |
| `links_Win.txt` | Список ссылок для Windows-версии |
| `links_MacOS.txt` | Список ссылок для macOS-версии |
| `MacOS_updated.zip` | Готовая собранная версия для macOS |
| `start.exe` | Исполняемый файл для Windows (собранный через PyInstaller) |

---

## ⚙️ Установка и запуск

### 🔹 Windows

1. Скачай репозиторий:
   ```bash
   git clone https://github.com/gregkorneev/start.git
   cd start
   ```
2. Убедись, что установлен Python 3.
3. Установи зависимости (если они требуются):
   ```bash
   pip install -r requirements.txt
   ```
4. Запусти:
   ```bash
   python open_links_windows.py
   ```
   или просто открой `start.exe`.

---

### 🔹 macOS

1. Скачай архив `MacOS_updated.zip` из репозитория и распакуй.
2. Запусти файл:
   ```bash
   python3 open_links_macos.py
   ```
   или используй встроенный `.app`, если он есть в сборке.

---

## 🌐 Обновление ссылок

Файлы со ссылками теперь берутся из GitHub-репозитория:

| Платформа | Файл | Ссылка |
|------------|------|--------|
| Windows | `links_Win.txt` | [GitHub version](https://github.com/gregkorneev/start/blob/main/links_Win.txt) |
| macOS | `links_MacOS.txt` | [GitHub version](https://github.com/gregkorneev/start/blob/main/links_MacOS.txt) |

В коде эти пути уже обновлены и заменяют старые ссылки на Яндекс.Диск.

---

## 🧩 Сборка exe

Для пересборки исполняемого файла на Windows:
```bash
pyinstaller --onefile open_links_windows.py --name start
```
Готовый файл появится в папке `dist/`.

---

## 🪪 Автор

**Gregory Korneev**  
📍 [github.com/gregkorneev](https://github.com/gregkorneev)
