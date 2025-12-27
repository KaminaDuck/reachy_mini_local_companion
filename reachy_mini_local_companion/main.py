import logging
import threading
import time
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

from reachy_mini_local_companion.llm.agent import LLMChatAgent
from reachy_mini_local_companion.llm.models import (
    ChatRequest,
    ProfileCreate,
    ProfileUpdate,
)
from reachy_mini_local_companion.llm.profiles import ProfileStore
from reachy_mini_local_companion.stt.manager import (
    STTConfig,
    STTEngineType,
    STTManager,
    TranscriptionEvent,
)
from reachy_mini_local_companion.tts import (
    PiperTTSEngine,
    TTSConfig,
    VoiceManager,
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

        # Initialize LLM Chat Agent
        profile_store = ProfileStore()
        chat_agent = LLMChatAgent(profile_store)

        # Initialize TTS
        tts_cache_dir = Path.home() / ".cache" / "reachy_mini" / "tts_models"
        voice_manager = VoiceManager(cache_dir=tts_cache_dir)
        tts_engine = PiperTTSEngine(voice_manager)
        tts_config = TTSConfig()

        # Try to load default voice if installed
        try:
            if voice_manager.is_installed(tts_config.selected_voice):
                tts_engine.load_voice(tts_config.selected_voice)
                logger.info(f"Loaded default TTS voice: {tts_config.selected_voice}")
        except Exception as e:
            logger.warning(f"Could not load default TTS voice: {e}")

        # === Pydantic Models for API ===
        class AntennaState(BaseModel):
            enabled: bool

        class STTConfigRequest(BaseModel):
            enabled: bool | None = None
            engine: STTEngineType | None = None
            wake_word_enabled: bool | None = None
            wake_word_threshold: float | None = None

        class TTSConfigRequest(BaseModel):
            enabled: bool | None = None
            selected_voice: str | None = None
            auto_speak_llm: bool | None = None
            volume: int | None = None

        class SpeakRequest(BaseModel):
            text: str

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

        # === LLM Chat Endpoints ===
        @self.settings_app.get("/profiles")
        def list_profiles() -> list[dict[str, Any]]:
            """List all available profiles."""
            profiles = profile_store.list_all()
            return [p.model_dump(mode="json") for p in profiles]

        @self.settings_app.post("/profiles")
        def create_profile(data: ProfileCreate) -> dict[str, Any]:
            """Create a new profile."""
            profile = profile_store.create(data)
            return profile.model_dump(mode="json")

        @self.settings_app.get("/profiles/{profile_id}")
        def get_profile(profile_id: str) -> dict[str, Any]:
            """Get a profile by ID."""
            profile = profile_store.get(profile_id)
            if profile is None:
                return {"error": "Profile not found"}
            return profile.model_dump(mode="json")

        @self.settings_app.put("/profiles/{profile_id}")
        def update_profile(profile_id: str, data: ProfileUpdate) -> dict[str, Any]:
            """Update a profile."""
            profile = profile_store.update(profile_id, data)
            if profile is None:
                return {"error": "Profile not found"}
            return profile.model_dump(mode="json")

        @self.settings_app.delete("/profiles/{profile_id}")
        def delete_profile(profile_id: str) -> dict[str, Any]:
            """Delete a profile."""
            success = profile_store.delete(profile_id)
            if not success:
                return {"error": "Cannot delete profile (not found or last profile)"}
            return {"status": "deleted"}

        @self.settings_app.post("/chat")
        def send_chat_message(request: ChatRequest) -> dict[str, Any]:
            """Send a message to the LLM and get a response."""
            try:
                response = chat_agent.chat_sync(request)

                # Auto-speak LLM response if enabled
                if tts_config.auto_speak_llm and tts_config.enabled and tts_engine.is_ready:
                    try:
                        volume = tts_config.volume / 100.0  # Convert 0-100 to 0.0-1.0
                        tts_engine.speak(response.message, reachy_mini, volume=volume)
                    except RuntimeError as tts_err:
                        logger.warning("Auto-speak failed: %s", tts_err)

                return {
                    "message": response.message,
                    "profile_id": response.profile_id,
                    "profile_name": response.profile_name,
                }
            except Exception as e:
                logger.error("Chat error: %s", e)
                return {"error": str(e)}

        @self.settings_app.delete("/chat/history")
        def clear_chat_history() -> dict[str, str]:
            """Clear the conversation history."""
            chat_agent.clear_history()
            return {"status": "cleared"}

        @self.settings_app.get("/chat/history")
        def get_chat_history() -> list[dict[str, Any]]:
            """Get the conversation history."""
            messages = chat_agent.get_history()
            return [m.model_dump(mode="json") for m in messages]

        @self.settings_app.get("/chat/status")
        def get_chat_status() -> dict[str, Any]:
            """Get LLM provider status."""
            status = chat_agent.get_status()
            current_profile = chat_agent.get_current_profile()
            return {
                "connected": status.connected,
                "provider": status.provider,
                "model": status.model,
                "error": status.error,
                "current_profile_id": current_profile.id if current_profile else None,
                "current_profile_name": current_profile.name if current_profile else None,
            }

        # === TTS Endpoints ===
        @self.settings_app.get("/tts/voices")
        def list_tts_voices() -> list[dict[str, Any]]:
            """List available TTS voices."""
            voices = voice_manager.list_voices()
            return [v.model_dump(mode="json") for v in voices]

        @self.settings_app.post("/tts/voices/{voice_id}/install")
        def install_tts_voice(voice_id: str) -> dict[str, Any]:
            """Install a TTS voice."""
            try:
                voice_manager.install_voice(voice_id)
                return {"status": "installed", "voice_id": voice_id}
            except ValueError as e:
                return {"status": "error", "error": str(e)}
            except RuntimeError as e:
                return {"status": "error", "error": str(e)}

        @self.settings_app.delete("/tts/voices/{voice_id}")
        def remove_tts_voice(voice_id: str) -> dict[str, Any]:
            """Remove an installed TTS voice."""
            if voice_manager.remove_voice(voice_id):
                return {"status": "removed", "voice_id": voice_id}
            return {"status": "error", "error": "Voice not found"}

        @self.settings_app.get("/tts/config")
        def get_tts_config() -> dict[str, Any]:
            """Get current TTS configuration."""
            return tts_config.model_dump(mode="json")

        @self.settings_app.post("/tts/config")
        def update_tts_config(config: TTSConfigRequest) -> dict[str, Any]:
            """Update TTS configuration."""
            nonlocal tts_config

            # Update config values
            if config.enabled is not None:
                tts_config.enabled = config.enabled
            if config.auto_speak_llm is not None:
                tts_config.auto_speak_llm = config.auto_speak_llm
            if config.volume is not None:
                # Clamp volume to valid range
                tts_config.volume = max(0, min(100, config.volume))

            # Handle voice change
            new_voice = config.selected_voice
            if new_voice is not None and new_voice != tts_config.selected_voice:
                try:
                    tts_engine.load_voice(new_voice)
                    tts_config.selected_voice = new_voice
                except RuntimeError as e:
                    return {"status": "error", "error": str(e)}

            return {"status": "ok", "config": tts_config.model_dump(mode="json")}

        @self.settings_app.get("/tts/status")
        def get_tts_status() -> dict[str, Any]:
            """Get current TTS system status."""
            status = tts_engine.get_status()
            return {
                "enabled": tts_config.enabled,
                "ready": status.ready,
                "current_voice": status.current_voice,
                "speaking": status.speaking,
                "auto_speak_llm": tts_config.auto_speak_llm,
                "volume": tts_config.volume,
                "error": status.error,
            }

        @self.settings_app.post("/tts/speak")
        def speak_text(request: SpeakRequest) -> dict[str, Any]:
            """Synthesize and play text through the speaker."""
            if not tts_config.enabled:
                return {"status": "error", "error": "TTS is disabled"}
            if not tts_engine.is_ready:
                return {"status": "error", "error": "No voice loaded"}

            try:
                volume = tts_config.volume / 100.0  # Convert 0-100 to 0.0-1.0
                tts_engine.speak(request.text, reachy_mini, volume=volume)
                return {"status": "ok", "text": request.text}
            except RuntimeError as e:
                return {"status": "error", "error": str(e)}

        @self.settings_app.post("/tts/preview/{voice_id}")
        def preview_tts_voice(voice_id: str) -> dict[str, Any]:
            """Preview a voice with sample text."""
            original_voice = tts_engine.current_voice_id
            sample_text = "Hello! This is a preview of my voice."

            try:
                tts_engine.load_voice(voice_id)
                volume = tts_config.volume / 100.0  # Convert 0-100 to 0.0-1.0
                tts_engine.speak(sample_text, reachy_mini, volume=volume)

                # Restore original voice if different
                if original_voice and original_voice != voice_id:
                    tts_engine.load_voice(original_voice)

                return {"status": "ok", "voice_id": voice_id}
            except RuntimeError as e:
                return {"status": "error", "error": str(e)}

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
        tts_engine.unload_voice()


if __name__ == "__main__":
    app = ReachyMiniLocalCompanion()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()
