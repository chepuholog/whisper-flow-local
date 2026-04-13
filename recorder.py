import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import logging
from config import AUDIO_SAMPLERATE, AUDIO_CHANNELS

log = logging.getLogger("WhisperFlow")


class Recorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.stream = None
        # Логируем доступные устройства при инициализации
        try:
            default_device = sd.query_devices(kind='input')
            log.info(f"Устройство ввода по умолчанию: {default_device['name']}")
        except Exception as e:
            log.error(f"Ошибка получения аудиоустройства: {e}", exc_info=True)

    def start(self):
        self.frames = []
        self.recording = True
        log.debug(f"Открываю поток: samplerate={AUDIO_SAMPLERATE}, channels={AUDIO_CHANNELS}")
        self.stream = sd.InputStream(
            samplerate=AUDIO_SAMPLERATE,
            channels=AUDIO_CHANNELS,
            dtype='float32',
            callback=self._callback
        )
        self.stream.start()
        log.debug("Поток записи открыт.")

    def _callback(self, indata, frames, time, status):
        if status:
            log.warning(f"sounddevice статус: {status}")
        if self.recording:
            self.frames.append(indata.copy())

    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        log.debug(f"stop(): фреймов накоплено = {len(self.frames)}")
        if not self.frames:
            return None

        audio = np.concatenate(self.frames, axis=0).flatten()
        peak = float(np.max(np.abs(audio))) if len(audio) > 0 else 0.0
        log.info(f"Аудио: {len(audio)} сэмплов, пиковая амплитуда = {peak:.4f}")

        if peak < 0.001:
            log.warning("Очень тихий сигнал — возможно, VAD отфильтрует всё.")

        # Сохраняем во временный WAV файл
        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wav.write(tmp.name, AUDIO_SAMPLERATE, (audio * 32767).astype(np.int16))
        log.debug(f"WAV сохранён: {tmp.name}")
        return tmp.name
