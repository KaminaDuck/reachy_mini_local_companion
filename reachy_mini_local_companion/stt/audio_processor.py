"""Audio processing and Voice Activity Detection."""

import logging
from collections import deque
from enum import Enum

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


class AudioState(str, Enum):
    """State machine states for audio processing."""

    IDLE = "idle"
    WAKE_DETECTED = "wake_detected"
    LISTENING = "listening"
    PROCESSING = "processing"


class AudioProcessor:
    """Audio buffer management and Voice Activity Detection.

    Manages the audio capture pipeline state machine:
    IDLE -> WAKE_DETECTED -> LISTENING -> PROCESSING -> IDLE
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        max_duration_seconds: float = 10.0,
        silence_timeout_seconds: float = 1.5,
        vad_aggressiveness: int = 2,
    ) -> None:
        """Initialize audio processor.

        Args:
            sample_rate: Audio sample rate in Hz.
            max_duration_seconds: Maximum utterance duration.
            silence_timeout_seconds: Silence duration to end utterance.
            vad_aggressiveness: WebRTC VAD aggressiveness (0-3, higher = more aggressive).
        """
        self.sample_rate = sample_rate
        self.max_duration_seconds = max_duration_seconds
        self.silence_timeout_seconds = silence_timeout_seconds
        self.vad_aggressiveness = vad_aggressiveness

        # Buffer for audio samples
        self.max_samples = int(sample_rate * max_duration_seconds)
        self._audio_buffer: deque[float] = deque(maxlen=self.max_samples)

        # State machine
        self._state = AudioState.IDLE
        self._silence_samples = 0
        self._speech_samples = 0
        self._silence_threshold = int(sample_rate * silence_timeout_seconds)

        # VAD frame size (WebRTC VAD requires 10, 20, or 30ms frames)
        self._vad_frame_ms = 30
        self._vad_frame_size = int(sample_rate * self._vad_frame_ms / 1000)

        # Initialize WebRTC VAD
        self._vad = None
        self._init_vad()

    def _init_vad(self) -> None:
        """Initialize WebRTC Voice Activity Detection."""
        try:
            import webrtcvad

            self._vad = webrtcvad.Vad(self.vad_aggressiveness)
        except Exception as e:
            logger.warning(f"Failed to initialize WebRTC VAD: {e}")
            self._vad = None

    @property
    def state(self) -> AudioState:
        """Current audio processing state."""
        return self._state

    def set_state(self, new_state: AudioState) -> None:
        """Set the processing state."""
        if new_state != self._state:
            logger.debug(f"Audio state: {self._state.value} -> {new_state.value}")
            self._state = new_state

    def is_speech(self, audio_chunk: NDArray[np.float32]) -> bool:
        """Check if audio chunk contains speech using VAD.

        Args:
            audio_chunk: Audio samples as float32 array.

        Returns:
            True if speech is detected.
        """
        if self._vad is None:
            # Fallback: use simple energy-based detection
            energy = np.sqrt(np.mean(audio_chunk**2))
            return energy > 0.01

        # Convert to int16 for WebRTC VAD
        audio_int16 = (audio_chunk * 32767).astype(np.int16)

        # Process in VAD frame sizes
        speech_frames = 0
        total_frames = 0

        for i in range(0, len(audio_int16) - self._vad_frame_size + 1, self._vad_frame_size):
            frame = audio_int16[i : i + self._vad_frame_size]
            try:
                if self._vad.is_speech(frame.tobytes(), self.sample_rate):
                    speech_frames += 1
                total_frames += 1
            except Exception:
                pass

        # Consider speech if >50% of frames contain speech
        return speech_frames > total_frames / 2 if total_frames > 0 else False

    def process_chunk(self, audio_chunk: NDArray[np.float32]) -> AudioState:
        """Process an audio chunk and update state machine.

        Args:
            audio_chunk: Audio samples as float32 array.

        Returns:
            Current state after processing.
        """
        chunk_samples = len(audio_chunk)

        if self._state == AudioState.IDLE:
            # In idle state, don't buffer (waiting for wake word)
            pass

        elif self._state == AudioState.WAKE_DETECTED:
            # Wake word detected, start listening
            self._audio_buffer.clear()
            self._silence_samples = 0
            self._speech_samples = 0
            self.set_state(AudioState.LISTENING)
            # Add this chunk to buffer
            self._audio_buffer.extend(audio_chunk)
            self._speech_samples += chunk_samples

        elif self._state == AudioState.LISTENING:
            # Add audio to buffer
            self._audio_buffer.extend(audio_chunk)

            is_speech = self.is_speech(audio_chunk)

            if is_speech:
                self._speech_samples += chunk_samples
                self._silence_samples = 0
            else:
                self._silence_samples += chunk_samples

            # Check for end of utterance (silence timeout)
            if self._silence_samples >= self._silence_threshold:
                logger.debug(
                    f"Utterance complete: {self._speech_samples / self.sample_rate:.2f}s speech, "
                    f"{self._silence_samples / self.sample_rate:.2f}s silence"
                )
                self.set_state(AudioState.PROCESSING)

            # Check for max duration
            if len(self._audio_buffer) >= self.max_samples:
                logger.debug("Max utterance duration reached")
                self.set_state(AudioState.PROCESSING)

        elif self._state == AudioState.PROCESSING:
            # In processing state, don't accept new audio
            pass

        return self._state

    def get_utterance(self) -> NDArray[np.float32]:
        """Get the buffered utterance for transcription.

        Returns:
            Audio samples as float32 array.
        """
        return np.array(list(self._audio_buffer), dtype=np.float32)

    def reset(self) -> None:
        """Reset the processor to idle state."""
        self._audio_buffer.clear()
        self._silence_samples = 0
        self._speech_samples = 0
        self.set_state(AudioState.IDLE)

    def on_wake_word_detected(self) -> None:
        """Called when wake word is detected."""
        self.set_state(AudioState.WAKE_DETECTED)

    def on_transcription_complete(self) -> None:
        """Called when transcription is complete."""
        self.reset()

    @property
    def buffer_duration_seconds(self) -> float:
        """Current buffer duration in seconds."""
        return len(self._audio_buffer) / self.sample_rate

    @property
    def is_listening(self) -> bool:
        """Check if processor is actively listening."""
        return self._state in (AudioState.WAKE_DETECTED, AudioState.LISTENING)
