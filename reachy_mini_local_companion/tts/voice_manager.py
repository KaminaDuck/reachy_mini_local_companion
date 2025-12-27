"""Voice model management for Piper TTS."""

import logging
import urllib.request
from pathlib import Path
from typing import Callable

from reachy_mini_local_companion.tts.models import VoiceInfo, VoiceQuality

logger = logging.getLogger(__name__)

# Hugging Face base URL for Piper voice models
PIPER_VOICES_BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0"

# Voice catalog with popular voices
VOICE_CATALOG: list[dict[str, str | float]] = [
    # English (US) voices
    {
        "id": "en_US-lessac-medium",
        "name": "Lessac (US)",
        "language": "en_US",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "en_US-lessac-high",
        "name": "Lessac HQ (US)",
        "language": "en_US",
        "quality": "high",
        "size_mb": 95.0,
    },
    {
        "id": "en_US-amy-medium",
        "name": "Amy (US)",
        "language": "en_US",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "en_US-ryan-medium",
        "name": "Ryan (US)",
        "language": "en_US",
        "quality": "medium",
        "size_mb": 75.0,
    },
    # English (UK) voices
    {
        "id": "en_GB-alan-medium",
        "name": "Alan (UK)",
        "language": "en_GB",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "en_GB-cori-medium",
        "name": "Cori (UK)",
        "language": "en_GB",
        "quality": "medium",
        "size_mb": 75.0,
    },
    # Other languages
    {
        "id": "de_DE-thorsten-medium",
        "name": "Thorsten (German)",
        "language": "de_DE",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "fr_FR-upmc-medium",
        "name": "UPMC (French)",
        "language": "fr_FR",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "es_ES-davefx-medium",
        "name": "DaveFX (Spanish)",
        "language": "es_ES",
        "quality": "medium",
        "size_mb": 75.0,
    },
    {
        "id": "it_IT-riccardo-x_low",
        "name": "Riccardo (Italian)",
        "language": "it_IT",
        "quality": "low",
        "size_mb": 20.0,
    },
]


class VoiceManager:
    """Manages Piper TTS voice models.

    Handles voice discovery, downloading, and installation.
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize the voice manager.

        Args:
            cache_dir: Directory for storing voice models.
                      Defaults to ~/.cache/reachy_mini/tts_models/
        """
        self.cache_dir = cache_dir or Path.home() / ".cache" / "reachy_mini" / "tts_models"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def list_voices(self) -> list[VoiceInfo]:
        """List all available voices with installation status.

        Returns:
            List of VoiceInfo objects for all cataloged voices.
        """
        voices = []
        for entry in VOICE_CATALOG:
            voice_id = str(entry["id"])
            quality_str = str(entry["quality"])

            # Map quality string to enum
            quality_map = {"low": VoiceQuality.LOW, "medium": VoiceQuality.MEDIUM, "high": VoiceQuality.HIGH}
            quality = quality_map.get(quality_str, VoiceQuality.MEDIUM)

            voices.append(
                VoiceInfo(
                    id=voice_id,
                    name=str(entry["name"]),
                    language=str(entry["language"]),
                    quality=quality,
                    installed=self.is_installed(voice_id),
                    size_mb=float(entry["size_mb"]),
                )
            )
        return voices

    def is_installed(self, voice_id: str) -> bool:
        """Check if a voice is installed.

        Args:
            voice_id: The voice identifier (e.g., "en_US-lessac-medium")

        Returns:
            True if both the ONNX model and JSON config exist.
        """
        onnx_path = self.get_voice_path(voice_id)
        json_path = onnx_path.with_suffix(".onnx.json")
        return onnx_path.exists() and json_path.exists()

    def get_voice_path(self, voice_id: str) -> Path:
        """Get the path to a voice model file.

        Args:
            voice_id: The voice identifier.

        Returns:
            Path to the ONNX model file.
        """
        return self.cache_dir / f"{voice_id}.onnx"

    def install_voice(
        self,
        voice_id: str,
        progress_callback: Callable[[float], None] | None = None,
    ) -> None:
        """Download and install a voice model.

        Args:
            voice_id: The voice identifier to install.
            progress_callback: Optional callback for progress updates (0.0-1.0).

        Raises:
            ValueError: If the voice is not in the catalog.
            RuntimeError: If download fails.
        """
        # Verify voice is in catalog
        if not any(entry["id"] == voice_id for entry in VOICE_CATALOG):
            raise ValueError(f"Unknown voice: {voice_id}")

        if self.is_installed(voice_id):
            logger.info(f"Voice {voice_id} already installed")
            return

        # Parse voice_id to build download paths
        # Format: lang_COUNTRY-name-quality (e.g., en_US-lessac-medium)
        parts = voice_id.rsplit("-", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid voice ID format: {voice_id}")

        lang_country, name, quality = parts
        # Split lang_country into lang/country for URL path
        lang_parts = lang_country.split("_")
        if len(lang_parts) != 2:
            raise ValueError(f"Invalid language format in voice ID: {voice_id}")

        lang, country = lang_parts

        # Build URLs
        # Path format: en/en_US/lessac/medium/en_US-lessac-medium.onnx
        base_path = f"{lang}/{lang}_{country}/{name}/{quality}"
        onnx_url = f"{PIPER_VOICES_BASE_URL}/{base_path}/{voice_id}.onnx"
        json_url = f"{PIPER_VOICES_BASE_URL}/{base_path}/{voice_id}.onnx.json"

        onnx_path = self.get_voice_path(voice_id)
        json_path = onnx_path.with_suffix(".onnx.json")

        try:
            # Download ONNX model
            logger.info(f"Downloading voice model: {voice_id}")
            self._download_file(onnx_url, onnx_path, progress_callback, weight=0.95)

            # Download JSON config
            logger.info(f"Downloading voice config: {voice_id}")
            self._download_file(json_url, json_path, progress_callback, weight=0.05, offset=0.95)

            if progress_callback:
                progress_callback(1.0)

            logger.info(f"Voice {voice_id} installed successfully")

        except Exception as e:
            # Clean up partial downloads
            onnx_path.unlink(missing_ok=True)
            json_path.unlink(missing_ok=True)
            raise RuntimeError(f"Failed to install voice {voice_id}: {e}") from e

    def _download_file(
        self,
        url: str,
        dest: Path,
        progress_callback: Callable[[float], None] | None = None,
        weight: float = 1.0,
        offset: float = 0.0,
    ) -> None:
        """Download a file with optional progress tracking.

        Args:
            url: URL to download from.
            dest: Destination path.
            progress_callback: Optional progress callback.
            weight: Weight of this download in total progress (0-1).
            offset: Starting offset for progress (0-1).
        """

        def reporthook(block_num: int, block_size: int, total_size: int) -> None:
            if progress_callback and total_size > 0:
                downloaded = block_num * block_size
                progress = min(downloaded / total_size, 1.0)
                progress_callback(offset + progress * weight)

        urllib.request.urlretrieve(url, dest, reporthook=reporthook if progress_callback else None)

    def remove_voice(self, voice_id: str) -> bool:
        """Remove an installed voice.

        Args:
            voice_id: The voice identifier to remove.

        Returns:
            True if voice was removed, False if not found.
        """
        onnx_path = self.get_voice_path(voice_id)
        json_path = onnx_path.with_suffix(".onnx.json")

        removed = False
        if onnx_path.exists():
            onnx_path.unlink()
            removed = True
        if json_path.exists():
            json_path.unlink()
            removed = True

        if removed:
            logger.info(f"Voice {voice_id} removed")

        return removed

    def get_installed_voices(self) -> list[str]:
        """Get list of installed voice IDs.

        Returns:
            List of voice IDs that are installed.
        """
        return [voice_id for voice_id in [str(e["id"]) for e in VOICE_CATALOG] if self.is_installed(voice_id)]
