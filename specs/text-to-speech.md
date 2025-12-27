# Feature: Local Text-to-Speech with Model Selection

## Feature Description

Add local, privacy-preserving text-to-speech (TTS) capability to the Reachy Mini Local Companion app. This feature uses locally-running neural TTS models to synthesize speech from text, playing audio through the Reachy Mini's built-in speaker via `mini.speaker.play()`. Users can select from multiple TTS voice models (Piper voices in different qualities and languages) based on their voice quality and performance preferences. This feature completes the voice interaction pipeline alongside the existing STT and LLM chat features.

## User Story

As a **Reachy Mini user**
I want to **have my robot speak responses aloud using natural-sounding voices**
So that **I can have hands-free, natural conversations with my robot without reading a screen**

## Problem Statement

Currently, the Reachy Mini Local Companion app provides text-based LLM chat responses that users must read on screen. There is no voice output capability, limiting natural conversational interaction. Users who want a complete voice assistant experience (speak → understand → respond → speak back) cannot achieve this with the current feature set. Additionally, cloud-based TTS services raise privacy concerns and require internet connectivity.

## Solution Statement

Implement a local TTS pipeline using Piper TTS, a fast neural text-to-speech system optimized for Raspberry Pi:

1. **TTS Engine**: Use Piper TTS with ONNX voice models for efficient local synthesis
2. **Voice Model Selection**: Allow users to choose from multiple Piper voices (different languages, qualities, speakers)
3. **Audio Output**: Play synthesized audio through the Reachy Mini's speaker via `mini.speaker.play()`
4. **Web UI Integration**: Add voice selection controls and TTS status to the existing control panel
5. **LLM Integration**: Optionally auto-speak LLM chat responses
6. **Streaming Support**: Support streaming synthesis for lower latency on longer text

## Relevant Files

Use these files to implement the feature:

- [main.py](reachy_mini_local_companion/main.py) - Core app class; add TTS endpoints and integrate with speaker
- [static/index.html](reachy_mini_local_companion/static/index.html) - Add TTS controls (voice selector, test button, auto-speak toggle)
- [static/main.js](reachy_mini_local_companion/static/main.js) - Add frontend logic for TTS configuration and testing
- [static/style.css](reachy_mini_local_companion/static/style.css) - Style new TTS UI components
- [pyproject.toml](pyproject.toml) - Add new dependencies (piper-tts)
- [.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md](.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md) - SDK reference for speaker API (`mini.speaker.play()`)
- [specs/llm-chat-with-profiles.md](specs/llm-chat-with-profiles.md) - LLM chat spec for TTS integration with chat responses

### New Files

- `reachy_mini_local_companion/tts/__init__.py` - TTS module init
- `reachy_mini_local_companion/tts/engine.py` - Piper TTS engine wrapper
- `reachy_mini_local_companion/tts/voice_manager.py` - Voice model management (download, list, select)
- `reachy_mini_local_companion/tts/models.py` - Pydantic models for TTS configuration
- `tests/test_tts.py` - Unit tests for TTS module

## Implementation Plan

### Phase 1: Foundation

1. **Add Dependencies**: Update `pyproject.toml` with required packages:
   - `piper-tts` - Fast neural TTS with ONNX runtime
   - `soundfile` - Audio file handling (may already be available via reachy-mini)

2. **Create TTS Module Structure**: Establish the `tts/` subpackage with voice management

3. **Implement Voice Model Manager**: Handle voice model discovery, downloading, and selection
   - Store models in `~/.cache/reachy_mini/tts_models/`
   - Support downloading voices from Hugging Face on first use

### Phase 2: Core Implementation

1. **Piper TTS Engine**: Implement `PiperTTSEngine` class
   - Load Piper voice models (ONNX + JSON config)
   - `synthesize(text: str) -> bytes` for batch synthesis
   - `synthesize_stream(text: str) -> Iterator[bytes]` for streaming
   - Handle voice switching without restart

2. **Voice Configuration**: Implement voice model metadata
   - Parse Piper voice JSON configs for sample rate, language info
   - Provide voice preview capability
   - Track installed vs available voices

3. **Audio Playback Integration**: Connect to Reachy Mini speaker
   - Convert Piper audio output to format expected by `mini.speaker.play()`
   - Handle sample rate conversion if needed

### Phase 3: Integration

1. **FastAPI Endpoints**: Add REST endpoints to `main.py`:
   - `GET /tts/voices` - List available and installed voices
   - `POST /tts/voices/{voice_id}/install` - Download and install a voice
   - `DELETE /tts/voices/{voice_id}` - Remove an installed voice
   - `GET /tts/config` - Get current TTS configuration
   - `POST /tts/config` - Update TTS configuration (selected voice, auto-speak)
   - `POST /tts/speak` - Synthesize and play text immediately
   - `POST /tts/preview` - Preview a voice with sample text

2. **LLM Chat Integration**: Add auto-speak option
   - When enabled, automatically speak LLM responses
   - Add toggle in chat UI
   - Handle long responses with streaming synthesis

3. **Web UI Updates**: Extend control panel with:
   - Voice selector dropdown (installed voices)
   - Install/remove voice buttons
   - Test speak button with sample text input
   - Auto-speak LLM responses toggle
   - Speaking status indicator
   - Volume control (if supported by speaker API)

## Step by Step Tasks

### Step 1: Add Dependencies

- Update `pyproject.toml` to include new dependencies:
  ```toml
  dependencies = [
      "reachy-mini",
      "piper-tts>=1.2.0",
  ]
  ```
- Run `uv sync` to install dependencies
- Verify installation: `uv run python -c "from piper.voice import PiperVoice; print('Piper OK')"`

### Step 2: Create TTS Module Structure

- Create `reachy_mini_local_companion/tts/` directory
- Create `__init__.py` with exports:
  ```python
  from .engine import PiperTTSEngine
  from .voice_manager import VoiceManager
  from .models import TTSConfig, VoiceInfo
  ```
- Create `models.py` with Pydantic models:
  ```python
  from pydantic import BaseModel
  from typing import Optional
  from enum import Enum

  class VoiceQuality(str, Enum):
      LOW = "low"        # x_low - fastest, smallest
      MEDIUM = "medium"  # medium - balanced
      HIGH = "high"      # high - best quality

  class VoiceInfo(BaseModel):
      id: str                    # e.g., "en_US-lessac-medium"
      name: str                  # e.g., "Lessac (US English)"
      language: str              # e.g., "en_US"
      quality: VoiceQuality
      sample_rate: int           # e.g., 22050
      installed: bool
      size_mb: float             # Model size in MB

  class TTSConfig(BaseModel):
      enabled: bool = True
      selected_voice: str = "en_US-lessac-medium"
      auto_speak_llm: bool = False
      speaking_rate: float = 1.0  # Speech speed multiplier
  ```

### Step 3: Implement Voice Manager

- Create `voice_manager.py`:
  ```python
  class VoiceManager:
      VOICE_CATALOG = [
          # Popular English voices
          {"id": "en_US-lessac-medium", "name": "Lessac (US)", "lang": "en_US", "quality": "medium", "size_mb": 75},
          {"id": "en_US-lessac-high", "name": "Lessac HQ (US)", "lang": "en_US", "quality": "high", "size_mb": 95},
          {"id": "en_US-amy-medium", "name": "Amy (US)", "lang": "en_US", "quality": "medium", "size_mb": 75},
          {"id": "en_GB-alan-medium", "name": "Alan (UK)", "lang": "en_GB", "quality": "medium", "size_mb": 75},
          {"id": "en_GB-cori-medium", "name": "Cori (UK)", "lang": "en_GB", "quality": "medium", "size_mb": 75},
          # Other languages
          {"id": "de_DE-thorsten-medium", "name": "Thorsten (German)", "lang": "de_DE", "quality": "medium", "size_mb": 75},
          {"id": "fr_FR-upmc-medium", "name": "UPMC (French)", "lang": "fr_FR", "quality": "medium", "size_mb": 75},
          {"id": "es_ES-davefx-medium", "name": "DaveFX (Spanish)", "lang": "es_ES", "quality": "medium", "size_mb": 75},
      ]

      def __init__(self, cache_dir: Path):
          self.cache_dir = cache_dir
          self.cache_dir.mkdir(parents=True, exist_ok=True)

      def list_voices(self) -> list[VoiceInfo]: ...
      def is_installed(self, voice_id: str) -> bool: ...
      def install_voice(self, voice_id: str, progress_callback=None) -> None: ...
      def remove_voice(self, voice_id: str) -> None: ...
      def get_voice_path(self, voice_id: str) -> Path: ...
  ```
- Implement voice download from Hugging Face: `https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{voice_id}.onnx`
- Include progress tracking for downloads

### Step 4: Implement Piper TTS Engine

- Create `engine.py`:
  ```python
  from piper.voice import PiperVoice
  import numpy as np
  import wave
  import io

  class PiperTTSEngine:
      def __init__(self, voice_manager: VoiceManager):
          self.voice_manager = voice_manager
          self.current_voice: PiperVoice | None = None
          self.current_voice_id: str | None = None

      def load_voice(self, voice_id: str) -> None:
          """Load a voice model. Downloads if not installed."""
          if not self.voice_manager.is_installed(voice_id):
              self.voice_manager.install_voice(voice_id)

          model_path = self.voice_manager.get_voice_path(voice_id)
          self.current_voice = PiperVoice.load(str(model_path))
          self.current_voice_id = voice_id

      def synthesize(self, text: str) -> bytes:
          """Synthesize text to WAV audio bytes."""
          if not self.current_voice:
              raise RuntimeError("No voice loaded")

          # Create in-memory WAV file
          audio_buffer = io.BytesIO()
          with wave.open(audio_buffer, 'wb') as wav_file:
              wav_file.setnchannels(1)
              wav_file.setsampwidth(2)  # 16-bit
              wav_file.setframerate(self.current_voice.config.sample_rate)
              self.current_voice.synthesize(text, wav_file)

          return audio_buffer.getvalue()

      def synthesize_stream(self, text: str) -> Iterator[bytes]:
          """Stream audio chunks for lower latency."""
          if not self.current_voice:
              raise RuntimeError("No voice loaded")

          for audio_bytes in self.current_voice.synthesize_stream_raw(text):
              yield audio_bytes

      @property
      def sample_rate(self) -> int:
          return self.current_voice.config.sample_rate if self.current_voice else 22050
  ```

### Step 5: Add Speaker Integration

- Update `engine.py` to include speaker helper:
  ```python
  def speak(self, text: str, reachy_mini) -> None:
      """Synthesize text and play through robot speaker."""
      audio_bytes = self.synthesize(text)

      # Write to temp file for speaker.play()
      # (adjust based on actual speaker API requirements)
      with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
          f.write(audio_bytes)
          temp_path = f.name

      try:
          reachy_mini.speaker.play(temp_path)
      finally:
          os.unlink(temp_path)
  ```
- Alternatively, if speaker supports raw audio buffer, use that directly

### Step 6: Add FastAPI Endpoints

- Update `main.py` to add TTS endpoints:
  ```python
  from reachy_mini_local_companion.tts import PiperTTSEngine, VoiceManager, TTSConfig, VoiceInfo

  # In run() method, before the main loop:
  voice_manager = VoiceManager(Path.home() / ".cache" / "reachy_mini" / "tts_models")
  tts_engine = PiperTTSEngine(voice_manager)
  tts_config = TTSConfig()

  # Load default voice if installed
  try:
      tts_engine.load_voice(tts_config.selected_voice)
  except Exception:
      pass  # Will be configured via UI

  @self.settings_app.get("/tts/voices")
  def list_voices() -> list[VoiceInfo]:
      return voice_manager.list_voices()

  @self.settings_app.post("/tts/voices/{voice_id}/install")
  def install_voice(voice_id: str):
      voice_manager.install_voice(voice_id)
      return {"status": "installed", "voice_id": voice_id}

  @self.settings_app.delete("/tts/voices/{voice_id}")
  def remove_voice(voice_id: str):
      voice_manager.remove_voice(voice_id)
      return {"status": "removed", "voice_id": voice_id}

  @self.settings_app.get("/tts/config")
  def get_tts_config() -> TTSConfig:
      return tts_config

  class TTSConfigUpdate(BaseModel):
      selected_voice: str | None = None
      auto_speak_llm: bool | None = None
      speaking_rate: float | None = None

  @self.settings_app.post("/tts/config")
  def update_tts_config(update: TTSConfigUpdate):
      nonlocal tts_config
      if update.selected_voice:
          tts_engine.load_voice(update.selected_voice)
          tts_config.selected_voice = update.selected_voice
      if update.auto_speak_llm is not None:
          tts_config.auto_speak_llm = update.auto_speak_llm
      if update.speaking_rate is not None:
          tts_config.speaking_rate = update.speaking_rate
      return tts_config

  class SpeakRequest(BaseModel):
      text: str

  @self.settings_app.post("/tts/speak")
  def speak_text(request: SpeakRequest):
      tts_engine.speak(request.text, reachy_mini)
      return {"status": "speaking", "text": request.text}

  @self.settings_app.post("/tts/preview")
  def preview_voice(voice_id: str):
      # Temporarily load voice for preview
      tts_engine.load_voice(voice_id)
      sample_text = "Hello! This is a preview of my voice."
      tts_engine.speak(sample_text, reachy_mini)
      # Reload original voice
      tts_engine.load_voice(tts_config.selected_voice)
      return {"status": "previewed", "voice_id": voice_id}
  ```

### Step 7: Integrate with LLM Chat (Optional)

- If LLM chat feature is implemented, modify chat endpoint to support auto-speak:
  ```python
  @self.settings_app.post("/chat")
  def chat(request: ChatRequest):
      response = llm_agent.chat(request.message, request.profile_id)

      # Auto-speak if enabled
      if tts_config.auto_speak_llm and tts_engine.current_voice:
          tts_engine.speak(response.message, reachy_mini)

      return response
  ```

### Step 8: Update Web UI - HTML

- Update `static/index.html` to add TTS section:
  ```html
  <div id="tts-controls">
      <h2>Text-to-Speech</h2>

      <div class="control-row">
          <label for="voice-select">Voice:</label>
          <select id="voice-select">
              <option value="">Select a voice...</option>
          </select>
          <button id="install-voice-btn" style="display:none;">Install</button>
      </div>

      <div class="control-row">
          <label>
              <input type="checkbox" id="auto-speak-checkbox">
              Auto-speak LLM responses
          </label>
      </div>

      <div class="control-row">
          <input type="text" id="test-text" placeholder="Enter text to speak...">
          <button id="speak-btn">Speak</button>
      </div>

      <div id="tts-status">Ready</div>
  </div>
  ```

### Step 9: Update Web UI - JavaScript

- Update `static/main.js`:
  ```javascript
  let voices = [];
  let ttsConfig = { selected_voice: '', auto_speak_llm: false };

  async function loadVoices() {
      const resp = await fetch('/tts/voices');
      voices = await resp.json();

      const select = document.getElementById('voice-select');
      select.innerHTML = '<option value="">Select a voice...</option>';

      // Group by installed status
      const installed = voices.filter(v => v.installed);
      const available = voices.filter(v => !v.installed);

      if (installed.length > 0) {
          const group = document.createElement('optgroup');
          group.label = 'Installed';
          installed.forEach(v => {
              const opt = document.createElement('option');
              opt.value = v.id;
              opt.textContent = `${v.name} (${v.quality})`;
              group.appendChild(opt);
          });
          select.appendChild(group);
      }

      if (available.length > 0) {
          const group = document.createElement('optgroup');
          group.label = 'Available to Install';
          available.forEach(v => {
              const opt = document.createElement('option');
              opt.value = v.id;
              opt.textContent = `${v.name} (${v.quality}) - ${v.size_mb}MB`;
              group.appendChild(opt);
          });
          select.appendChild(group);
      }

      select.value = ttsConfig.selected_voice;
  }

  async function loadTTSConfig() {
      const resp = await fetch('/tts/config');
      ttsConfig = await resp.json();
      document.getElementById('voice-select').value = ttsConfig.selected_voice;
      document.getElementById('auto-speak-checkbox').checked = ttsConfig.auto_speak_llm;
  }

  async function updateVoice(voiceId) {
      const voice = voices.find(v => v.id === voiceId);
      if (!voice) return;

      if (!voice.installed) {
          document.getElementById('tts-status').textContent = 'Installing voice...';
          await fetch(`/tts/voices/${voiceId}/install`, { method: 'POST' });
          await loadVoices();
      }

      await fetch('/tts/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ selected_voice: voiceId })
      });

      document.getElementById('tts-status').textContent = 'Voice loaded';
  }

  async function speakText() {
      const text = document.getElementById('test-text').value;
      if (!text) return;

      document.getElementById('tts-status').textContent = 'Speaking...';
      await fetch('/tts/speak', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
      });
      document.getElementById('tts-status').textContent = 'Ready';
  }

  async function updateAutoSpeak(enabled) {
      await fetch('/tts/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ auto_speak_llm: enabled })
      });
  }

  // Event listeners
  document.getElementById('voice-select').addEventListener('change', e => updateVoice(e.target.value));
  document.getElementById('speak-btn').addEventListener('click', speakText);
  document.getElementById('auto-speak-checkbox').addEventListener('change', e => updateAutoSpeak(e.target.checked));

  // Initialize
  loadTTSConfig().then(loadVoices);
  ```

### Step 10: Update Web UI - Styles

- Update `static/style.css`:
  ```css
  #tts-controls {
      margin-top: 24px;
      padding: 16px;
      border: 1px solid #ddd;
      border-radius: 8px;
  }

  #tts-controls h2 {
      margin-top: 0;
      margin-bottom: 16px;
  }

  .control-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
  }

  #voice-select {
      flex: 1;
      padding: 8px;
      border-radius: 4px;
      border: 1px solid #ccc;
  }

  #test-text {
      flex: 1;
      padding: 8px;
      border-radius: 4px;
      border: 1px solid #ccc;
  }

  #speak-btn {
      padding: 8px 16px;
      background-color: #27ae60;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
  }

  #speak-btn:hover {
      background-color: #219a52;
  }

  #tts-status {
      margin-top: 8px;
      font-style: italic;
      color: #666;
  }

  #install-voice-btn {
      padding: 8px 12px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
  }
  ```

### Step 11: Write Unit Tests

- Create `tests/test_tts.py`:
  ```python
  import pytest
  from pathlib import Path
  from unittest.mock import Mock, patch
  from reachy_mini_local_companion.tts import VoiceManager, PiperTTSEngine, TTSConfig, VoiceInfo

  @pytest.fixture
  def temp_cache_dir(tmp_path):
      return tmp_path / "tts_models"

  class TestVoiceManager:
      def test_list_voices_returns_catalog(self, temp_cache_dir):
          manager = VoiceManager(temp_cache_dir)
          voices = manager.list_voices()
          assert len(voices) > 0
          assert all(isinstance(v, VoiceInfo) for v in voices)

      def test_is_installed_false_initially(self, temp_cache_dir):
          manager = VoiceManager(temp_cache_dir)
          assert not manager.is_installed("en_US-lessac-medium")

      def test_install_voice_creates_files(self, temp_cache_dir):
          manager = VoiceManager(temp_cache_dir)
          with patch.object(manager, '_download_voice'):
              manager.install_voice("en_US-lessac-medium")
              # Would check file existence after download

  class TestPiperTTSEngine:
      def test_synthesize_requires_loaded_voice(self, temp_cache_dir):
          manager = VoiceManager(temp_cache_dir)
          engine = PiperTTSEngine(manager)

          with pytest.raises(RuntimeError, match="No voice loaded"):
              engine.synthesize("Hello")

      @patch('piper.voice.PiperVoice.load')
      def test_load_voice_sets_current(self, mock_load, temp_cache_dir):
          manager = VoiceManager(temp_cache_dir)
          engine = PiperTTSEngine(manager)

          with patch.object(manager, 'is_installed', return_value=True):
              with patch.object(manager, 'get_voice_path', return_value=Path("/fake/path.onnx")):
                  engine.load_voice("en_US-lessac-medium")
                  assert engine.current_voice_id == "en_US-lessac-medium"

  class TestTTSConfig:
      def test_default_values(self):
          config = TTSConfig()
          assert config.enabled is True
          assert config.selected_voice == "en_US-lessac-medium"
          assert config.auto_speak_llm is False
          assert config.speaking_rate == 1.0
  ```

### Step 12: Write Integration Tests

- Create `tests/test_tts_integration.py`:
  ```python
  import pytest
  from fastapi.testclient import TestClient

  # Integration tests would require mocking the Reachy Mini instance
  # and testing the full endpoint flow

  class TestTTSEndpoints:
      def test_list_voices_endpoint(self, client):
          response = client.get("/tts/voices")
          assert response.status_code == 200
          voices = response.json()
          assert isinstance(voices, list)

      def test_get_config_endpoint(self, client):
          response = client.get("/tts/config")
          assert response.status_code == 200
          config = response.json()
          assert "selected_voice" in config
          assert "auto_speak_llm" in config
  ```

### Step 13: Validate Feature

- Run all validation commands to ensure zero regressions
- Test voice installation and switching
- Test text synthesis and playback
- Verify auto-speak integration with LLM chat (if implemented)
- Test on actual Reachy Mini hardware

## Testing Strategy

### Unit Tests

- **VoiceManager**: Test voice catalog listing, installation status, download logic
- **PiperTTSEngine**: Test voice loading, synthesis output format, streaming behavior
- **TTSConfig**: Test configuration model validation and defaults

### Integration Tests

- **FastAPI Endpoints**: Test all TTS endpoints return correct schemas
- **Voice Installation Flow**: Test download → install → load → speak pipeline
- **Configuration Persistence**: Test config updates survive requests

### Edge Cases

- Empty text input (should handle gracefully, no audio)
- Very long text (chunking for streaming)
- Missing voice model file (clear error message)
- Voice download failure (network error handling)
- Speaker unavailable or busy (queue or reject)
- Invalid voice ID in config (fallback to default)
- Concurrent speak requests (queue or cancel previous)
- Unicode/emoji in text (proper handling)
- SSML or special markup (strip or support)

## Acceptance Criteria

- [ ] Users can select from at least 5 different voice models via the web UI
- [ ] Users can install new voices on-demand with progress feedback
- [ ] The robot speaks text aloud when the "Speak" button is pressed
- [ ] Voice synthesis completes within 2 seconds for a 20-word sentence on Raspberry Pi 4
- [ ] Auto-speak option correctly speaks LLM chat responses (if LLM feature is implemented)
- [ ] All existing functionality (antennas, sound playback, STT) continues working
- [ ] CPU usage stays below 50% during synthesis on Raspberry Pi 4
- [ ] Memory usage stays below 500MB with one voice loaded
- [ ] No audio data is sent to external servers (fully local)
- [ ] Unit tests cover TTS module with >80% coverage

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd /Users/duck/Projects/reachy_mini_local_companion && uv sync` - Install all dependencies
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -c "from piper.voice import PiperVoice; print('Piper OK')"` - Verify Piper import
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -c "from reachy_mini_local_companion.tts import PiperTTSEngine, VoiceManager; print('TTS module OK')"` - Verify TTS module imports
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run pytest tests/test_tts.py -v` - Run TTS unit tests
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run pytest tests/ -v` - Run all tests
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -m reachy_mini_local_companion.main` - Verify app starts without errors (Ctrl+C to exit)

## Notes

### New Dependencies

```toml
[project]
dependencies = [
    "reachy-mini",
    "piper-tts>=1.2.0",
]
```

### Voice Model Storage

Models are stored in `~/.cache/reachy_mini/tts_models/` to avoid bloating the package:
- Piper voices are typically 60-100MB each (ONNX + JSON config)
- First voice selection triggers download with progress indicator
- Multiple voices can be installed for different use cases

### Recommended Voices

| Voice ID | Language | Quality | Size | Notes |
|----------|----------|---------|------|-------|
| `en_US-lessac-medium` | English (US) | Medium | ~75MB | Default, good balance |
| `en_US-lessac-high` | English (US) | High | ~95MB | Best quality, slower |
| `en_GB-alan-medium` | English (UK) | Medium | ~75MB | British accent |
| `en_US-amy-medium` | English (US) | Medium | ~75MB | Female voice |
| `de_DE-thorsten-medium` | German | Medium | ~75MB | German language |
| `fr_FR-upmc-medium` | French | Medium | ~75MB | French language |
| `es_ES-davefx-medium` | Spanish | Medium | ~75MB | Spanish language |

### Performance Considerations

- **Raspberry Pi 4 (4GB)**: Medium quality voices recommended, ~1-2s latency for short sentences
- **Raspberry Pi 4 (8GB)**: High quality voices work well
- **Desktop/Laptop**: All voice qualities perform excellently

### Speaker API Integration

The Reachy Mini SDK provides `mini.speaker.play(audio_buffer)` for audio playback. Verify the expected audio format:
- Sample rate: May need conversion to match speaker hardware
- Format: PCM/WAV expected
- Blocking vs async: Check if play() blocks until complete

If the speaker API expects a file path instead of buffer, use a temporary file approach.

### Future Enhancements

- **SSML Support**: Parse Speech Synthesis Markup Language for expressive control
- **Voice Cloning**: Use Coqui TTS XTTS for custom voice cloning
- **Emotion Control**: Adjust voice parameters based on content sentiment
- **Multi-language Detection**: Auto-select voice based on text language
- **Speech Queue**: Queue multiple speak requests for sequential playback
- **Interrupt Support**: Cancel current speech when new text arrives

### References

- [Piper TTS GitHub](https://github.com/rhasspy/piper) - Fast local neural TTS
- [Piper Voices](https://rhasspy.github.io/piper-samples/) - Voice samples and models
- [Hugging Face Piper Models](https://huggingface.co/rhasspy/piper-voices) - Model downloads
- [Reachy Mini SDK Reference](.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md) - Speaker API
