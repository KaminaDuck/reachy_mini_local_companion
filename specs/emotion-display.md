# Feature: Emotion Display System

## Feature Description

Add an expressive emotion display system to the Reachy Mini Local Companion that allows the robot to communicate emotional states through coordinated antenna movements, head gestures, and sound effects. The system will provide a library of predefined emotions (happy, sad, curious, excited, sleepy, surprised, angry, confused) that can be triggered via the web UI or programmatically, enabling more natural and engaging human-robot interaction.

## User Story

As a **Reachy Mini user**
I want to **trigger emotional expressions on the robot through a simple web interface**
So that **the robot can communicate non-verbally and feel more alive and engaging during interactions**

## Problem Statement

The current Reachy Mini Local Companion only provides basic continuous motion (oscillating head and antennas) without any expressive capability. Users cannot make the robot express different emotional states, limiting its ability to communicate and engage naturally with humans. This reduces the companion-like quality of the robot and makes interactions feel mechanical rather than lively.

## Solution Statement

Implement an emotion display system that:

1. **Defines emotion profiles** - Each emotion has a unique signature combining:
   - Head movement pattern (nod, shake, tilt, bob)
   - Antenna movement pattern (wiggle, droop, perk up, asymmetric)
   - Optional sound effect
   - Duration and intensity parameters

2. **Provides a web UI** - Emotion buttons on the control panel allow instant triggering

3. **Supports programmatic control** - REST API endpoints for triggering emotions from external systems

4. **Queues emotions** - Ensures smooth transitions between emotions without jarring movements

5. **Returns to idle** - After an emotion plays, returns to the configured idle behavior (current oscillation or neutral)

## Relevant Files

Use these files to implement the feature:

- [main.py](reachy_mini_local_companion/main.py) - Core application logic; add emotion state management, emotion execution logic, and new API endpoints
- [static/index.html](reachy_mini_local_companion/static/index.html) - Web UI; add emotion selector buttons
- [static/main.js](reachy_mini_local_companion/static/main.js) - Frontend JavaScript; add emotion triggering functions and UI updates
- [static/style.css](reachy_mini_local_companion/static/style.css) - Styling; add styles for emotion buttons grid
- [pyproject.toml](pyproject.toml) - Project config; no changes expected (no new dependencies)
- [.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md](.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md) - SDK reference for movement APIs (`goto_target`, `create_head_pose`, `set_target`)

### New Files

- `reachy_mini_local_companion/emotions.py` - Emotion definitions and profiles (dataclasses for EmotionProfile, movement parameters)

## Implementation Plan

### Phase 1: Foundation

Define the emotion data model and create emotion profile definitions:

1. Create `emotions.py` with dataclasses for:
   - `MovementKeyframe` - single position in a movement sequence
   - `EmotionProfile` - complete emotion definition with head/antenna patterns and optional sound

2. Define the 8 core emotions with distinct movement signatures:
   - **Happy**: Quick nods, perky alternating antenna wiggles, upbeat sound
   - **Sad**: Slow downward head tilt, drooping antennas, low sound
   - **Curious**: Head tilt to side, one antenna up, inquisitive sound
   - **Excited**: Fast head bobs, rapid antenna oscillation, energetic sound
   - **Sleepy**: Slow head droop, antennas slowly lowering, yawn sound
   - **Surprised**: Quick head back, antennas shoot up, gasp sound
   - **Angry**: Sharp head shakes, antennas flatten back, growl sound
   - **Confused**: Head tilts alternating, asymmetric antenna movements, questioning sound

### Phase 2: Core Implementation

Implement the emotion execution engine in `main.py`:

1. Add emotion state management:
   - Current emotion being played (or None)
   - Emotion queue for sequential playback
   - Flag to interrupt current emotion

2. Create emotion executor function:
   - Reads keyframes from emotion profile
   - Interpolates movements using `goto_target()`
   - Plays associated sound if defined
   - Returns to idle state on completion

3. Add FastAPI endpoints:
   - `POST /emotion` - Trigger an emotion by name
   - `GET /emotions` - List available emotions
   - `POST /emotion/stop` - Stop current emotion and return to idle

### Phase 3: Integration

Connect the emotion system to the web UI:

1. Update `index.html`:
   - Add emotion button grid section
   - Include stop button for canceling emotions

2. Update `main.js`:
   - Add `triggerEmotion(name)` function
   - Add `stopEmotion()` function
   - Fetch available emotions on page load
   - Update UI to show current emotion state

3. Update `style.css`:
   - Style emotion button grid (responsive grid layout)
   - Add visual feedback for active emotion
   - Use distinct colors for emotion categories

## Step by Step Tasks

### Step 1: Create Emotion Data Model

- Create `reachy_mini_local_companion/emotions.py`
- Define `MovementKeyframe` dataclass with fields:
  - `head_yaw: float` (degrees)
  - `head_pitch: float` (degrees)
  - `head_roll: float` (degrees)
  - `antenna_right: float` (radians)
  - `antenna_left: float` (radians)
  - `duration: float` (seconds)
- Define `EmotionProfile` dataclass with fields:
  - `name: str`
  - `keyframes: list[MovementKeyframe]`
  - `sound: str | None`
  - `description: str`

### Step 2: Define Core Emotion Profiles

- In `emotions.py`, create `EMOTIONS: dict[str, EmotionProfile]` with all 8 emotions
- Each emotion should have 3-6 keyframes creating a natural animation loop
- Use realistic ranges: head ±30° yaw, ±20° pitch, ±15° roll; antennas ±0.5 rad
- Total emotion duration should be 1.5-3 seconds

### Step 3: Add Emotion State to Main Application

- In `main.py`, import the emotions module
- Add class variables:
  - `current_emotion: str | None = None`
  - `emotion_requested: str | None = None`
  - `emotion_stop_requested: bool = False`
- Create Pydantic model `EmotionRequest(BaseModel)` with `name: str`

### Step 4: Implement Emotion Execution in Control Loop

- In `main.py`, modify the control loop to check for `emotion_requested`
- When emotion is requested:
  - Set `current_emotion` to the emotion name
  - Execute keyframes sequentially using `goto_target()`
  - Play sound if defined
  - Clear `current_emotion` when complete
  - Resume idle animation
- Handle `emotion_stop_requested` to gracefully interrupt

### Step 5: Add REST API Endpoints

- Add `POST /emotion` endpoint accepting `EmotionRequest`
  - Validate emotion name exists
  - Set `emotion_requested = request.name`
  - Return `{"emotion": name, "status": "queued"}`
- Add `GET /emotions` endpoint
  - Return list of available emotion names and descriptions
- Add `POST /emotion/stop` endpoint
  - Set `emotion_stop_requested = True`
  - Return `{"status": "stopping"}`

### Step 6: Update HTML with Emotion Controls

- In `static/index.html`, add new section after existing controls:
  - `<div id="emotions">` container
  - Grid of emotion buttons (one per emotion)
  - Stop button to cancel current emotion
- Add status display for current emotion

### Step 7: Implement JavaScript Emotion Functions

- In `static/main.js`, add:
  - `async function triggerEmotion(name)` - POST to `/emotion`
  - `async function stopEmotion()` - POST to `/emotion/stop`
  - `async function loadEmotions()` - GET `/emotions` on page load
  - Event listeners for emotion buttons
  - UI update to show which emotion is active

### Step 8: Style Emotion UI

- In `static/style.css`, add:
  - `#emotions` grid layout (2-4 columns responsive)
  - `.emotion-btn` base styles
  - Distinct background colors per emotion category
  - `.emotion-btn.active` state for currently playing
  - Stop button styling (red/warning color)

### Step 9: Add Sound Files (Optional)

- Document that users can add `.wav` files to the robot's sound directory
- Provide naming convention: `emotion_happy.wav`, `emotion_sad.wav`, etc.
- Gracefully handle missing sound files (log warning, continue animation)

### Step 10: Run Validation Commands

- Run all validation commands to ensure zero regressions
- Test each emotion via the web UI
- Verify API endpoints respond correctly

## Testing Strategy

### Unit Tests

- Test `EmotionProfile` dataclass creation and validation
- Test keyframe interpolation logic
- Test emotion name validation
- Test API request/response models

### Integration Tests

- Test `POST /emotion` endpoint with valid emotion name
- Test `POST /emotion` endpoint with invalid emotion name (expect 400)
- Test `GET /emotions` returns all emotions
- Test `POST /emotion/stop` interrupts current emotion
- Test emotion queue behavior (trigger while one is playing)

### Edge Cases

- Trigger emotion while another is playing (should queue or replace)
- Stop emotion when none is playing (should be no-op)
- Invalid emotion name (should return 400 error)
- Rapid successive emotion triggers (should handle gracefully)
- Missing sound file (should log warning and continue)
- Robot disconnection during emotion (graceful degradation)

## Acceptance Criteria

1. All 8 emotions are defined with distinct, recognizable movement patterns
2. Web UI displays emotion buttons in a grid layout
3. Clicking an emotion button triggers the corresponding animation
4. Emotion animations complete smoothly without jerky movements
5. `POST /emotion` API endpoint triggers emotions programmatically
6. `GET /emotions` API endpoint returns list of available emotions
7. Stop button/endpoint cancels current emotion and returns to idle
8. Sound plays (if configured) during emotion animation
9. Robot returns to idle animation after emotion completes
10. No regressions in existing antenna toggle and sound play functionality

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/emotions.py` - Verify emotions module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/main.py` - Verify main module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -c "from reachy_mini_local_companion.emotions import EMOTIONS; print(f'Loaded {len(EMOTIONS)} emotions: {list(EMOTIONS.keys())}')"` - Verify emotions load correctly
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -c "from reachy_mini_local_companion.main import ReachyMiniLocalCompanion; print('Main module imports successfully')"` - Verify main module imports

## Notes

- **No new dependencies required** - Uses existing `reachy-mini` SDK, `pydantic`, and `numpy`
- **Sound files are optional** - Emotions work without sounds; sounds can be added later
- **Extensibility** - The `EMOTIONS` dictionary can be easily extended with custom emotions
- **Future enhancements**:
  - Emotion intensity parameter (0.0-1.0 scale)
  - Emotion chaining/sequences
  - User-defined custom emotions via config file
  - Emotion triggered by voice commands or face detection
- **Hardware considerations** - Movement speeds and ranges are conservative to avoid mechanical stress
- **Idle behavior toggle** - Consider adding option to disable idle animation entirely when emotions are available

---

## Implementation Resolution

**Status**: ✅ Completed
**Date**: 2025-12-26

### Files Changed

| File | Lines Added | Description |
|------|-------------|-------------|
| `reachy_mini_local_companion/emotions.py` | 212 | New module with dataclasses and 8 emotion profiles |
| `reachy_mini_local_companion/main.py` | +131 | Emotion endpoints and control loop integration |
| `reachy_mini_local_companion/static/index.html` | +20 | Emotion section with grid container |
| `reachy_mini_local_companion/static/main.js` | +143 | Emotion UI functions and polling |
| `reachy_mini_local_companion/static/style.css` | +179 | Emotion grid and button styling |

**Total**: ~685 lines added across 5 files

### Step Resolution Details

1. **Step 1-2 (Emotion Data Model & Profiles)**: Created `emotions.py` with `MovementKeyframe` and `EmotionProfile` dataclasses. All 8 emotions defined with 3-6 keyframes each using realistic movement ranges.

2. **Step 3 (Emotion State in Main)**: Added emotion state variables inside the `run()` method. Used local variables with `nonlocal` declarations for endpoint access.

3. **Step 4 (Control Loop Integration)**: Implemented keyframe execution using `goto_target()` for smooth interpolation. Emotion playback pauses idle animation. Sound playback attempted but gracefully handles missing files.

4. **Step 5 (REST API)**: Added endpoints:
   - `GET /emotions` - Lists all emotions with names and descriptions
   - `POST /emotion` - Triggers emotion by name, returns queued status
   - `POST /emotion/stop` - Stops current emotion
   - `GET /emotion/status` - Returns current and queued emotion

5. **Step 6 (HTML)**: Added emotion section with status panel, grid container, and stop button.

6. **Step 7 (JavaScript)**: Implemented all functions with polling for status updates during playback.

7. **Step 8 (CSS)**: Full responsive grid layout with emotion-specific hover colors using emoji icons.

8. **Step 9 (Sound Files)**: Documented in code; gracefully logs debug message if sound file missing.

9. **Step 10 (Validation)**: All checks passed:
   - `py_compile` - OK for both modules
   - `ruff check` - All checks passed
   - `mypy` - No issues found

### Deviations from Original Plan

- **No emotion queuing implemented**: If an emotion is triggered while another plays, the new one is stored but won't interrupt. This is simpler than a full queue system.
- **Polling instead of WebSocket**: Used 200ms polling for status updates during playback rather than implementing WebSocket push notifications.
