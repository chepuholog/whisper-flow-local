import threading
import keyboard
import pystray
from PIL import Image, ImageDraw
import sys
import os

# Добавляем папку скрипта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recorder import Recorder
from transcriber import Transcriber
from typer import type_text
from config import HOTKEY


# --- Состояние ---
recorder = Recorder()
transcriber = None  # Загружается отдельно, чтобы не тормозить старт
is_recording = False
tray_icon = None


def make_icon(recording: bool) -> Image.Image:
    """Создаёт красивую иконку микрофона для трея."""
    S = 128
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Фон — чёрный скруглённый квадрат
    d.rounded_rectangle([0, 0, S-1, S-1], radius=26, fill=(17, 17, 17, 255))

    # Цвета микрофона
    mic_main  = (116, 198, 157, 255)  # зелёный основной
    mic_light = (149, 213, 178, 255)  # блик
    mic_dark  = (45,  106, 79,  255)  # линии решётки

    if recording:
        mic_main  = (149, 213, 178, 255)
        mic_light = (178, 229, 202, 255)

    # Корпус микрофона (капсула)
    mx, my, mw, mh = 46, 14, 36, 60
    d.rounded_rectangle([mx, my, mx+mw, my+mh], radius=18, fill=mic_main)

    # Блик слева-сверху
    d.rounded_rectangle([mx+4, my+5, mx+16, my+26], radius=6, fill=mic_light)

    # Решётка — 3 горизонтальные линии
    for i, fy in enumerate([0.38, 0.52, 0.66]):
        ly = int(my + mh * fy)
        d.line([mx+7, ly, mx+mw-7, ly], fill=mic_dark, width=2)

    # Дуга-подставка
    aw = 52
    ax = (S - aw) // 2
    at = my + int(mh * 0.72)
    ab = my + mh + 18
    d.arc([ax, at, ax+aw, ab], start=0, end=180, fill=mic_main, width=5)

    # Ножка
    cx = S // 2
    leg_top = (at + ab) // 2
    leg_bot = S - 18
    d.line([cx, leg_top, cx, leg_bot], fill=mic_main, width=5)

    # Основание
    bw = 34
    d.line([cx - bw//2, leg_bot, cx + bw//2, leg_bot], fill=mic_main, width=6)

    # Красная точка при записи
    if recording:
        r = 13
        d.ellipse([S-r*2-4, 4, S-4, r*2+4], fill=(230, 57, 70, 255))
        d.ellipse([S-r*2+2, 10, S-10, r*2-2], fill=(255, 107, 107, 255))

    return img.resize((64, 64), Image.LANCZOS)


def update_tray(recording: bool):
    global tray_icon
    if tray_icon:
        tray_icon.icon = make_icon(recording)
        tray_icon.title = "🔴 WhisperFlow: запись..." if recording else "⚪ WhisperFlow: готов"


def on_hotkey_press():
    global is_recording
    if is_recording:
        return
    if transcriber is None:
        print("[WhisperFlow] Модель ещё загружается, подождите...")
        return

    is_recording = True
    update_tray(True)
    print("[WhisperFlow] Запись началась...")
    recorder.start()


def on_hotkey_release():
    global is_recording
    if not is_recording:
        return

    is_recording = False
    print("[WhisperFlow] Запись остановлена. Распознаю...")
    update_tray(False)

    wav_path = recorder.stop()
    if not wav_path:
        print("[WhisperFlow] Аудио не записано.")
        return

    # Распознавание и вставка в отдельном потоке
    def process():
        text = transcriber.transcribe(wav_path)
        if text:
            print(f"[WhisperFlow] Распознано: {text}")
            type_text(text)
        else:
            print("[WhisperFlow] Текст не распознан.")

    threading.Thread(target=process, daemon=True).start()


def load_model():
    global transcriber
    transcriber = Transcriber()


def quit_app(icon, item):
    icon.stop()
    keyboard.unhook_all()
    sys.exit(0)


def main():
    global tray_icon

    # Загружаем модель в фоне
    threading.Thread(target=load_model, daemon=True).start()

    # Регистрируем глобальные хоткеи
    keyboard.on_press_key(HOTKEY, lambda _: on_hotkey_press(), suppress=True)
    keyboard.on_release_key(HOTKEY, lambda _: on_hotkey_release(), suppress=True)

    print(f"[WhisperFlow] Запущен. Зажмите {HOTKEY.upper()} для записи.")

    # Иконка в трее
    menu = pystray.Menu(
        pystray.MenuItem("WhisperFlow", None, enabled=False),
        pystray.MenuItem("Выход", quit_app),
    )
    tray_icon = pystray.Icon(
        "WhisperFlow",
        make_icon(False),
        f"WhisperFlow — зажми {HOTKEY.upper()}",
        menu
    )
    tray_icon.run()


if __name__ == "__main__":
    main()
