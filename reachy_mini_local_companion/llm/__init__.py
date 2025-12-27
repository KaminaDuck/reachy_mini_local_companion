"""LLM Chat module for Reachy Mini Local Companion.

This module provides LLM integration using Pydantic AI with support for
multiple providers (Ollama, OpenAI, Azure, etc.) and custom personality profiles.
"""

from reachy_mini_local_companion.llm.agent import LLMChatAgent
from reachy_mini_local_companion.llm.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    Profile,
    ProviderConfig,
    ProviderStatus,
)
from reachy_mini_local_companion.llm.profiles import ProfileStore

__all__ = [
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "LLMChatAgent",
    "Profile",
    "ProfileStore",
    "ProviderConfig",
    "ProviderStatus",
]
