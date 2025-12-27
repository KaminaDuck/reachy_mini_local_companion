"""Wake word detection using openWakeWord."""

import logging
from pathlib import Path
from typing import Callable

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

# Default wake words available in openWakeWord
DEFAULT_WAKE_WORDS = [
    "hey_jarvis",
    "alexa",
    "hey_mycroft",
    "ok_google",
]


class WakeWordDetector:
    """Wake word detection using openWakeWord.

    Detects predefined wake phrases to activate speech recognition.
    Uses openWakeWord's pre-trained models for efficiency.
    """

    def __init__(
        self,
        wake_words: list[str] | None = None,
        threshold: float = 0.5,
        model_dir: Path | None = None,
    ) -> None:
        """Initialize wake word detector.

        Args:
            wake_words: List of wake word model names to load.
                       Defaults to ["hey_jarvis"] as a proxy for "Hey Reachy".
            threshold: Detection threshold (0.0 to 1.0).
            model_dir: Directory for model storage.
        """
        self.wake_words = wake_words or ["hey_jarvis"]
        self.threshold = threshold
        self.model_dir = model_dir or Path.home() / ".cache" / "reachy_mini" / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self._model = None
        self._is_loaded = False
        self._sample_rate = 16000
        self._chunk_size = 1280  # 80ms at 16kHz (openWakeWord requirement)

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load_model(self, progress_callback: Callable[[float], None] | None = None) -> None:
        """Load wake word detection models."""
        from openwakeword import Model

        if progress_callback:
            progress_callback(0.2)

        # openWakeWord automatically downloads models on first use
        self._model = Model(
            wakeword_models=self.wake_words,
            inference_framework="onnx",
        )

        if progress_callback:
            progress_callback(1.0)

        self._is_loaded = True
        logger.info(f"Loaded wake word models: {self.wake_words}")

    def unload_model(self) -> None:
        """Unload wake word models."""
        self._model = None
        self._is_loaded = False

    def detect(self, audio_chunk: NDArray[np.float32]) -> dict[str, float]:
        """Check for wake word in audio chunk.

        Args:
            audio_chunk: Audio samples as float32 array normalized to [-1, 1].
                        Should be 80ms (1280 samples at 16kHz) for best results.

        Returns:
            Dictionary mapping wake word names to detection scores.
        """
        if not self._is_loaded or self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Convert float32 [-1, 1] to int16
        audio_int16 = (audio_chunk * 32767).astype(np.int16)

        # Run prediction
        prediction = self._model.predict(audio_int16)

        return dict(prediction)

    def is_wake_word_detected(self, audio_chunk: NDArray[np.float32]) -> tuple[bool, str | None]:
        """Check if any wake word is detected above threshold.

        Args:
            audio_chunk: Audio samples as float32 array.

        Returns:
            Tuple of (detected, wake_word_name).
        """
        scores = self.detect(audio_chunk)

        for word, score in scores.items():
            if score >= self.threshold:
                logger.debug(f"Wake word detected: {word} (score: {score:.3f})")
                return True, word

        return False, None

    def reset(self) -> None:
        """Reset the detector state for a new detection session."""
        if self._model is not None:
            self._model.reset()

    def get_available_wake_words(self) -> list[str]:
        """Get list of available pre-trained wake words."""
        return DEFAULT_WAKE_WORDS

    @property
    def chunk_size(self) -> int:
        """Required chunk size in samples (80ms at 16kHz)."""
        return self._chunk_size

    @property
    def sample_rate(self) -> int:
        """Required sample rate in Hz."""
        return self._sample_rate
