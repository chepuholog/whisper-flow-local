import os
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, WHISPER_LANGUAGE


class Transcriber:
    def __init__(self):
        print(f"[WhisperFlow] Загрузка модели '{WHISPER_MODEL}'...")
        # cpu + int8 — работает без GPU, достаточно быстро
        self.model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        print("[WhisperFlow] Модель загружена. Готов к работе!")

    def transcribe(self, wav_path: str) -> str:
        try:
            segments, info = self.model.transcribe(
                wav_path,
                language=WHISPER_LANGUAGE,
                beam_size=5,
                vad_filter=True,           # Фильтр тишины
                vad_parameters=dict(min_silence_duration_ms=500),
            )
            text = " ".join(seg.text.strip() for seg in segments)
            return text.strip()
        finally:
            # Удаляем временный файл
            if os.path.exists(wav_path):
                os.remove(wav_path)
