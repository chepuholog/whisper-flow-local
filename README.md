# 🎙️ WhisperFlow Local

> Бесплатный голосовой ввод для Windows — говори, текст появляется сам.

Аналог Whisper Flow: зажал CapsLock, надиктовал по-русски, отпустил — текст вставился туда, где стоит курсор. Работает в любом приложении: браузер, Word, Telegram, VS Code и т.д.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue?logo=windows)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Free](https://img.shields.io/badge/Бесплатно-100%25-brightgreen)

---

## ✨ Возможности

- 🎤 Голосовой ввод в **любое текстовое поле** на экране
- 🇷🇺 Отличное распознавание **русского языка**
- 🔒 Работает **полностью локально** — никакого интернета, никаких API ключей
- ♾️ **Без лимитов** — пользуйся сколько угодно
- 🟢 Красивая **иконка в трее** — меняется во время записи
- ⚡ Быстрая модель Whisper `small` — баланс скорости и качества

---

## 🖥️ Как это работает

```
Кликнул в текстовое поле
        ↓
Зажал CapsLock → иконка стала яркой (запись идёт)
        ↓
Говоришь по-русски
        ↓
Отпустил CapsLock → Whisper распознаёт → текст вставился
```

---

## 🚀 Установка

### Требования
- Windows 10 / 11
- Python 3.8+
- Микрофон

### Шаги

**1. Клонируй репозиторий:**
```bash
git clone https://github.com/твой-username/whisper-flow-local.git
cd whisper-flow-local
```

**2. Установи зависимости:**
```bash
pip install -r requirements.txt
```

**3. Запусти** *(обязательно от имени администратора)*:
```bash
python main.py
```

При первом запуске автоматически скачается модель Whisper (~500 МБ) — это только один раз.

---

## ⚙️ Настройки

Открой `config.py`:

```python
HOTKEY = 'caps lock'    # Клавиша записи (удерживать)
WHISPER_MODEL = 'small' # tiny / base / small / medium
WHISPER_LANGUAGE = 'ru' # Язык распознавания
```

### Доступные модели Whisper

| Модель | Размер | Скорость | Качество |
|--------|--------|----------|----------|
| `tiny` | ~75 МБ | ⚡⚡⚡ | ★★☆ |
| `base` | ~150 МБ | ⚡⚡ | ★★★ |
| `small` | ~500 МБ | ⚡ | ★★★★ ✅ рекомендуется |
| `medium` | ~1.5 ГБ | 🐢 | ★★★★★ |

---

## 📁 Структура проекта

```
whisper-flow-local/
├── main.py          # Точка входа, иконка в трее
├── recorder.py      # Запись аудио с микрофона
├── transcriber.py   # Распознавание через Whisper
├── typer.py         # Вставка текста через буфер обмена
├── config.py        # Настройки
├── icon.ico         # Иконка приложения
└── requirements.txt # Зависимости
```

---

## 🛠️ Технологии

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — быстрая локальная версия OpenAI Whisper
- [sounddevice](https://python-sounddevice.readthedocs.io/) — запись аудио
- [keyboard](https://github.com/boppreh/keyboard) — глобальные хоткеи
- [pystray](https://github.com/moses-palmer/pystray) — иконка в системном трее
- [pyperclip](https://github.com/asweigart/pyperclip) — работа с буфером обмена

---

## 🤝 Вклад в проект

Буду рад любым улучшениям! Вот идеи что можно добавить:

- [ ] Поддержка других языков
- [ ] Звуковой сигнал при начале/конце записи
- [ ] Уведомление с распознанным текстом
- [ ] Настройка хоткея через GUI
- [ ] Поддержка macOS / Linux

Просто сделай Fork → внеси изменения → отправь Pull Request!

---

## 📄 Лицензия

MIT — делай что хочешь, просто упомяни автора.
