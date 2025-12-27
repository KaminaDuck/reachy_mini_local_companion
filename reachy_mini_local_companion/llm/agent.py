"""Pydantic AI agent for LLM chat functionality."""

import logging
import os
from typing import Any

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage

from reachy_mini_local_companion.llm.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    Profile,
    ProviderConfig,
    ProviderStatus,
    ProviderType,
)
from reachy_mini_local_companion.llm.profiles import ProfileStore

logger = logging.getLogger(__name__)


def get_provider_config_from_env() -> ProviderConfig:
    """Build provider configuration from environment variables.

    Environment variables:
        LLM_PROVIDER: Provider type (ollama, openai, azure, openrouter, custom)
        LLM_MODEL: Model name (e.g., llama3.1, gpt-4o)
        LLM_BASE_URL: Custom base URL for API (optional)
        LLM_API_KEY: API key (optional, uses provider-specific env vars as fallback)
    """
    provider_str = os.environ.get("LLM_PROVIDER", "ollama").lower()

    try:
        provider = ProviderType(provider_str)
    except ValueError:
        logger.warning(f"Unknown provider '{provider_str}', defaulting to ollama")
        provider = ProviderType.OLLAMA

    model = os.environ.get("LLM_MODEL", "llama3.1")
    base_url = os.environ.get("LLM_BASE_URL")
    api_key = os.environ.get("LLM_API_KEY")

    return ProviderConfig(
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
    )


def build_model_string(config: ProviderConfig) -> str:
    """Build the model string for Pydantic AI Agent.

    Returns a string like 'ollama:llama3.1' or 'openai:gpt-4o'.
    """
    return f"{config.provider.value}:{config.model}"


class LLMChatAgent:
    """LLM chat agent using Pydantic AI.

    Manages conversations with support for:
    - Multiple LLM providers (Ollama, OpenAI, Azure, etc.)
    - Custom personality profiles via system prompts
    - Multi-turn conversation history
    """

    def __init__(
        self,
        profile_store: ProfileStore,
        config: ProviderConfig | None = None,
    ) -> None:
        """Initialize the chat agent.

        Args:
            profile_store: Store for managing profiles.
            config: Provider configuration. If None, reads from environment.
        """
        self._profile_store = profile_store
        self._config = config or get_provider_config_from_env()
        self._current_profile: Profile | None = None
        self._message_history: list[ModelMessage] = []
        self._agent: Agent[None, str] | None = None
        self._connected = False
        self._last_error: str | None = None

        # Set initial profile
        self._current_profile = profile_store.get_default()

    def _create_agent(self, profile: Profile) -> Agent[None, str]:
        """Create a new Pydantic AI agent with the given profile."""
        model_string = build_model_string(self._config)

        logger.info(f"Creating agent with model: {model_string}, profile: {profile.name}")

        return Agent(
            model_string,
            system_prompt=profile.system_prompt,
        )

    def get_status(self) -> ProviderStatus:
        """Get the current provider status."""
        return ProviderStatus(
            connected=self._connected,
            provider=self._config.provider.value,
            model=self._config.model,
            error=self._last_error,
        )

    def get_current_profile(self) -> Profile | None:
        """Get the currently active profile."""
        return self._current_profile

    def set_profile(self, profile_id: str) -> Profile | None:
        """Set the active profile and clear conversation history.

        Args:
            profile_id: ID of the profile to activate.

        Returns:
            The activated profile, or None if not found.
        """
        profile = self._profile_store.get(profile_id)
        if profile is None:
            logger.warning(f"Profile not found: {profile_id}")
            return None

        if self._current_profile and self._current_profile.id == profile_id:
            return profile

        logger.info(f"Switching to profile: {profile.name}")
        self._current_profile = profile
        self._agent = None  # Force recreation with new system prompt
        self._message_history = []  # Clear history on profile switch

        return profile

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a message and get a response.

        Args:
            request: The chat request containing the message and optional profile_id.

        Returns:
            The chat response with the assistant's message.

        Raises:
            RuntimeError: If no profile is set or agent creation fails.
        """
        # Handle profile selection
        if request.profile_id:
            profile = self.set_profile(request.profile_id)
            if profile is None:
                raise ValueError(f"Profile not found: {request.profile_id}")
        elif self._current_profile is None:
            self._current_profile = self._profile_store.get_default()

        profile = self._current_profile
        if profile is None:
            raise RuntimeError("No profile available")

        # Create or reuse agent
        if self._agent is None:
            self._agent = self._create_agent(profile)

        # Run the agent
        try:
            result = await self._agent.run(
                request.message,
                message_history=self._message_history if self._message_history else None,
            )

            # Update history with new messages
            self._message_history = result.all_messages()
            self._connected = True
            self._last_error = None

            return ChatResponse(
                message=result.output,
                profile_id=profile.id,
                profile_name=profile.name,
            )

        except Exception as e:
            logger.error(f"Chat error: {e}")
            self._connected = False
            self._last_error = str(e)
            raise RuntimeError(f"Failed to get response from LLM: {e}") from e

    def chat_sync(self, request: ChatRequest) -> ChatResponse:
        """Synchronous version of chat for non-async contexts.

        Args:
            request: The chat request containing the message and optional profile_id.

        Returns:
            The chat response with the assistant's message.
        """
        # Handle profile selection
        if request.profile_id:
            profile = self.set_profile(request.profile_id)
            if profile is None:
                raise ValueError(f"Profile not found: {request.profile_id}")
        elif self._current_profile is None:
            self._current_profile = self._profile_store.get_default()

        profile = self._current_profile
        if profile is None:
            raise RuntimeError("No profile available")

        # Create or reuse agent
        if self._agent is None:
            self._agent = self._create_agent(profile)

        # Run the agent synchronously
        try:
            result = self._agent.run_sync(
                request.message,
                message_history=self._message_history if self._message_history else None,
            )

            # Update history with new messages
            self._message_history = result.all_messages()
            self._connected = True
            self._last_error = None

            return ChatResponse(
                message=result.output,
                profile_id=profile.id,
                profile_name=profile.name,
            )

        except Exception as e:
            logger.error(f"Chat error: {e}")
            self._connected = False
            self._last_error = str(e)
            raise RuntimeError(f"Failed to get response from LLM: {e}") from e

    def get_history(self) -> list[ChatMessage]:
        """Get the conversation history as ChatMessage objects."""
        messages: list[ChatMessage] = []

        for msg in self._message_history:
            # Extract user messages
            if hasattr(msg, "parts"):
                for part in msg.parts:
                    if hasattr(part, "content"):
                        role = "user" if msg.__class__.__name__ == "ModelRequest" else "assistant"
                        # Skip system prompts
                        if part.__class__.__name__ == "SystemPromptPart":
                            continue
                        messages.append(
                            ChatMessage(
                                role=role,  # type: ignore[arg-type]
                                content=str(part.content),
                            )
                        )

        return messages

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._message_history = []
        logger.info("Conversation history cleared")

    def get_config(self) -> dict[str, Any]:
        """Get the current configuration as a dictionary."""
        return {
            "provider": self._config.provider.value,
            "model": self._config.model,
            "base_url": self._config.base_url,
            "current_profile": self._current_profile.id if self._current_profile else None,
        }
