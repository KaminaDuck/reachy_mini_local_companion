"""STT Manager - coordinates wake word detection, audio processing, and transcription."""

import logging
import threading
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel

from reachy_mini_local_companion.stt.audio_processor import AudioProcessor, AudioState
from reachy_mini_local_companion.stt.base import STTEngine, STTResult
from reachy_mini_local_companion.stt.vosk_engine import VoskSTTEngine
from reachy_mini_local_companion.stt.wake_word import WakeWordDetector
from reachy_mini_local_companion.stt.whisper_engine import WhisperSTTEngine

logger = logging.getLogger(__name__)


class STTEngineType(str, Enum):
    """Available STT engine types."""

    VOSK_SMALL = "vosk-small"
    VOSK_LARGE = "vosk-large"
    WHISPER_TINY = "whisper-tiny"
    WHISPER_BASE = "whisper-base"
    WHISPER_SMALL = "whisper-small"


class STTConfig(BaseModel):
    """Configuration for STT system."""

    enabled: bool = True
    engine: STTEngineType = STTEngineType.VOSK_SMALL
    wake_word_enabled: bool = True
    wake_word_threshold: float = 0.5
    silence_timeout_seconds: float = 1.5
    max_duration_seconds: float = 10.0


class STTStatus(BaseModel):
    """Current status of STT system."""

    enabled: bool
    engine: STTEngineType
    state: AudioState
    wake_word_enabled: bool
    model_loaded: bool
    last_transcript: str = ""
    error: str | None = None


@dataclass
class TranscriptionEvent:
    """Event emitted when transcription completes."""

    text: str
    confidence: float
    duration_seconds: float
    wake_word: str | None = None


@dataclass
class STTManagerState:
    """Internal state for the STT manager."""

    enabled: bool = False
    model_loaded: bool = False
    last_transcript: str = ""
    last_wake_word: str | None = None
    error: str | None = None
    listeners: list[Callable[[TranscriptionEvent], None]] = field(default_factory=list)


class STTManager:
    """Coordinates wake word detection, audio processing, and STT engines.

    Provides a unified interface for the complete speech-to-text pipeline.
    """

    def __init__(
        self,
        config: STTConfig | None = None,
        model_dir: Path | None = None,
    ) -> None:
        """Initialize STT manager.

        Args:
            config: STT configuration.
            model_dir: Directory for model storage.
        """
        self.config = config or STTConfig()
        self.model_dir = model_dir or Path.home() / ".cache" / "reachy_mini" / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)

        # Components
        self._engine: STTEngine | None = None
        self._wake_word_detector: WakeWordDetector | None = None
        self._audio_processor = AudioProcessor(
            silence_timeout_seconds=self.config.silence_timeout_seconds,
            max_duration_seconds=self.config.max_duration_seconds,
        )

        # State
        self._state = STTManagerState()
        self._lock = threading.Lock()

        # Initialize based on config
        if self.config.enabled:
            self._create_engine()
            if self.config.wake_word_enabled:
                self._create_wake_word_detector()

    def _create_engine(self) -> None:
        """Create STT engine based on configuration."""
        engine_type = self.config.engine

        if engine_type == STTEngineType.VOSK_SMALL:
            self._engine = VoskSTTEngine("vosk-model-small-en-us", self.model_dir)
        elif engine_type == STTEngineType.VOSK_LARGE:
            self._engine = VoskSTTEngine("vosk-model-en-us", self.model_dir)
        elif engine_type == STTEngineType.WHISPER_TINY:
            self._engine = WhisperSTTEngine("tiny.en", self.model_dir)
        elif engine_type == STTEngineType.WHISPER_BASE:
            self._engine = WhisperSTTEngine("base.en", self.model_dir)
        elif engine_type == STTEngineType.WHISPER_SMALL:
            self._engine = WhisperSTTEngine("small.en", self.model_dir)
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")

    def _create_wake_word_detector(self) -> None:
        """Create wake word detector."""
        self._wake_word_detector = WakeWordDetector(
            wake_words=["hey_jarvis"],  # Using hey_jarvis as proxy for "Hey Reachy"
            threshold=self.config.wake_word_threshold,
            model_dir=self.model_dir,
        )

    def load_models(self, progress_callback: Callable[[str, float], None] | None = None) -> None:
        """Load all models (STT engine and wake word).

        Args:
            progress_callback: Callback for progress updates (component_name, progress).
        """
        with self._lock:
            try:
                # Load STT engine
                if self._engine is not None:
                    logger.info(f"Loading STT engine: {self.config.engine}")

                    def stt_progress(p: float) -> None:
                        if progress_callback:
                            progress_callback("stt_engine", p)

                    self._engine.load_model(stt_progress)

                # Load wake word detector
                if self._wake_word_detector is not None:
                    logger.info("Loading wake word detector")

                    def ww_progress(p: float) -> None:
                        if progress_callback:
                            progress_callback("wake_word", p)

                    self._wake_word_detector.load_model(ww_progress)

                self._state.model_loaded = True
                self._state.enabled = True
                self._state.error = None

            except Exception as e:
                logger.error(f"Failed to load models: {e}")
                self._state.error = str(e)
                self._state.model_loaded = False
                raise

    def unload_models(self) -> None:
        """Unload all models to free memory."""
        with self._lock:
            if self._engine is not None:
                self._engine.unload_model()
            if self._wake_word_detector is not None:
                self._wake_word_detector.unload_model()
            self._state.model_loaded = False
            self._state.enabled = False

    def process_audio(self, audio_chunk: NDArray[np.float32]) -> STTResult | None:
        """Process an audio chunk through the STT pipeline.

        Args:
            audio_chunk: Audio samples as float32 array normalized to [-1, 1].

        Returns:
            Transcription result if available, None otherwise.
        """
        if not self._state.enabled or not self._state.model_loaded:
            return None

        with self._lock:
            current_state = self._audio_processor.state

            # Check for wake word in idle state
            if current_state == AudioState.IDLE:
                if self._wake_word_detector is not None and self.config.wake_word_enabled:
                    detected, wake_word = self._wake_word_detector.is_wake_word_detected(audio_chunk)
                    if detected:
                        logger.info(f"Wake word detected: {wake_word}")
                        self._state.last_wake_word = wake_word
                        self._audio_processor.on_wake_word_detected()
                else:
                    # No wake word detection, start listening immediately
                    self._audio_processor.on_wake_word_detected()

            # Process audio through the audio processor
            new_state = self._audio_processor.process_chunk(audio_chunk)

            # If we've collected enough audio, transcribe
            if new_state == AudioState.PROCESSING:
                return self._transcribe_utterance()

        return None

    def _transcribe_utterance(self) -> STTResult | None:
        """Transcribe the buffered utterance."""
        if self._engine is None:
            return None

        utterance = self._audio_processor.get_utterance()
        if len(utterance) == 0:
            self._audio_processor.on_transcription_complete()
            return None

        try:
            result = self._engine.transcribe(utterance)
            self._state.last_transcript = result.text

            # Emit event to listeners
            event = TranscriptionEvent(
                text=result.text,
                confidence=result.confidence,
                duration_seconds=result.duration_seconds,
                wake_word=self._state.last_wake_word,
            )
            for listener in self._state.listeners:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"Error in transcription listener: {e}")

            logger.info(f"Transcription: {result.text}")

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            self._state.error = str(e)
            result = None

        finally:
            self._audio_processor.on_transcription_complete()
            self._state.last_wake_word = None

        return result

    def add_listener(self, callback: Callable[[TranscriptionEvent], None]) -> None:
        """Add a listener for transcription events."""
        self._state.listeners.append(callback)

    def remove_listener(self, callback: Callable[[TranscriptionEvent], None]) -> None:
        """Remove a transcription listener."""
        if callback in self._state.listeners:
            self._state.listeners.remove(callback)

    def get_status(self) -> STTStatus:
        """Get current STT system status."""
        return STTStatus(
            enabled=self._state.enabled,
            engine=self.config.engine,
            state=self._audio_processor.state,
            wake_word_enabled=self.config.wake_word_enabled,
            model_loaded=self._state.model_loaded,
            last_transcript=self._state.last_transcript,
            error=self._state.error,
        )

    def update_config(self, new_config: STTConfig) -> None:
        """Update STT configuration.

        Note: Changing engine requires reloading models.
        """
        with self._lock:
            engine_changed = new_config.engine != self.config.engine
            wake_word_changed = new_config.wake_word_enabled != self.config.wake_word_enabled

            self.config = new_config

            # Update audio processor settings
            self._audio_processor.silence_timeout_seconds = new_config.silence_timeout_seconds
            self._audio_processor.max_duration_seconds = new_config.max_duration_seconds

            # Recreate components if needed
            if engine_changed:
                if self._engine is not None:
                    self._engine.unload_model()
                self._create_engine()
                self._state.model_loaded = False

            if wake_word_changed:
                if new_config.wake_word_enabled:
                    self._create_wake_word_detector()
                else:
                    if self._wake_word_detector is not None:
                        self._wake_word_detector.unload_model()
                    self._wake_word_detector = None

            # Update wake word threshold
            if self._wake_word_detector is not None:
                self._wake_word_detector.threshold = new_config.wake_word_threshold

            self._state.enabled = new_config.enabled

    def start_listening(self) -> None:
        """Start listening without wake word (manual activation)."""
        with self._lock:
            if self._state.enabled and self._state.model_loaded:
                self._audio_processor.on_wake_word_detected()

    def stop_listening(self) -> None:
        """Stop listening and reset state."""
        with self._lock:
            self._audio_processor.reset()
            if self._wake_word_detector is not None:
                self._wake_word_detector.reset()

    def get_available_engines(self) -> list[dict[str, str]]:
        """Get list of available STT engines."""
        return [
            {"id": STTEngineType.VOSK_SMALL.value, "name": "Vosk Small (Fast, 40MB)"},
            {"id": STTEngineType.VOSK_LARGE.value, "name": "Vosk Large (Accurate, 1.8GB)"},
            {"id": STTEngineType.WHISPER_TINY.value, "name": "Whisper Tiny (75MB)"},
            {"id": STTEngineType.WHISPER_BASE.value, "name": "Whisper Base (150MB)"},
            {"id": STTEngineType.WHISPER_SMALL.value, "name": "Whisper Small (500MB)"},
        ]

    @property
    def is_ready(self) -> bool:
        """Check if STT system is ready for use."""
        return self._state.enabled and self._state.model_loaded

    @property
    def is_listening(self) -> bool:
        """Check if currently listening for speech."""
        return self._audio_processor.is_listening
