# Feature: LLM Chat with Custom Profiles

## Feature Description
Add a capability to send user queries to a large language model (LLM) from the Reachy Mini companion app. The LLM can be hosted on a local network server (e.g., Ollama, vLLM, LM Studio) or in the cloud (OpenAI, Azure, etc.). Users can create and select custom profiles that define system prompts, allowing the robot to adopt different personalities or roles during conversations. The feature integrates with the existing web control panel and stores conversation history for multi-turn interactions.

## User Story
As a Reachy Mini user
I want to send messages to an LLM through my robot companion
So that I can have interactive conversations with the robot using different personality profiles

## Problem Statement
Currently, the Reachy Mini Local Companion app only provides basic motor control (head movement, antenna animation) and sound playback. Users cannot have conversational interactions with the robot. There is no way to leverage LLMs for natural language interaction, personality customization, or intelligent responses, limiting the robot's utility as a companion.

## Solution Statement
Implement an LLM chat feature using Pydantic AI that:
1. Supports multiple LLM providers (local via Ollama/vLLM and cloud via OpenAI-compatible APIs)
2. Allows custom profiles with configurable system prompts for different robot personalities
3. Maintains conversation history for multi-turn interactions
4. Exposes REST API endpoints for chat functionality
5. Provides a web UI for sending messages and managing profiles
6. Stores profiles persistently in JSON format

## Relevant Files
Use these files to implement the feature:

- [main.py](reachy_mini_local_companion/main.py) - Main app entry point; add new FastAPI endpoints for chat and profiles here
- [static/index.html](reachy_mini_local_companion/static/index.html) - Web UI; add chat interface elements
- [static/main.js](reachy_mini_local_companion/static/main.js) - Frontend JavaScript; add chat and profile management logic
- [static/style.css](reachy_mini_local_companion/static/style.css) - Styles for the web UI; add chat panel styles
- [pyproject.toml](pyproject.toml) - Add new dependencies (`pydantic-ai-slim[openai]`)
- [.claude/references/python/pydantic-ai/agents.md](.claude/references/python/pydantic-ai/agents.md) - Reference for Pydantic AI agent patterns
- [.claude/references/python/pydantic-ai/openai-integration.md](.claude/references/python/pydantic-ai/openai-integration.md) - Reference for OpenAI-compatible provider configuration

### New Files
- `reachy_mini_local_companion/llm/` - New module for LLM functionality
  - `__init__.py` - Module exports
  - `agent.py` - Pydantic AI agent configuration and chat logic
  - `profiles.py` - Profile management (CRUD operations, persistence)
  - `models.py` - Pydantic models for chat requests/responses and profiles
- `reachy_mini_local_companion/profiles.json` - Default profiles storage file

## Implementation Plan

### Phase 1: Foundation
Set up the LLM module structure and core dependencies:
1. Add `pydantic-ai-slim[openai]` dependency to pyproject.toml
2. Create the `llm/` module with models for chat and profiles
3. Implement profile persistence layer (load/save from JSON)
4. Create default profiles (e.g., "Friendly Assistant", "Curious Robot", "Helpful Guide")

### Phase 2: Core Implementation
Implement the Pydantic AI agent and chat functionality:
1. Create a configurable agent that accepts dynamic system prompts from profiles
2. Implement conversation history management per session
3. Support multiple LLM providers via environment variables:
   - `LLM_PROVIDER`: Provider shorthand (e.g., `ollama`, `openai`, `azure`)
   - `LLM_MODEL`: Model name (e.g., `llama3.1`, `gpt-4o`)
   - `LLM_BASE_URL`: Custom base URL for local servers (optional)
   - `LLM_API_KEY`: API key for cloud providers (optional)
4. Add error handling for connection failures and API errors

### Phase 3: Integration
Integrate with the existing FastAPI settings app and web UI:
1. Add REST endpoints to the settings app:
   - `GET /profiles` - List all profiles
   - `POST /profiles` - Create new profile
   - `GET /profiles/{id}` - Get profile by ID
   - `PUT /profiles/{id}` - Update profile
   - `DELETE /profiles/{id}` - Delete profile
   - `POST /chat` - Send message and get response
   - `DELETE /chat/history` - Clear conversation history
2. Extend the web UI with:
   - Profile selector dropdown
   - Chat message input and send button
   - Chat history display panel
   - Profile management modal (create/edit/delete)
3. Add provider configuration status indicator

## Step by Step Tasks

### Step 1: Add Dependencies
- Add `pydantic-ai-slim[openai]` to `pyproject.toml` dependencies
- Run `uv sync` to install the new dependency
- Verify installation with `uv run python -c "import pydantic_ai; print('OK')"`

### Step 2: Create LLM Module Structure
- Create `reachy_mini_local_companion/llm/` directory
- Create `__init__.py` with module exports
- Create `models.py` with Pydantic models:
  - `Profile(id, name, system_prompt, description, created_at, updated_at)`
  - `ChatMessage(role, content, timestamp)`
  - `ChatRequest(message, profile_id)`
  - `ChatResponse(message, profile_id, conversation_id)`
  - `ProviderConfig(provider, model, base_url, api_key)`

### Step 3: Implement Profile Persistence
- Create `profiles.py` with profile management:
  - `ProfileStore` class with CRUD operations
  - Load profiles from `profiles.json` on initialization
  - Save profiles to `profiles.json` on modifications
  - Include default profiles if file doesn't exist
- Create default `profiles.json` with 3 starter profiles:
  - "Friendly Robot" - warm, encouraging personality
  - "Curious Explorer" - inquisitive, asks follow-up questions
  - "Helpful Assistant" - professional, task-focused

### Step 4: Implement Pydantic AI Agent
- Create `agent.py` with:
  - `LLMChatAgent` class wrapping Pydantic AI Agent
  - Dynamic model/provider configuration from environment
  - Method to update system prompt when profile changes
  - Conversation history storage and retrieval
  - Support for `ollama:`, `openai:`, `azure:` provider prefixes
- Handle graceful degradation when LLM is unavailable

### Step 5: Add API Endpoints to Main App
- Add imports for LLM module in `main.py`
- Instantiate `ProfileStore` and `LLMChatAgent` in the run method
- Add profile endpoints:
  - `GET /profiles` - return list of all profiles
  - `POST /profiles` - create new profile, return created profile
  - `GET /profiles/{profile_id}` - return specific profile
  - `PUT /profiles/{profile_id}` - update profile
  - `DELETE /profiles/{profile_id}` - delete profile
- Add chat endpoints:
  - `POST /chat` - send message with profile_id, return response
  - `DELETE /chat/history` - clear conversation history
  - `GET /chat/status` - return LLM provider status (connected/disconnected)

### Step 6: Extend Web UI - HTML Structure
- Add to `static/index.html`:
  - Chat panel container with message display area
  - Message input field with send button
  - Profile selector dropdown
  - "Manage Profiles" button
  - Profile management modal (list, create, edit, delete)
  - LLM status indicator (connected/disconnected)

### Step 7: Extend Web UI - JavaScript Logic
- Add to `static/main.js`:
  - `loadProfiles()` - fetch and populate profile dropdown
  - `selectProfile(id)` - update active profile
  - `sendMessage(text)` - POST to /chat, append response to display
  - `clearHistory()` - DELETE /chat/history
  - `createProfile(name, systemPrompt)` - POST to /profiles
  - `updateProfile(id, data)` - PUT to /profiles/{id}
  - `deleteProfile(id)` - DELETE to /profiles/{id}
  - `checkLLMStatus()` - GET /chat/status, update indicator
  - Chat history rendering with user/assistant message styling

### Step 8: Extend Web UI - Styling
- Add to `static/style.css`:
  - Chat panel layout (flexbox column)
  - Message bubbles (user vs assistant styling)
  - Profile selector and status indicator styles
  - Modal styles for profile management
  - Loading/sending states
  - Responsive design for different screen sizes

### Step 9: Add Unit Tests
- Create `tests/` directory if not exists
- Create `tests/test_profiles.py`:
  - Test profile CRUD operations
  - Test persistence to JSON
  - Test default profile creation
- Create `tests/test_chat.py`:
  - Test chat request/response models
  - Test conversation history management
  - Mock LLM responses for testing

### Step 10: Integration Testing and Validation
- Run all validation commands to ensure zero regressions
- Test with Ollama local server (if available)
- Test profile switching during conversation
- Test error handling when LLM is unavailable
- Verify web UI functions correctly

## Testing Strategy

### Unit Tests
- `test_profiles.py`: Test ProfileStore CRUD operations, JSON persistence, default profile generation
- `test_models.py`: Test Pydantic model validation for Profile, ChatRequest, ChatResponse
- `test_agent.py`: Test LLMChatAgent initialization, history management (mock LLM calls)

### Integration Tests
- Test full request/response cycle through FastAPI endpoints
- Test profile selection affects system prompt in agent
- Test conversation history accumulates correctly
- Test error responses for invalid profile IDs

### Edge Cases
- Empty message handling (should reject or handle gracefully)
- Very long messages (token limit considerations)
- Missing/invalid profile_id in chat request
- LLM provider unavailable (connection timeout, API error)
- Concurrent chat requests
- Profile deletion while in use
- Invalid JSON in profiles.json (graceful recovery)
- Empty profiles.json (should create defaults)

## Acceptance Criteria
- [ ] Users can send text messages to an LLM and receive responses via the web UI
- [ ] Users can select from multiple personality profiles before chatting
- [ ] Users can create, edit, and delete custom profiles with unique system prompts
- [ ] Conversation history persists within a session for multi-turn interactions
- [ ] The app supports both local (Ollama) and cloud (OpenAI) LLM providers via environment variables
- [ ] The UI displays connection status for the configured LLM provider
- [ ] Error messages are displayed when the LLM is unavailable
- [ ] All existing functionality (antenna control, sound playback) continues to work
- [ ] Unit tests cover profile management and chat models with >80% coverage
- [ ] The feature works without any LLM configured (graceful degradation with error message)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `uv sync` - Ensure all dependencies are installed
- `uv run python -c "from reachy_mini_local_companion.llm import ProfileStore, LLMChatAgent; print('Imports OK')"` - Verify LLM module imports
- `uv run python -c "from pydantic_ai import Agent; print('Pydantic AI OK')"` - Verify Pydantic AI installation
- `uv run pytest tests/ -v` - Run all unit tests with verbose output
- `uv run python -m reachy_mini_local_companion.main &; sleep 3; curl -s http://localhost:8042/profiles | python -m json.tool; kill %1` - Test profiles endpoint (if running locally)

## Notes

### New Dependencies
- `pydantic-ai-slim[openai]` - Pydantic AI framework with OpenAI-compatible provider support

### Environment Variables
The following environment variables configure the LLM provider:
- `LLM_PROVIDER`: Provider prefix (default: `ollama`)
- `LLM_MODEL`: Model name (default: `llama3.1`)
- `LLM_BASE_URL`: Custom base URL for local servers (optional, e.g., `http://localhost:11434/v1`)
- `LLM_API_KEY`: API key for cloud providers (optional, uses provider-specific env vars as fallback)

### Future Considerations
- **Streaming responses**: Implement `run_stream()` for real-time token-by-token display
- **Voice input**: Integrate with existing microphone capabilities for speech-to-text
- **Voice output**: Use speaker to read LLM responses aloud (TTS integration)
- **Robot reactions**: Trigger head/antenna movements based on LLM response sentiment
- **Persistent history**: Save conversation history across sessions to a database
- **Profile sharing**: Export/import profiles as JSON files

### Provider Examples
```bash
# Ollama (local)
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3.1

# OpenAI (cloud)
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o
export OPENAI_API_KEY=sk-...

# Azure OpenAI
export LLM_PROVIDER=azure
export LLM_MODEL=gpt-4o
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
export AZURE_OPENAI_API_KEY=...
export OPENAI_API_VERSION=2024-08-01-preview

# Local vLLM server
export LLM_PROVIDER=openai
export LLM_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct
export LLM_BASE_URL=http://localhost:8000/v1
export LLM_API_KEY=not-needed
```
