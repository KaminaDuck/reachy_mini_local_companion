"""Faster-Whisper-based speech-to-text engine."""

import time
from pathlib import Path
from typing import Callable

import numpy as np
from numpy.typing import NDArray

from reachy_mini_local_companion.stt.base import STTEngine, STTResult

# Available Whisper model sizes
WHISPER_MODELS = {
    "tiny": {"size_mb": 75, "vram_mb": 1000},
    "tiny.en": {"size_mb": 75, "vram_mb": 1000},
    "base": {"size_mb": 150, "vram_mb": 1000},
    "base.en": {"size_mb": 150, "vram_mb": 1000},
    "small": {"size_mb": 500, "vram_mb": 2000},
    "small.en": {"size_mb": 500, "vram_mb": 2000},
    "medium": {"size_mb": 1500, "vram_mb": 5000},
    "medium.en": {"size_mb": 1500, "vram_mb": 5000},
    "large-v3": {"size_mb": 3000, "vram_mb": 10000},
}


class WhisperSTTEngine(STTEngine):
    """Faster-Whisper-based speech-to-text engine.

    Uses CTranslate2 for optimized Whisper inference.
    Provides high accuracy but requires more resources than Vosk.
    """

    def __init__(
        self,
        model_name: str = "tiny.en",
        model_dir: Path | None = None,
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        """Initialize Whisper STT engine.

        Args:
            model_name: Whisper model size (e.g., 'tiny', 'base', 'small').
            model_dir: Directory for model storage.
            device: Compute device ('cpu', 'cuda', 'auto').
            compute_type: Quantization type ('float16', 'int8', 'int8_float16').
        """
        super().__init__(model_name, model_dir)
        self._model = None
        self._device = device
        self._compute_type = compute_type

    @property
    def engine_name(self) -> str:
        return "whisper"

    def load_model(self, progress_callback: Callable[[float], None] | None = None) -> None:
        """Load Whisper model."""
        from faster_whisper import WhisperModel

        if progress_callback:
            progress_callback(0.1)

        # faster-whisper downloads models automatically to HuggingFace cache
        # We use the model_dir as download_root if provided
        self._model = WhisperModel(
            self.model_name,
            device=self._device,
            compute_type=self._compute_type,
            download_root=str(self.model_dir) if self.model_dir else None,
        )

        if progress_callback:
            progress_callback(1.0)

        self._is_loaded = True

    def unload_model(self) -> None:
        """Unload the Whisper model."""
        self._model = None
        self._is_loaded = False

    def transcribe(self, audio: NDArray[np.float32], sample_rate: int = 16000) -> STTResult:
        """Transcribe audio using Whisper."""
        if not self._is_loaded or self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        start_time = time.time()

        # Resample if needed (Whisper expects 16kHz)
        if sample_rate != 16000:
            # Simple resampling - for production use librosa or scipy
            ratio = 16000 / sample_rate
            indices = np.arange(0, len(audio), 1 / ratio).astype(int)
            indices = indices[indices < len(audio)]
            audio = audio[indices]

        # Run transcription
        segments, info = self._model.transcribe(
            audio,
            beam_size=5,
            language="en",
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
        )

        # Collect all segments
        text_parts = []
        total_confidence = 0.0
        segment_count = 0

        for segment in segments:
            text_parts.append(segment.text.strip())
            total_confidence += segment.avg_logprob
            segment_count += 1

        text = " ".join(text_parts)
        avg_confidence = np.exp(total_confidence / max(segment_count, 1))  # Convert log prob to probability

        duration = time.time() - start_time

        return STTResult(
            text=text,
            confidence=float(avg_confidence),
            is_final=True,
            duration_seconds=duration,
        )

    def supports_streaming(self) -> bool:
        return False  # faster-whisper does batch transcription

    def get_available_models(self) -> list[str]:
        return list(WHISPER_MODELS.keys())
