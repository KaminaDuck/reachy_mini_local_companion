"""Piper TTS engine wrapper."""

import io
import logging
import os
import tempfile
import threading
import wave
from typing import TYPE_CHECKING, Iterator

import numpy as np

from reachy_mini_local_companion.tts.models import TTSStatus
from reachy_mini_local_companion.tts.voice_manager import VoiceManager


def scale_audio_volume(wav_bytes: bytes, volume: float) -> bytes:
    """Scale audio samples in a WAV file by volume factor.

    Args:
        wav_bytes: WAV audio data as bytes.
        volume: Volume factor (0.0 to 1.0).

    Returns:
        Scaled WAV audio data as bytes.
    """
    if volume >= 1.0:
        return wav_bytes  # No scaling needed

    if volume <= 0.0:
        # Return silence - keep same format but zero samples
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_in:
            params = wav_in.getparams()
            frames = wav_in.readframes(params.nframes)

        samples = np.frombuffer(frames, dtype=np.int16)
        silent = np.zeros_like(samples)

        output = io.BytesIO()
        with wave.open(output, "wb") as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(silent.tobytes())

        return output.getvalue()

    # Read original WAV
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(params.nframes)

    # Scale samples with clipping prevention
    samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    scaled = np.clip(samples * volume, -32768, 32767).astype(np.int16)

    # Write scaled WAV
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(scaled.tobytes())

    return output.getvalue()

if TYPE_CHECKING:
    from piper.voice import PiperVoice
    from reachy_mini import ReachyMini

logger = logging.getLogger(__name__)


class PiperTTSEngine:
    """Piper TTS engine for local speech synthesis.

    Provides methods for synthesizing text to audio and playing
    through the Reachy Mini speaker.
    """

    def __init__(self, voice_manager: VoiceManager) -> None:
        """Initialize the TTS engine.

        Args:
            voice_manager: Voice manager for model access.
        """
        self.voice_manager = voice_manager
        self._voice: "PiperVoice | None" = None
        self._voice_id: str | None = None
        self._lock = threading.Lock()
        self._speaking = False
        self._last_error: str | None = None

    def load_voice(self, voice_id: str) -> None:
        """Load a voice model.

        If the voice is not installed, it will be downloaded first.

        Args:
            voice_id: The voice identifier to load.

        Raises:
            RuntimeError: If voice loading fails.
        """
        with self._lock:
            if self._voice_id == voice_id and self._voice is not None:
                logger.debug(f"Voice {voice_id} already loaded")
                return

            try:
                # Install if not present
                if not self.voice_manager.is_installed(voice_id):
                    logger.info(f"Voice {voice_id} not installed, downloading...")
                    self.voice_manager.install_voice(voice_id)

                # Load the voice model
                model_path = self.voice_manager.get_voice_path(voice_id)

                # Import piper here to avoid import errors if not installed
                from piper.voice import PiperVoice

                logger.info(f"Loading voice: {voice_id}")
                self._voice = PiperVoice.load(str(model_path))
                self._voice_id = voice_id
                self._last_error = None

                logger.info(f"Voice {voice_id} loaded successfully")

            except Exception as e:
                self._last_error = str(e)
                logger.error(f"Failed to load voice {voice_id}: {e}")
                raise RuntimeError(f"Failed to load voice: {e}") from e

    def unload_voice(self) -> None:
        """Unload the current voice to free memory."""
        with self._lock:
            self._voice = None
            self._voice_id = None
            logger.info("Voice unloaded")

    def synthesize(self, text: str, volume: float = 1.0) -> bytes:
        """Synthesize text to WAV audio bytes.

        Args:
            text: The text to synthesize.
            volume: Volume level (0.0 to 1.0). Default is 1.0 (full volume).

        Returns:
            WAV audio data as bytes.

        Raises:
            RuntimeError: If no voice is loaded.
        """
        if self._voice is None:
            raise RuntimeError("No voice loaded")

        with self._lock:
            audio_buffer = io.BytesIO()

            with wave.open(audio_buffer, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 16-bit audio
                wav_file.setframerate(self._voice.config.sample_rate)
                self._voice.synthesize(text, wav_file)

            wav_bytes = audio_buffer.getvalue()

            # Apply volume scaling if not at full volume
            if volume < 1.0:
                wav_bytes = scale_audio_volume(wav_bytes, volume)

            return wav_bytes

    def synthesize_stream(self, text: str) -> Iterator[bytes]:
        """Stream audio synthesis for lower latency on longer text.

        Args:
            text: The text to synthesize.

        Yields:
            Raw audio chunks (16-bit PCM).

        Raises:
            RuntimeError: If no voice is loaded.
        """
        if self._voice is None:
            raise RuntimeError("No voice loaded")

        with self._lock:
            for audio_bytes in self._voice.synthesize_stream_raw(text):
                yield audio_bytes

    def speak(self, text: str, reachy_mini: "ReachyMini", volume: float = 1.0) -> None:
        """Synthesize text and play through the robot's speaker.

        Args:
            text: The text to speak.
            reachy_mini: The Reachy Mini instance for speaker access.
            volume: Volume level (0.0 to 1.0). Default is 1.0 (full volume).

        Raises:
            RuntimeError: If no voice is loaded or playback fails.
        """
        if not text.strip():
            logger.debug("Empty text, skipping speech")
            return

        # Skip playback entirely if volume is 0
        if volume <= 0.0:
            logger.debug("Volume is 0, skipping speech")
            return

        self._speaking = True
        try:
            audio_bytes = self.synthesize(text, volume=volume)

            # Write to temp file for speaker playback
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name

            try:
                logger.info(f"Speaking: {text[:50]}...")
                reachy_mini.speaker.play(temp_path)
            finally:
                os.unlink(temp_path)

        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Speech playback error: {e}")
            raise RuntimeError(f"Failed to speak: {e}") from e
        finally:
            self._speaking = False

    def get_status(self) -> TTSStatus:
        """Get current TTS engine status.

        Returns:
            TTSStatus with current state information.
        """
        return TTSStatus(
            enabled=True,
            ready=self._voice is not None,
            current_voice=self._voice_id,
            speaking=self._speaking,
            error=self._last_error,
        )

    @property
    def sample_rate(self) -> int:
        """Get the sample rate of the loaded voice.

        Returns:
            Sample rate in Hz, or 22050 as default.
        """
        if self._voice is not None:
            return self._voice.config.sample_rate
        return 22050

    @property
    def is_ready(self) -> bool:
        """Check if the engine is ready to synthesize.

        Returns:
            True if a voice is loaded.
        """
        return self._voice is not None

    @property
    def current_voice_id(self) -> str | None:
        """Get the currently loaded voice ID.

        Returns:
            Voice ID or None if no voice loaded.
        """
        return self._voice_id
