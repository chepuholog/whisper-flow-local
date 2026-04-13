import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
from config import AUDIO_SAMPLERATE, AUDIO_CHANNELS


class Recorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.stream = None

    def start(self):
        self.frames = []
        self.recording = True
        self.stream = sd.InputStream(
            samplerate=AUDIO_SAMPLERATE,
            channels=AUDIO_CHANNELS,
            dtype='float32',
            callback=self._callback
        )
        self.stream.start()

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.frames:
            return None

        audio = np.concatenate(self.frames, axis=0).flatten()

        # Сохраняем во временный WAV файл
        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        wav.write(tmp.name, AUDIO_SAMPLERATE, (audio * 32767).astype(np.int16))
        return tmp.name
