"""Pydantic models for TTS configuration and voice information."""

from enum import Enum

from pydantic import BaseModel


class VoiceQuality(str, Enum):
    """Voice quality levels corresponding to Piper model variants."""

    LOW = "low"  # x_low - fastest, smallest
    MEDIUM = "medium"  # medium - balanced
    HIGH = "high"  # high - best quality


class VoiceInfo(BaseModel):
    """Information about an available TTS voice."""

    id: str  # e.g., "en_US-lessac-medium"
    name: str  # e.g., "Lessac (US English)"
    language: str  # e.g., "en_US"
    quality: VoiceQuality
    sample_rate: int = 22050  # Default Piper sample rate
    installed: bool = False
    size_mb: float = 0.0  # Model size in MB


class TTSConfig(BaseModel):
    """Configuration for the TTS system."""

    enabled: bool = True
    selected_voice: str = "en_US-lessac-medium"
    auto_speak_llm: bool = False
    speaking_rate: float = 1.0  # Speech speed multiplier (not used by Piper, for future)
    volume: int = 80  # Volume level 0-100%


class TTSStatus(BaseModel):
    """Current status of the TTS system."""

    enabled: bool
    ready: bool
    current_voice: str | None
    speaking: bool = False
    error: str | None = None
