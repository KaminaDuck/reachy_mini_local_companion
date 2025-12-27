"""Text-to-Speech module for Reachy Mini Local Companion."""

from reachy_mini_local_companion.tts.engine import PiperTTSEngine
from reachy_mini_local_companion.tts.models import TTSConfig, TTSStatus, VoiceInfo, VoiceQuality
from reachy_mini_local_companion.tts.voice_manager import VoiceManager

__all__ = [
    "PiperTTSEngine",
    "VoiceManager",
    "TTSConfig",
    "TTSStatus",
    "VoiceInfo",
    "VoiceQuality",
]
