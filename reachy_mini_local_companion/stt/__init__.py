"""Speech-to-Text module for Reachy Mini Local Companion.

Provides local, privacy-preserving speech recognition with wake word detection.
"""

from reachy_mini_local_companion.stt.base import STTEngine, STTResult
from reachy_mini_local_companion.stt.vosk_engine import VoskSTTEngine
from reachy_mini_local_companion.stt.whisper_engine import WhisperSTTEngine
from reachy_mini_local_companion.stt.wake_word import WakeWordDetector
from reachy_mini_local_companion.stt.audio_processor import AudioProcessor, AudioState
from reachy_mini_local_companion.stt.manager import STTManager, STTConfig

__all__ = [
    "STTEngine",
    "STTResult",
    "VoskSTTEngine",
    "WhisperSTTEngine",
    "WakeWordDetector",
    "AudioProcessor",
    "AudioState",
    "STTManager",
    "STTConfig",
]
