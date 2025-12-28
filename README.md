---
title: Reachy Mini Local Companion
emoji: 👋
colorFrom: red
colorTo: blue
sdk: static
pinned: false
short_description: Local AI companion for Reachy Mini with voice and emotions
tags:
 - reachy_mini
 - reachy_mini_python_app
---

# Reachy Mini Local Companion

A modular local AI companion application for the Pollen Robotics Reachy Mini robot. Features voice interaction, LLM chat, expressive emotions, and more.

## Features

| Capability | Description | Dependencies |
|------------|-------------|--------------|
| **STT** | Speech-to-Text with wake word detection | vosk, faster-whisper, openwakeword |
| **LLM** | Multi-provider chat with personality profiles | pydantic-ai |
| **TTS** | Neural text-to-speech synthesis | piper-tts |
| **Emotions** | Expressive head/antenna animations | (none - built-in) |
| **Volume** | Speaker volume control | (with TTS) |
| **Vision** | Camera-based features | (planned) |

## Modular Testing with Git Worktrees

This project supports isolated testing of individual capabilities using git worktrees. Each capability has its own branch with minimal dependencies.

### Quick Start

```bash
# Set up all worktrees (one-time)
git worktree add worktrees/stt feature/stt
git worktree add worktrees/llm feature/llm
git worktree add worktrees/tts feature/tts
git worktree add worktrees/emotions feature/emotions
git worktree add worktrees/volume feature/volume
git worktree add worktrees/vision feature/vision

# List worktrees
git worktree list
```

### Testing a Single Capability

```bash
# Navigate to the capability worktree
cd worktrees/emotions

# Create virtual environment and install minimal deps
uv venv && source .venv/bin/activate
uv pip install -e .

# Copy and configure feature flags
cp .env.example .env

# Run the app
python -m reachy_mini_local_companion.main
```

### Worktree Directory Structure

```
reachy_mini_local_companion/
├── worktrees/
│   ├── stt/        # STT-only testing (feature/stt branch)
│   ├── llm/        # LLM-only testing (feature/llm branch)
│   ├── tts/        # TTS-only testing (feature/tts branch)
│   ├── emotions/   # Emotions-only testing (feature/emotions branch)
│   ├── volume/     # Volume control testing (feature/volume branch)
│   └── vision/     # Vision testing placeholder (feature/vision branch)
└── (main working directory - all features)
```

### Feature Flags

Control which capabilities are loaded at runtime via environment variables:

```bash
# Enable only STT
FEATURE_STT=true
FEATURE_LLM=false
FEATURE_TTS=false
FEATURE_EMOTIONS=false
FEATURE_VOLUME=true
FEATURE_VISION=false
```

The app will:
1. Skip importing disabled modules (reducing dependency requirements)
2. Skip registering disabled API endpoints
3. Skip processing for disabled features in the main loop

### API Endpoint: `/features`

Query enabled capabilities at runtime:

```bash
curl http://localhost:8042/features
# {"stt": true, "llm": false, "tts": false, "emotions": false, "volume": true, "vision": false}
```

## Development

### Full Installation (All Features)

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
```

### LLM Configuration

Set environment variables for your LLM provider:

```bash
export LLM_PROVIDER=ollama  # or: openai, azure, openrouter, custom
export LLM_MODEL=llama3.1
export LLM_BASE_URL=http://localhost:11434  # optional
export LLM_API_KEY=your-key  # if required
```

## License

See LICENSE file.
