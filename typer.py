import pyperclip
import pyautogui
import time


def type_text(text: str):
    """Вставляет текст в активное окно через буфер обмена."""
    if not text:
        return

    # Сохраняем текущий буфер обмена
    try:
        old_clipboard = pyperclip.paste()
    except Exception:
        old_clipboard = ""

    try:
        # Копируем наш текст
        pyperclip.copy(text)
        time.sleep(0.05)

        # Вставляем Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.05)

    finally:
        # Восстанавливаем старый буфер
        try:
            pyperclip.copy(old_clipboard)
        except Exception:
            pass
