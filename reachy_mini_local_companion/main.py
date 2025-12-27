import logging
import threading
import time
from typing import Any

import numpy as np
from pydantic import BaseModel
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

from reachy_mini_local_companion.stt.manager import (
    STTConfig,
    STTEngineType,
    STTManager,
    TranscriptionEvent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReachyMiniLocalCompanion(ReachyMiniApp):
    # Optional: URL to a custom configuration page for the app
    # eg. "http://localhost:8042"
    custom_app_url: str | None = "http://0.0.0.0:8042"
    # Optional: specify a media backend ("gstreamer", "default", etc.)
    request_media_backend: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        t0 = time.time()

        antennas_enabled = True
        sound_play_requested = False

        # Initialize STT Manager
        stt_config = STTConfig(
            enabled=False,  # Disabled by default, user enables via UI
            engine=STTEngineType.VOSK_SMALL,
            wake_word_enabled=True,
            wake_word_threshold=0.5,
        )
        stt_manager = STTManager(config=stt_config)

        # Track last transcription for the UI
        last_transcripts: list[dict[str, Any]] = []
        max_transcripts = 10

        def on_transcription(event: TranscriptionEvent) -> None:
            """Handle transcription events."""
            nonlocal last_transcripts
            transcript = {
                "text": event.text,
                "confidence": event.confidence,
                "wake_word": event.wake_word,
                "timestamp": time.time(),
            }
            last_transcripts.append(transcript)
            # Keep only the last N transcripts
            if len(last_transcripts) > max_transcripts:
                last_transcripts = last_transcripts[-max_transcripts:]
            logger.info(f"Transcription: {event.text}")

        stt_manager.add_listener(on_transcription)

        # === Pydantic Models for API ===
        class AntennaState(BaseModel):
            enabled: bool

        class STTConfigRequest(BaseModel):
            enabled: bool | None = None
            engine: STTEngineType | None = None
            wake_word_enabled: bool | None = None
            wake_word_threshold: float | None = None

        # === Existing Endpoints ===
        @self.settings_app.post("/antennas")
        def update_antennas_state(state: AntennaState) -> dict[str, bool]:
            nonlocal antennas_enabled
            antennas_enabled = state.enabled
            return {"antennas_enabled": antennas_enabled}

        @self.settings_app.post("/play_sound")
        def request_sound_play() -> dict[str, str]:
            nonlocal sound_play_requested
            sound_play_requested = True
            return {"status": "requested"}

        # === STT Endpoints ===
        @self.settings_app.get("/stt/status")
        def get_stt_status() -> dict[str, Any]:
            """Get current STT system status."""
            status = stt_manager.get_status()
            return {
                "enabled": status.enabled,
                "engine": status.engine.value,
                "state": status.state.value,
                "wake_word_enabled": status.wake_word_enabled,
                "model_loaded": status.model_loaded,
                "last_transcript": status.last_transcript,
                "error": status.error,
            }

        @self.settings_app.post("/stt/config")
        def update_stt_config(config: STTConfigRequest) -> dict[str, Any]:
            """Update STT configuration."""
            current_config = stt_manager.config

            # Build new config from current + updates
            new_config = STTConfig(
                enabled=config.enabled if config.enabled is not None else current_config.enabled,
                engine=config.engine if config.engine is not None else current_config.engine,
                wake_word_enabled=(
                    config.wake_word_enabled
                    if config.wake_word_enabled is not None
                    else current_config.wake_word_enabled
                ),
                wake_word_threshold=(
                    config.wake_word_threshold
                    if config.wake_word_threshold is not None
                    else current_config.wake_word_threshold
                ),
            )

            stt_manager.update_config(new_config)

            # If enabled and models not loaded, load them
            if new_config.enabled and not stt_manager.is_ready:
                try:
                    stt_manager.load_models()
                except Exception as e:
                    logger.error(f"Failed to load STT models: {e}")
                    return {"status": "error", "error": str(e)}

            return {"status": "ok", "config": new_config.model_dump()}

        @self.settings_app.get("/stt/models")
        def list_stt_models() -> list[dict[str, str]]:
            """List available STT models."""
            return stt_manager.get_available_engines()

        @self.settings_app.get("/stt/transcripts")
        def get_transcripts() -> list[dict[str, Any]]:
            """Get recent transcriptions."""
            return last_transcripts

        @self.settings_app.post("/stt/listen/start")
        def start_listening() -> dict[str, str]:
            """Manually start listening (bypass wake word)."""
            if not stt_manager.is_ready:
                return {"status": "error", "error": "STT not ready"}
            stt_manager.start_listening()
            return {"status": "listening"}

        @self.settings_app.post("/stt/listen/stop")
        def stop_listening() -> dict[str, str]:
            """Stop listening and reset state."""
            stt_manager.stop_listening()
            return {"status": "stopped"}

        @self.settings_app.delete("/stt/transcripts")
        def clear_transcripts() -> dict[str, str]:
            """Clear transcript history."""
            nonlocal last_transcripts
            last_transcripts = []
            return {"status": "cleared"}

        # === Main control loop ===
        while not stop_event.is_set():
            t = time.time() - t0

            yaw_deg = 30.0 * np.sin(2.0 * np.pi * 0.2 * t)
            head_pose = create_head_pose(yaw=yaw_deg, degrees=True)

            if antennas_enabled:
                amp_deg = 25.0
                a = amp_deg * np.sin(2.0 * np.pi * 0.5 * t)
                antennas_deg = np.array([a, -a])
            else:
                antennas_deg = np.array([0.0, 0.0])

            if sound_play_requested:
                logger.info("Playing sound...")
                reachy_mini.media.play_sound("wake_up.wav")
                sound_play_requested = False

            # Process audio for STT if enabled
            if stt_manager.is_ready:
                try:
                    # Get audio chunk from microphone
                    audio_chunk = reachy_mini.microphone.get_audio_chunk()
                    if audio_chunk is not None and len(audio_chunk) > 0:
                        # Normalize to float32 [-1, 1] if needed
                        if audio_chunk.dtype == np.int16:
                            audio_float = audio_chunk.astype(np.float32) / 32767.0
                        else:
                            audio_float = audio_chunk.astype(np.float32)

                        # Process through STT pipeline
                        stt_manager.process_audio(audio_float)
                except Exception as e:
                    logger.debug(f"Audio processing error: {e}")

            antennas_rad = np.deg2rad(antennas_deg)

            reachy_mini.set_target(
                head=head_pose,
                antennas=antennas_rad,
            )

            time.sleep(0.02)

        # Cleanup
        stt_manager.unload_models()


if __name__ == "__main__":
    app = ReachyMiniLocalCompanion()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()
