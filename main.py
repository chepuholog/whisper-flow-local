import threading
import keyboard
import pystray
from PIL import Image, ImageDraw
import sys
import os
import logging

# Добавляем папку скрипта в путь
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Логирование в файл (т.к. запускается без консоли)
log_path = os.path.join(BASE_DIR, "whisperflow.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
    ]
)
log = logging.getLogger("WhisperFlow")

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
        log.warning("Модель ещё загружается, подождите...")
        return

    log.info("Запись началась...")
    try:
        recorder.start()
        is_recording = True
        update_tray(True)
    except Exception as e:
        log.error(f"Ошибка запуска записи: {e}", exc_info=True)


def on_hotkey_release():
    global is_recording
    if not is_recording:
        return

    is_recording = False
    log.info("Запись остановлена. Распознаю...")
    update_tray(False)

    try:
        wav_path = recorder.stop()
    except Exception as e:
        log.error(f"Ошибка остановки записи: {e}", exc_info=True)
        return

    if not wav_path:
        log.warning("Аудио не записано (нет фреймов).")
        return

    # Распознавание и вставка в отдельном потоке
    def process():
        try:
            text = transcriber.transcribe(wav_path)
            if text:
                log.info(f"Распознано: {text}")
                type_text(text)
            else:
                log.warning("Текст не распознан (пустой результат).")
        except Exception as e:
            log.error(f"Ошибка транскрибации: {e}", exc_info=True)

    threading.Thread(target=process, daemon=True).start()


def load_model():
    global transcriber
    try:
        transcriber = Transcriber()
        log.info("Модель загружена. Готов к работе!")
    except Exception as e:
        log.error(f"Ошибка загрузки модели: {e}", exc_info=True)


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

    log.info(f"Запущен. Зажмите {HOTKEY.upper()} для записи.")

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
