import pyperclip
import keyboard
import time


def type_text(text: str):
    """Вставляет текст в активное окно через буфер обмена."""
    if not text:
        return

    try:
        old_clipboard = pyperclip.paste()
    except Exception:
        old_clipboard = ""

    try:
        pyperclip.copy(text)
        time.sleep(0.1)
        keyboard.send('ctrl+v')
        time.sleep(0.1)

    finally:
        try:
            pyperclip.copy(old_clipboard)
        except Exception:
            pass
