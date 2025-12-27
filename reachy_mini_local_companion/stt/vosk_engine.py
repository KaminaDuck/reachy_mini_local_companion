"""Vosk-based speech-to-text engine."""

import json
import time
import zipfile
from pathlib import Path
from typing import Callable
from urllib.request import urlretrieve

import numpy as np
from numpy.typing import NDArray

from reachy_mini_local_companion.stt.base import STTEngine, STTResult

# Vosk model URLs and sizes
VOSK_MODELS = {
    "vosk-model-small-en-us": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "size_mb": 40,
    },
    "vosk-model-en-us": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
        "size_mb": 1800,
    },
}


class VoskSTTEngine(STTEngine):
    """Vosk-based offline speech-to-text engine.

    Vosk provides fast, lightweight offline speech recognition.
    Good for real-time transcription on resource-constrained devices.
    """

    def __init__(self, model_name: str = "vosk-model-small-en-us", model_dir: Path | None = None) -> None:
        """Initialize Vosk STT engine.

        Args:
            model_name: Vosk model name (e.g., 'vosk-model-small-en-us').
            model_dir: Directory for model storage.
        """
        super().__init__(model_name, model_dir)
        self._model = None
        self._recognizer = None
        self._sample_rate = 16000

    @property
    def engine_name(self) -> str:
        return "vosk"

    def load_model(self, progress_callback: Callable[[float], None] | None = None) -> None:
        """Load Vosk model, downloading if necessary."""
        from vosk import Model, SetLogLevel

        SetLogLevel(-1)  # Suppress Vosk logging

        model_path = self.model_dir / self.model_name

        if not model_path.exists():
            self._download_model(progress_callback)

        self._model = Model(str(model_path))
        self._is_loaded = True

    def _download_model(self, progress_callback: Callable[[float], None] | None = None) -> None:
        """Download and extract Vosk model."""
        if self.model_name not in VOSK_MODELS:
            raise ValueError(f"Unknown Vosk model: {self.model_name}. Available: {list(VOSK_MODELS.keys())}")

        model_info = VOSK_MODELS[self.model_name]
        url = str(model_info["url"])
        zip_path = self.model_dir / f"{self.model_name}.zip"

        def _progress_hook(block_num: int, block_size: int, total_size: int) -> None:
            if progress_callback and total_size > 0:
                progress = min(1.0, block_num * block_size / total_size)
                progress_callback(progress * 0.9)  # 90% for download

        urlretrieve(url, zip_path, reporthook=_progress_hook)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(self.model_dir)

        zip_path.unlink()

        if progress_callback:
            progress_callback(1.0)

    def unload_model(self) -> None:
        """Unload the Vosk model."""
        self._model = None
        self._recognizer = None
        self._is_loaded = False

    def transcribe(self, audio: NDArray[np.float32], sample_rate: int = 16000) -> STTResult:
        """Transcribe audio using Vosk."""
        from vosk import KaldiRecognizer

        if not self._is_loaded or self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        start_time = time.time()

        # Convert float32 [-1, 1] to int16
        audio_int16 = (audio * 32767).astype(np.int16)
        audio_bytes = audio_int16.tobytes()

        recognizer = KaldiRecognizer(self._model, sample_rate)
        recognizer.AcceptWaveform(audio_bytes)

        result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")

        duration = time.time() - start_time

        return STTResult(
            text=text,
            confidence=1.0,  # Vosk doesn't provide confidence scores
            is_final=True,
            duration_seconds=duration,
        )

    def supports_streaming(self) -> bool:
        return True

    def get_available_models(self) -> list[str]:
        return list(VOSK_MODELS.keys())
