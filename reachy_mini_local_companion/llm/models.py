"""Pydantic models for LLM chat functionality."""

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def generate_id() -> str:
    """Generate a unique ID for profiles."""
    return uuid4().hex[:8]


class Profile(BaseModel):
    """A personality profile for the LLM agent."""

    id: str = Field(default_factory=generate_id)
    name: str = Field(..., min_length=1, max_length=100)
    system_prompt: str = Field(..., min_length=1)
    description: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProfileCreate(BaseModel):
    """Request model for creating a new profile."""

    name: str = Field(..., min_length=1, max_length=100)
    system_prompt: str = Field(..., min_length=1)
    description: str = Field(default="")


class ProfileUpdate(BaseModel):
    """Request model for updating a profile."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    system_prompt: str | None = Field(default=None, min_length=1)
    description: str | None = None


class ChatMessage(BaseModel):
    """A single chat message."""

    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request model for sending a chat message."""

    message: str = Field(..., min_length=1)
    profile_id: str | None = None


class ChatResponse(BaseModel):
    """Response model for chat messages."""

    message: str
    profile_id: str
    profile_name: str


class ProviderType(str, Enum):
    """Supported LLM provider types."""

    OLLAMA = "ollama"
    OPENAI = "openai"
    AZURE = "azure"
    OPENROUTER = "openrouter"
    CUSTOM = "custom"


class ProviderConfig(BaseModel):
    """Configuration for the LLM provider."""

    provider: ProviderType = ProviderType.OLLAMA
    model: str = "llama3.1"
    base_url: str | None = None
    api_key: str | None = None


class ProviderStatus(BaseModel):
    """Status of the LLM provider connection."""

    connected: bool
    provider: str
    model: str
    error: str | None = None
