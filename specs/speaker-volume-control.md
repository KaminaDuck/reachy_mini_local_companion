# Feature: Speaker Volume Control

## Implementation Status: COMPLETED

**Date Completed:** 2025-12-26

### Resolution Summary

Successfully implemented software-based speaker volume control for the Reachy Mini Local Companion app.

#### Phase 1 (Foundation): Completed
- Added `volume: int = 80` field to `TTSConfig` in models.py
- Volume is included in `/tts/status` API response

#### Phase 2 (Core Implementation): Completed
- Implemented `scale_audio_volume()` function in engine.py for WAV sample scaling
- Updated `synthesize()` and `speak()` methods to accept volume parameter
- Volume 0% skips playback entirely for efficiency
- Volume 100% returns original audio without processing

#### Phase 3 (Integration): Completed
- Added `volume` field to `TTSConfigRequest` with clamping (0-100)
- Updated all TTS endpoints (`/tts/speak`, `/tts/preview`, auto-speak) to use volume
- Added volume slider to web UI with real-time percentage display
- Debounced API calls while dragging slider

### Files Changed

| File | Lines Changed | Purpose |
|------|---------------|---------|
| tts/models.py | +1 | Added `volume: int = 80` field |
| tts/engine.py | +67 | Added `scale_audio_volume()`, updated methods |
| main.py | +10 | Volume in config, status, and speak endpoints |
| static/index.html | +6 | Volume slider HTML |
| static/main.js | +22 | Volume slider logic with debouncing |
| static/style.css | +13 | Volume slider styling |

**Total: 6 files changed, 125 insertions(+), 8 deletions(-)**

### Changes from Original Plan

None - implementation followed the spec exactly.

---

## Feature Description

Add software-based volume control for the Reachy Mini speaker output. Since the Reachy Mini SDK's `speaker.play()` API does not expose hardware volume control, this feature implements volume adjustment by scaling audio samples before playback. Users can adjust volume (0-100%) via a slider in the web UI, and the setting persists across sessions. Volume control applies to both TTS speech synthesis and any other audio playback through the speaker.

## User Story

As a **Reachy Mini user**
I want to **adjust the speaker volume of my robot**
So that **I can control how loud the robot speaks based on my environment and preferences**

## Problem Statement

Currently, the Reachy Mini Local Companion app has no way to control the speaker volume. TTS responses and sound effects play at a fixed volume determined by the synthesized audio. Users in quiet environments (offices, bedrooms) may find the robot too loud, while users in noisy environments may need higher volume. There is no volume slider or mute option in the UI. The underlying Reachy Mini SDK's `speaker.play()` API does not expose hardware volume control, requiring a software-based solution.

## Solution Statement

Implement software-based volume control by:

1. **Audio Scaling**: Multiply audio samples by a volume factor (0.0-1.0) before playback
2. **Volume Configuration**: Add a `volume` setting (0-100%) to the TTS configuration model
3. **Volume Persistence**: Store volume setting in `TTSConfig` and expose via API
4. **UI Integration**: Add a volume slider to the TTS section of the web control panel
5. **Mute Functionality**: Volume at 0% effectively mutes the speaker
6. **Real-time Preview**: Changing volume takes effect immediately for next playback

## Relevant Files

Use these files to implement the feature:

- [reachy_mini_local_companion/tts/engine.py](reachy_mini_local_companion/tts/engine.py) - TTS engine; add volume scaling to `synthesize()` method
- [reachy_mini_local_companion/tts/models.py](reachy_mini_local_companion/tts/models.py) - TTS models; add `volume` field to `TTSConfig`
- [reachy_mini_local_companion/main.py](reachy_mini_local_companion/main.py) - Main app; update TTS config endpoints and add volume to status
- [reachy_mini_local_companion/static/index.html](reachy_mini_local_companion/static/index.html) - Web UI; add volume slider control
- [reachy_mini_local_companion/static/main.js](reachy_mini_local_companion/static/main.js) - Frontend JS; add volume slider logic
- [reachy_mini_local_companion/static/style.css](reachy_mini_local_companion/static/style.css) - Styles; add volume slider styling
- [.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md](.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md) - SDK reference for speaker API

### New Files

None required. All changes are modifications to existing files.

## Implementation Plan

### Phase 1: Foundation

1. **Add Volume to Data Model**: Extend `TTSConfig` with a `volume` field (integer 0-100, default 80)
2. **Add Volume to Status**: Include current volume in `TTSStatus` response

### Phase 2: Core Implementation

1. **Implement Audio Scaling**: Create a utility function to scale audio samples by volume factor
2. **Integrate Volume into Synthesis**: Apply volume scaling in `PiperTTSEngine.synthesize()` after synthesis, before writing to WAV
3. **Handle Edge Cases**:
   - Volume 0 should produce silence (or skip playback)
   - Clamp values to prevent clipping at high volumes

### Phase 3: Integration

1. **Update API Endpoints**: Add volume to `TTSConfigRequest` and include in status responses
2. **Add Web UI Controls**: Volume slider with percentage display
3. **Real-time Updates**: Volume changes apply to next playback without restart

## Step by Step Tasks

### Step 1: Update TTS Models

- Modify `reachy_mini_local_companion/tts/models.py`:
  - Add `volume: int = 80` field to `TTSConfig` (range 0-100, default 80%)
  - Add validation to ensure volume is within range

### Step 2: Implement Audio Volume Scaling

- Create a helper function in `engine.py`:
  ```python
  def scale_audio_volume(audio_data: bytes, volume: float) -> bytes:
      """Scale WAV audio samples by volume factor (0.0-1.0)."""
  ```
- Read WAV data, extract samples, multiply by volume factor, repack as WAV
- Use numpy for efficient sample manipulation
- Clamp values to prevent int16 overflow

### Step 3: Integrate Volume into TTS Engine

- Modify `PiperTTSEngine.synthesize()`:
  - Accept optional `volume` parameter (float 0.0-1.0)
  - After synthesizing to WAV bytes, apply volume scaling
  - Return scaled audio bytes
- Modify `PiperTTSEngine.speak()`:
  - Accept `volume` parameter and pass to `synthesize()`

### Step 4: Update Main App Endpoints

- Modify `main.py`:
  - Update `TTSConfigRequest` to include `volume: int | None = None`
  - Handle volume updates in `/tts/config` POST endpoint
  - Pass `tts_config.volume / 100.0` to `tts_engine.speak()` calls
  - Include volume in `/tts/status` response

### Step 5: Add Volume Slider to Web UI - HTML

- Modify `static/index.html`:
  - Add volume slider control in TTS section:
    ```html
    <div class="tts-config">
        <label for="volume-slider">Volume:</label>
        <input type="range" id="volume-slider" min="0" max="100" step="5" value="80">
        <span id="volume-value">80%</span>
    </div>
    ```
  - Position after the voice selector and before auto-speak toggle

### Step 6: Add Volume Slider Logic - JavaScript

- Modify `static/main.js`:
  - Add `updateVolume(volume)` function to POST to `/tts/config`
  - Update slider display on input (real-time feedback)
  - Debounce API calls to avoid excessive requests while dragging
  - Initialize slider value from `ttsConfig.volume` on load
  - Update `fetchTTSConfig()` to handle volume

### Step 7: Style Volume Slider - CSS

- Modify `static/style.css`:
  - Style the volume slider to match existing range inputs
  - Add visual feedback for slider position
  - Style the percentage display

### Step 8: Test and Validate

- Run all validation commands
- Test volume at 0%, 50%, 100%
- Verify volume persists across page refreshes
- Test with TTS speak and auto-speak LLM responses
- Verify no audio clipping at 100% volume

## Testing Strategy

### Unit Tests

- **TTSConfig**: Test volume field validation (0-100 range, default value)
- **scale_audio_volume**: Test scaling at 0%, 50%, 100% volumes
- **scale_audio_volume**: Test that output is valid WAV format
- **scale_audio_volume**: Test clipping prevention

### Integration Tests

- **Config Endpoint**: Test volume updates via POST `/tts/config`
- **Status Endpoint**: Verify volume included in GET `/tts/status`
- **Speak Endpoint**: Verify volume is applied during playback

### Edge Cases

- Volume set to 0 (should produce silence or skip playback)
- Volume set to 100 (should not clip or distort)
- Volume set to values outside range (should clamp to 0-100)
- Rapid volume changes while speaking (should not crash)
- Volume applied to empty text (handle gracefully)
- Volume persistence after app restart

## Acceptance Criteria

- [ ] Volume slider (0-100%) appears in TTS section of web UI
- [ ] Moving the slider updates the volume percentage display in real-time
- [ ] Volume changes take effect on the next TTS playback
- [ ] Volume setting persists when refreshing the page
- [ ] Volume at 0% produces silence or skips playback
- [ ] Volume at 100% plays at original synthesized level without distortion
- [ ] Volume is applied to both manual "Speak" and auto-speak LLM responses
- [ ] Volume is included in `/tts/status` API response
- [ ] All existing TTS functionality continues to work
- [ ] No audio clipping or distortion at any volume level

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd /Users/duck/Projects/reachy_mini_local_companion && uv sync` - Install all dependencies
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -c "from reachy_mini_local_companion.tts.models import TTSConfig; c = TTSConfig(); print(f'Volume default: {c.volume}')"` - Verify TTSConfig has volume field
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -c "from reachy_mini_local_companion.tts import PiperTTSEngine, VoiceManager; print('TTS module OK')"` - Verify TTS module imports
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -m py_compile reachy_mini_local_companion/main.py` - Verify main.py syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run python -m py_compile reachy_mini_local_companion/tts/engine.py` - Verify engine.py syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run ruff check reachy_mini_local_companion/` - Run linting
- `cd /Users/duck/Projects/reachy_mini_local_companion && uv run mypy reachy_mini_local_companion/ --ignore-missing-imports` - Run type checking

## Notes

### Technical Approach: Software Volume Control

Since the Reachy Mini SDK's `speaker.play()` API does not expose hardware volume control, we implement software-based volume adjustment:

1. **Audio Sample Scaling**: Multiply each 16-bit PCM sample by the volume factor (0.0-1.0)
2. **Clipping Prevention**: Clamp scaled values to int16 range (-32768 to 32767)
3. **WAV Format Preservation**: Read WAV → extract samples → scale → repack as WAV

```python
def scale_audio_volume(wav_bytes: bytes, volume: float) -> bytes:
    """Scale audio samples in a WAV file by volume factor."""
    import io
    import wave
    import numpy as np

    # Read original WAV
    with wave.open(io.BytesIO(wav_bytes), 'rb') as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(params.nframes)

    # Scale samples
    samples = np.frombuffer(frames, dtype=np.int16)
    scaled = np.clip(samples * volume, -32768, 32767).astype(np.int16)

    # Write scaled WAV
    output = io.BytesIO()
    with wave.open(output, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(scaled.tobytes())

    return output.getvalue()
```

### Volume at 0% Behavior

When volume is 0%, there are two options:
1. **Skip playback entirely**: More efficient, no audio processing
2. **Play silence**: Consistent timing with other volume levels

Recommendation: Skip playback entirely when volume is 0% to save processing and playback time.

### Default Volume

Default volume is set to 80% (not 100%) to:
- Provide headroom for users who want louder output
- Reduce the chance of startling users on first use
- Match common defaults in other audio applications

### UI Design

The volume slider follows the pattern already established for STT sensitivity slider:
```html
<div class="tts-config">
    <label for="volume-slider">Volume:</label>
    <input type="range" id="volume-slider" min="0" max="100" step="5" value="80">
    <span id="volume-value">80%</span>
</div>
```

### Future Enhancements

- **Volume presets**: Quick buttons for 25%, 50%, 75%, 100%
- **Mute toggle**: Separate mute button that remembers previous volume
- **Per-voice volume**: Different default volumes for different voices
- **Sound effect volume**: Separate volume control for `reachy_mini.media.play_sound()`
- **Fade effects**: Gradual volume changes for smoother transitions
- **System volume sync**: If hardware volume becomes available in SDK
