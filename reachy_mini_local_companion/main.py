"""Reachy Mini Local Companion - Modular AI companion application.

This application supports conditional loading of capabilities via feature flags.
Set these in your environment or modify the FEATURES dict below for testing.

Environment Variables:
    FEATURE_STT: Enable Speech-to-Text (default: true)
    FEATURE_LLM: Enable LLM Chat (default: true)
    FEATURE_TTS: Enable Text-to-Speech (default: true)
    FEATURE_EMOTIONS: Enable Emotion System (default: true)
    FEATURE_VOLUME: Enable Volume Control (default: true)
    FEATURE_VISION: Enable Vision System (default: false, not yet implemented)
"""

import logging
import os
import threading
import time
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel
from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Feature Flags
# =============================================================================


def get_feature_flag(name: str, default: bool = True) -> bool:
    """Get feature flag from environment variable."""
    env_value = os.environ.get(f"FEATURE_{name.upper()}", "").lower()
    if env_value in ("true", "1", "yes", "on"):
        return True
    if env_value in ("false", "0", "no", "off"):
        return False
    return default


FEATURES = {
    "stt": get_feature_flag("STT", default=True),
    "llm": get_feature_flag("LLM", default=True),
    "tts": get_feature_flag("TTS", default=True),
    "emotions": get_feature_flag("EMOTIONS", default=True),
    "volume": get_feature_flag("VOLUME", default=True),
    "vision": get_feature_flag("VISION", default=False),
}

logger.info(f"Feature flags: {FEATURES}")


# =============================================================================
# Conditional Imports
# =============================================================================

# STT imports
if FEATURES["stt"]:
    try:
        from reachy_mini_local_companion.stt.manager import (
            STTConfig,
            STTEngineType,
            STTManager,
            TranscriptionEvent,
        )

        STT_AVAILABLE = True
    except ImportError as e:
        logger.warning(f"STT module not available: {e}")
        STT_AVAILABLE = False
else:
    STT_AVAILABLE = False

# LLM imports
if FEATURES["llm"]:
    try:
        from reachy_mini_local_companion.llm.agent import LLMChatAgent
        from reachy_mini_local_companion.llm.models import (
            ChatRequest,
            ProfileCreate,
            ProfileUpdate,
        )
        from reachy_mini_local_companion.llm.profiles import ProfileStore

        LLM_AVAILABLE = True
    except ImportError as e:
        logger.warning(f"LLM module not available: {e}")
        LLM_AVAILABLE = False
else:
    LLM_AVAILABLE = False

# TTS imports
if FEATURES["tts"]:
    try:
        from reachy_mini_local_companion.tts import (
            PiperTTSEngine,
            TTSConfig,
            VoiceManager,
        )

        TTS_AVAILABLE = True
    except ImportError as e:
        logger.warning(f"TTS module not available: {e}")
        TTS_AVAILABLE = False
else:
    TTS_AVAILABLE = False

# Emotions imports (always available - no external deps)
if FEATURES["emotions"]:
    try:
        from reachy_mini_local_companion.emotions import (
            EMOTIONS,
            list_emotions,
        )

        EMOTIONS_AVAILABLE = True
    except ImportError as e:
        logger.warning(f"Emotions module not available: {e}")
        EMOTIONS_AVAILABLE = False
else:
    EMOTIONS_AVAILABLE = False


class ReachyMiniLocalCompanion(ReachyMiniApp):
    """Modular AI companion for Reachy Mini.

    Supports conditional loading of capabilities:
    - STT: Speech-to-Text with wake word detection
    - LLM: Language model chat with personality profiles
    - TTS: Text-to-Speech synthesis
    - Emotions: Expressive head/antenna animations
    - Volume: Speaker volume control
    - Vision: Camera-based features (planned)
    """

    custom_app_url: str | None = "http://0.0.0.0:8042"
    request_media_backend: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        t0 = time.time()
        antennas_enabled = True
        sound_play_requested = False

        # =================================================================
        # Initialize Components Based on Feature Flags
        # =================================================================

        # --- STT Setup ---
        stt_manager = None
        last_transcripts: list[dict[str, Any]] = []
        max_transcripts = 10

        if FEATURES["stt"] and STT_AVAILABLE:
            stt_config = STTConfig(
                enabled=False,
                engine=STTEngineType.VOSK_SMALL,
                wake_word_enabled=True,
                wake_word_threshold=0.5,
            )
            stt_manager = STTManager(config=stt_config)

            def on_transcription(event: TranscriptionEvent) -> None:
                nonlocal last_transcripts
                transcript = {
                    "text": event.text,
                    "confidence": event.confidence,
                    "wake_word": event.wake_word,
                    "timestamp": time.time(),
                }
                last_transcripts.append(transcript)
                if len(last_transcripts) > max_transcripts:
                    last_transcripts = last_transcripts[-max_transcripts:]
                logger.info(f"Transcription: {event.text}")

            stt_manager.add_listener(on_transcription)
            logger.info("STT module initialized")

        # --- LLM Setup ---
        profile_store = None
        chat_agent = None

        if FEATURES["llm"] and LLM_AVAILABLE:
            profile_store = ProfileStore()
            chat_agent = LLMChatAgent(profile_store)
            logger.info("LLM module initialized")

        # --- TTS Setup ---
        voice_manager = None
        tts_engine = None
        tts_config = None

        if FEATURES["tts"] and TTS_AVAILABLE:
            tts_cache_dir = Path.home() / ".cache" / "reachy_mini" / "tts_models"
            voice_manager = VoiceManager(cache_dir=tts_cache_dir)
            tts_engine = PiperTTSEngine(voice_manager)
            tts_config = TTSConfig()

            try:
                if voice_manager.is_installed(tts_config.selected_voice):
                    tts_engine.load_voice(tts_config.selected_voice)
                    logger.info(f"Loaded default TTS voice: {tts_config.selected_voice}")
            except Exception as e:
                logger.warning(f"Could not load default TTS voice: {e}")

            logger.info("TTS module initialized")

        # --- Emotions Setup ---
        current_emotion: str | None = None
        emotion_requested: str | None = None
        emotion_stop_requested: bool = False
        emotion_keyframe_index: int = 0
        emotion_keyframe_start_time: float = 0.0

        if FEATURES["emotions"] and EMOTIONS_AVAILABLE:
            logger.info("Emotions module initialized")

        # =================================================================
        # Pydantic Models for API
        # =================================================================

        class AntennaState(BaseModel):
            enabled: bool

        class FeatureStatus(BaseModel):
            stt: bool = FEATURES["stt"] and STT_AVAILABLE
            llm: bool = FEATURES["llm"] and LLM_AVAILABLE
            tts: bool = FEATURES["tts"] and TTS_AVAILABLE
            emotions: bool = FEATURES["emotions"] and EMOTIONS_AVAILABLE
            volume: bool = FEATURES["volume"]
            vision: bool = FEATURES["vision"]

        # =================================================================
        # Core Endpoints (Always Available)
        # =================================================================

        @self.settings_app.get("/features")
        def get_features() -> dict[str, bool]:
            """Get enabled feature status."""
            return FeatureStatus().model_dump()

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

        # =================================================================
        # STT Endpoints (Conditional)
        # =================================================================

        if FEATURES["stt"] and STT_AVAILABLE and stt_manager is not None:

            class STTConfigRequest(BaseModel):
                enabled: bool | None = None
                engine: STTEngineType | None = None
                wake_word_enabled: bool | None = None
                wake_word_threshold: float | None = None

            @self.settings_app.get("/stt/status")
            def get_stt_status() -> dict[str, Any]:
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
                current_config = stt_manager.config
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
                if new_config.enabled and not stt_manager.is_ready:
                    try:
                        stt_manager.load_models()
                    except Exception as e:
                        logger.error(f"Failed to load STT models: {e}")
                        return {"status": "error", "error": str(e)}
                return {"status": "ok", "config": new_config.model_dump()}

            @self.settings_app.get("/stt/models")
            def list_stt_models() -> list[dict[str, str]]:
                return stt_manager.get_available_engines()

            @self.settings_app.get("/stt/transcripts")
            def get_transcripts() -> list[dict[str, Any]]:
                return last_transcripts

            @self.settings_app.post("/stt/listen/start")
            def start_listening() -> dict[str, str]:
                if not stt_manager.is_ready:
                    return {"status": "error", "error": "STT not ready"}
                stt_manager.start_listening()
                return {"status": "listening"}

            @self.settings_app.post("/stt/listen/stop")
            def stop_listening() -> dict[str, str]:
                stt_manager.stop_listening()
                return {"status": "stopped"}

            @self.settings_app.delete("/stt/transcripts")
            def clear_transcripts() -> dict[str, str]:
                nonlocal last_transcripts
                last_transcripts = []
                return {"status": "cleared"}

        # =================================================================
        # LLM Endpoints (Conditional)
        # =================================================================

        if FEATURES["llm"] and LLM_AVAILABLE and chat_agent is not None and profile_store is not None:

            @self.settings_app.get("/profiles")
            def list_profiles() -> list[dict[str, Any]]:
                profiles = profile_store.list_all()
                return [p.model_dump(mode="json") for p in profiles]

            @self.settings_app.post("/profiles")
            def create_profile(data: ProfileCreate) -> dict[str, Any]:
                profile = profile_store.create(data)
                return profile.model_dump(mode="json")

            @self.settings_app.get("/profiles/{profile_id}")
            def get_profile(profile_id: str) -> dict[str, Any]:
                profile = profile_store.get(profile_id)
                if profile is None:
                    return {"error": "Profile not found"}
                return profile.model_dump(mode="json")

            @self.settings_app.put("/profiles/{profile_id}")
            def update_profile(profile_id: str, data: ProfileUpdate) -> dict[str, Any]:
                profile = profile_store.update(profile_id, data)
                if profile is None:
                    return {"error": "Profile not found"}
                return profile.model_dump(mode="json")

            @self.settings_app.delete("/profiles/{profile_id}")
            def delete_profile(profile_id: str) -> dict[str, Any]:
                success = profile_store.delete(profile_id)
                if not success:
                    return {"error": "Cannot delete profile (not found or last profile)"}
                return {"status": "deleted"}

            @self.settings_app.post("/chat")
            def send_chat_message(request: ChatRequest) -> dict[str, Any]:
                try:
                    response = chat_agent.chat_sync(request)
                    # Auto-speak if TTS enabled
                    if (
                        tts_config is not None
                        and tts_config.auto_speak_llm
                        and tts_config.enabled
                        and tts_engine is not None
                        and tts_engine.is_ready
                    ):
                        try:
                            volume = tts_config.volume / 100.0
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
                chat_agent.clear_history()
                return {"status": "cleared"}

            @self.settings_app.get("/chat/history")
            def get_chat_history() -> list[dict[str, Any]]:
                messages = chat_agent.get_history()
                return [m.model_dump(mode="json") for m in messages]

            @self.settings_app.get("/chat/status")
            def get_chat_status() -> dict[str, Any]:
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

        # =================================================================
        # TTS Endpoints (Conditional)
        # =================================================================

        if FEATURES["tts"] and TTS_AVAILABLE and tts_engine is not None and voice_manager is not None:

            class TTSConfigRequest(BaseModel):
                enabled: bool | None = None
                selected_voice: str | None = None
                auto_speak_llm: bool | None = None
                volume: int | None = None

            class SpeakRequest(BaseModel):
                text: str

            @self.settings_app.get("/tts/voices")
            def list_tts_voices() -> list[dict[str, Any]]:
                voices = voice_manager.list_voices()
                return [v.model_dump(mode="json") for v in voices]

            @self.settings_app.post("/tts/voices/{voice_id}/install")
            def install_tts_voice(voice_id: str) -> dict[str, Any]:
                try:
                    voice_manager.install_voice(voice_id)
                    return {"status": "installed", "voice_id": voice_id}
                except (ValueError, RuntimeError) as e:
                    return {"status": "error", "error": str(e)}

            @self.settings_app.delete("/tts/voices/{voice_id}")
            def remove_tts_voice(voice_id: str) -> dict[str, Any]:
                if voice_manager.remove_voice(voice_id):
                    return {"status": "removed", "voice_id": voice_id}
                return {"status": "error", "error": "Voice not found"}

            @self.settings_app.get("/tts/config")
            def get_tts_config() -> dict[str, Any]:
                return tts_config.model_dump(mode="json")

            @self.settings_app.post("/tts/config")
            def update_tts_config(config: TTSConfigRequest) -> dict[str, Any]:
                nonlocal tts_config
                if config.enabled is not None:
                    tts_config.enabled = config.enabled
                if config.auto_speak_llm is not None:
                    tts_config.auto_speak_llm = config.auto_speak_llm
                if config.volume is not None:
                    tts_config.volume = max(0, min(100, config.volume))
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
                if not tts_config.enabled:
                    return {"status": "error", "error": "TTS is disabled"}
                if not tts_engine.is_ready:
                    return {"status": "error", "error": "No voice loaded"}
                try:
                    volume = tts_config.volume / 100.0
                    tts_engine.speak(request.text, reachy_mini, volume=volume)
                    return {"status": "ok", "text": request.text}
                except RuntimeError as e:
                    return {"status": "error", "error": str(e)}

            @self.settings_app.post("/tts/preview/{voice_id}")
            def preview_tts_voice(voice_id: str) -> dict[str, Any]:
                original_voice = tts_engine.current_voice_id
                sample_text = "Hello! This is a preview of my voice."
                try:
                    tts_engine.load_voice(voice_id)
                    volume = tts_config.volume / 100.0
                    tts_engine.speak(sample_text, reachy_mini, volume=volume)
                    if original_voice and original_voice != voice_id:
                        tts_engine.load_voice(original_voice)
                    return {"status": "ok", "voice_id": voice_id}
                except RuntimeError as e:
                    return {"status": "error", "error": str(e)}

        # =================================================================
        # Emotions Endpoints (Conditional)
        # =================================================================

        if FEATURES["emotions"] and EMOTIONS_AVAILABLE:

            class EmotionRequest(BaseModel):
                name: str

            @self.settings_app.get("/emotions")
            def get_emotions() -> list[dict[str, str]]:
                return list_emotions()

            @self.settings_app.post("/emotion")
            def trigger_emotion(request: EmotionRequest) -> dict[str, Any]:
                nonlocal emotion_requested, emotion_stop_requested
                if request.name not in EMOTIONS:
                    return {"status": "error", "error": f"Unknown emotion: {request.name}"}
                emotion_requested = request.name
                emotion_stop_requested = False
                logger.info("Emotion requested: %s", request.name)
                return {"status": "queued", "emotion": request.name}

            @self.settings_app.post("/emotion/stop")
            def stop_emotion() -> dict[str, str]:
                nonlocal emotion_stop_requested
                emotion_stop_requested = True
                logger.info("Emotion stop requested")
                return {"status": "stopping"}

            @self.settings_app.get("/emotion/status")
            def get_emotion_status() -> dict[str, Any]:
                return {
                    "current_emotion": current_emotion,
                    "queued_emotion": emotion_requested,
                }

        # =================================================================
        # Main Control Loop
        # =================================================================

        while not stop_event.is_set():
            t = time.time() - t0

            # --- Emotion Execution ---
            if FEATURES["emotions"] and EMOTIONS_AVAILABLE:
                if emotion_requested is not None and current_emotion is None:
                    current_emotion = emotion_requested
                    emotion_requested = None
                    emotion_keyframe_index = 0
                    emotion_keyframe_start_time = time.time()
                    logger.info("Starting emotion: %s", current_emotion)

                    emotion_profile = EMOTIONS.get(current_emotion)
                    if emotion_profile and emotion_profile.sound:
                        try:
                            reachy_mini.media.play_sound(emotion_profile.sound)
                        except Exception as e:
                            logger.debug("Emotion sound not found: %s", e)

                if current_emotion is not None:
                    emotion_profile = EMOTIONS.get(current_emotion)
                    if emotion_profile and emotion_keyframe_index < len(emotion_profile.keyframes):
                        keyframe = emotion_profile.keyframes[emotion_keyframe_index]
                        elapsed = time.time() - emotion_keyframe_start_time

                        if elapsed >= keyframe.duration:
                            emotion_keyframe_index += 1
                            emotion_keyframe_start_time = time.time()
                            if emotion_keyframe_index >= len(emotion_profile.keyframes):
                                logger.info("Emotion complete: %s", current_emotion)
                                current_emotion = None
                        else:
                            head_pose = create_head_pose(
                                yaw=keyframe.head_yaw,
                                pitch=keyframe.head_pitch,
                                roll=keyframe.head_roll,
                                degrees=True,
                            )
                            antennas_rad = np.array([keyframe.antenna_right, keyframe.antenna_left])
                            remaining = keyframe.duration - elapsed
                            if remaining > 0.02:
                                reachy_mini.goto_target(
                                    head=head_pose,
                                    antennas=antennas_rad,
                                    duration=remaining,
                                )
                                time.sleep(max(0, remaining - 0.02))
                            else:
                                reachy_mini.set_target(head=head_pose, antennas=antennas_rad)

                    if emotion_stop_requested:
                        logger.info("Emotion stopped: %s", current_emotion)
                        current_emotion = None
                        emotion_stop_requested = False
                        emotion_keyframe_index = 0

            # --- Idle Animation ---
            if not FEATURES["emotions"] or not EMOTIONS_AVAILABLE or current_emotion is None:
                yaw_deg = 30.0 * np.sin(2.0 * np.pi * 0.2 * t)
                head_pose = create_head_pose(yaw=yaw_deg, degrees=True)

                if antennas_enabled:
                    amp_deg = 25.0
                    a = amp_deg * np.sin(2.0 * np.pi * 0.5 * t)
                    antennas_deg = np.array([a, -a])
                else:
                    antennas_deg = np.array([0.0, 0.0])

                antennas_rad = np.deg2rad(antennas_deg)
                reachy_mini.set_target(head=head_pose, antennas=antennas_rad)

            if sound_play_requested:
                logger.info("Playing sound...")
                reachy_mini.media.play_sound("wake_up.wav")
                sound_play_requested = False

            # --- STT Audio Processing ---
            if FEATURES["stt"] and STT_AVAILABLE and stt_manager is not None and stt_manager.is_ready:
                try:
                    audio_chunk = reachy_mini.microphone.get_audio_chunk()
                    if audio_chunk is not None and len(audio_chunk) > 0:
                        if audio_chunk.dtype == np.int16:
                            audio_float = audio_chunk.astype(np.float32) / 32767.0
                        else:
                            audio_float = audio_chunk.astype(np.float32)
                        stt_manager.process_audio(audio_float)
                except Exception as e:
                    logger.debug("Audio processing error: %s", e)

            time.sleep(0.02)

        # --- Cleanup ---
        if FEATURES["stt"] and STT_AVAILABLE and stt_manager is not None:
            stt_manager.unload_models()
        if FEATURES["tts"] and TTS_AVAILABLE and tts_engine is not None:
            tts_engine.unload_voice()


if __name__ == "__main__":
    app = ReachyMiniLocalCompanion()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()
