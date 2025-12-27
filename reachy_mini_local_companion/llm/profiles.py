"""Profile storage and management for LLM chat."""

import json
import logging
from datetime import datetime
from pathlib import Path

from reachy_mini_local_companion.llm.models import Profile, ProfileCreate, ProfileUpdate

logger = logging.getLogger(__name__)

# Default profiles to create on first run
DEFAULT_PROFILES = [
    Profile(
        id="friendly",
        name="Friendly Robot",
        system_prompt=(
            "You are Reachy, a friendly and warm robot companion. "
            "You speak in a cheerful, encouraging tone and love to help people. "
            "You're curious about humans and enjoy learning about their day. "
            "Keep responses concise but warm. Use simple language."
        ),
        description="A warm, encouraging personality that loves to help",
    ),
    Profile(
        id="curious",
        name="Curious Explorer",
        system_prompt=(
            "You are Reachy, an endlessly curious robot who loves learning. "
            "You ask thoughtful follow-up questions to understand things better. "
            "You're fascinated by how things work and love sharing interesting facts. "
            "Keep responses brief but always include a question to continue the conversation."
        ),
        description="An inquisitive personality that asks follow-up questions",
    ),
    Profile(
        id="helpful",
        name="Helpful Assistant",
        system_prompt=(
            "You are Reachy, a professional and efficient robot assistant. "
            "You provide clear, concise answers focused on being helpful. "
            "You're reliable, accurate, and task-oriented. "
            "Keep responses short and to the point."
        ),
        description="A professional, task-focused personality",
    ),
]


class ProfileStore:
    """Manages profile storage and retrieval."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Initialize the profile store.

        Args:
            storage_path: Path to the JSON file for profile storage.
                         If None, uses default location in user's home directory.
        """
        if storage_path is None:
            storage_path = Path.home() / ".cache" / "reachy_mini" / "profiles.json"

        self._storage_path = storage_path
        self._profiles: dict[str, Profile] = {}
        self._load()

    def _load(self) -> None:
        """Load profiles from storage."""
        if not self._storage_path.exists():
            logger.info("No profiles file found, creating defaults")
            self._create_defaults()
            return

        try:
            with open(self._storage_path) as f:
                data = json.load(f)

            for profile_data in data.get("profiles", []):
                profile = Profile(**profile_data)
                self._profiles[profile.id] = profile

            logger.info(f"Loaded {len(self._profiles)} profiles")
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to load profiles: {e}, creating defaults")
            self._create_defaults()

    def _save(self) -> None:
        """Save profiles to storage."""
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {"profiles": [p.model_dump(mode="json") for p in self._profiles.values()]}

        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.debug(f"Saved {len(self._profiles)} profiles")

    def _create_defaults(self) -> None:
        """Create default profiles."""
        for profile in DEFAULT_PROFILES:
            self._profiles[profile.id] = profile
        self._save()
        logger.info(f"Created {len(DEFAULT_PROFILES)} default profiles")

    def list_all(self) -> list[Profile]:
        """Get all profiles."""
        return list(self._profiles.values())

    def get(self, profile_id: str) -> Profile | None:
        """Get a profile by ID."""
        return self._profiles.get(profile_id)

    def get_default(self) -> Profile:
        """Get the default profile (first one)."""
        if not self._profiles:
            self._create_defaults()
        return next(iter(self._profiles.values()))

    def create(self, data: ProfileCreate) -> Profile:
        """Create a new profile."""
        profile = Profile(
            name=data.name,
            system_prompt=data.system_prompt,
            description=data.description,
        )
        self._profiles[profile.id] = profile
        self._save()
        logger.info(f"Created profile: {profile.name} ({profile.id})")
        return profile

    def update(self, profile_id: str, data: ProfileUpdate) -> Profile | None:
        """Update an existing profile."""
        profile = self._profiles.get(profile_id)
        if profile is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.now()
            updated_profile = profile.model_copy(update=update_data)
            self._profiles[profile_id] = updated_profile
            self._save()
            logger.info(f"Updated profile: {profile_id}")
            return updated_profile

        return profile

    def delete(self, profile_id: str) -> bool:
        """Delete a profile by ID."""
        if profile_id not in self._profiles:
            return False

        # Don't allow deleting the last profile
        if len(self._profiles) <= 1:
            logger.warning("Cannot delete the last profile")
            return False

        del self._profiles[profile_id]
        self._save()
        logger.info(f"Deleted profile: {profile_id}")
        return True
