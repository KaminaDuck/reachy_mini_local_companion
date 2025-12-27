"""Base classes and protocols for STT engines."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

import numpy as np
from numpy.typing import NDArray


class ModelSize(str, Enum):
    """Available model sizes for STT engines."""

    TINY = "tiny"
    SMALL = "small"
    BASE = "base"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class STTResult:
    """Result from speech-to-text transcription."""

    text: str
    confidence: float
    is_final: bool
    duration_seconds: float

    def __bool__(self) -> bool:
        return bool(self.text.strip())


class STTEngine(ABC):
    """Abstract base class for speech-to-text engines."""

    def __init__(self, model_name: str, model_dir: Path | None = None) -> None:
        """Initialize the STT engine.

        Args:
            model_name: Name/size of the model to use.
            model_dir: Directory for model storage. Defaults to ~/.cache/reachy_mini/models.
        """
        self.model_name = model_name
        self.model_dir = model_dir or Path.home() / ".cache" / "reachy_mini" / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self._is_loaded = False

    @property
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded

    @abstractmethod
    def load_model(self, progress_callback: Callable[[float], None] | None = None) -> None:
        """Load the STT model.

        Args:
            progress_callback: Optional callback for download progress (0.0 to 1.0).
        """
        ...

    @abstractmethod
    def unload_model(self) -> None:
        """Unload the model to free memory."""
        ...

    @abstractmethod
    def transcribe(self, audio: NDArray[np.float32], sample_rate: int = 16000) -> STTResult:
        """Transcribe audio to text.

        Args:
            audio: Audio samples as float32 array normalized to [-1, 1].
            sample_rate: Audio sample rate in Hz.

        Returns:
            Transcription result.
        """
        ...

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if this engine supports streaming transcription."""
        ...

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Get list of available model names for this engine."""
        ...

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Get the name of this STT engine."""
        ...
