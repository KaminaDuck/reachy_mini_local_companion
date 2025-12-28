---
title: "Reachy Mini SDK Reference"
description: "Python SDK API reference for controlling Reachy Mini robots"
type: "api-reference"
tags: ["robotics", "python", "sdk", "api", "motion-control", "pollen-robotics", "reachy-mini"]
category: "robotics"
subcategory: "pollen-robotics"
version: "1.0"
last_updated: "2025-12-26"
status: "stable"
sources:
  - name: "Reachy Mini GitHub Repository"
    url: "https://github.com/pollen-robotics/reachy_mini"
  - name: "Reachy Mini SDK Usage - DeepWiki"
    url: "https://deepwiki.com/pollen-robotics/reachy_mini/2-sdk-usage"
related:
  - robotics/pollen-robotics/reachy-mini-overview.md
  - robotics/pollen-robotics/hey-reachy-wake-word.md
author: "unknown"
contributors: []
---

# Reachy Mini SDK Reference

The `reachy_mini` Python SDK provides high-level APIs for controlling Reachy Mini robots. This reference covers initialization, movement control, state access, motor management, and media handling. ([GitHub][1])

## Installation

```bash
# Basic installation
uv add reachy-mini

# With MuJoCo simulation support
uv add reachy-mini[mujoco]

# From source
git clone https://github.com/pollen-robotics/reachy_mini
cd reachy_mini && uv sync --extra mujoco
```

## Initialization

### Basic Connection

```python
from reachy_mini import ReachyMini

# Context manager (recommended)
with ReachyMini() as mini:
    # Robot automatically connected and cleaned up
    pass
```

### Connection Parameters

```python
ReachyMini(
    localhost_only=True,      # False for wireless robots via mDNS
    robot_name="reachy_mini", # Zenoh topic prefix for multi-robot
    media_backend="default",  # "gstreamer", "webrtc", or "no_media"
    timeout=5.0               # Connection timeout in seconds
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `localhost_only` | `True` | Set `False` for wireless robots connecting via mDNS |
| `robot_name` | `"reachy_mini"` | Zenoh topic prefix, useful for multi-robot setups |
| `media_backend` | `"default"` | Media backend: `"default"`, `"gstreamer"`, `"webrtc"`, `"no_media"` |
| `timeout` | `5.0` | Connection establishment timeout in seconds |

### Deployment-Specific Initialization

```python
# Wireless robot (mDNS discovery)
with ReachyMini(localhost_only=False) as mini:
    pass

# Lite/Simulation (localhost)
with ReachyMini() as mini:
    pass

# No media (control-only)
with ReachyMini(media_backend="no_media") as mini:
    pass
```

## Movement Control

### goto_target() - Interpolated Movement

The primary motion interface providing smooth interpolated movements: ([DeepWiki][2])

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini() as mini:
    mini.goto_target(
        head=create_head_pose(z=10, mm=True),
        antennas=[0.5, -0.5],
        body_yaw=0.3,
        duration=2.0
    )
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `head` | 4x4 matrix | Transformation matrix from `create_head_pose()` |
| `antennas` | `[float, float]` | Right and left antenna angles in radians |
| `body_yaw` | `float` | Body rotation in radians |
| `duration` | `float` | Movement time in seconds |

### create_head_pose() - Pose Construction

Build transformation matrices for head positioning: ([DeepWiki][2])

```python
from reachy_mini.utils import create_head_pose

pose = create_head_pose(
    x=0, y=0, z=10,           # Translation
    roll=0, pitch=0, yaw=15,  # Rotation
    mm=True,                  # Use millimeters for position
    degrees=True              # Use degrees for angles
)
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `x`, `y`, `z` | `0` | Translation (meters by default, mm if `mm=True`) |
| `roll`, `pitch`, `yaw` | `0` | Rotation (radians by default, degrees if `degrees=True`) |
| `mm` | `False` | Interpret position values as millimeters |
| `degrees` | `False` | Interpret angle values as degrees |

### set_target() - Immediate Positioning

For instant (non-interpolated) positioning: ([DeepWiki][2])

```python
# Set antenna positions immediately
mini.set_target(antennas=[0.0, 0.0])
```

### look_at_world() - Gaze Direction

Direct the robot's head to look at a world-space point:

```python
# Look at a point in 3D space
mini.look_at_world(x=0.5, y=0.0, z=0.3)
```

### Movement Examples

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini() as mini:
    # Enable motors first
    mini.enable_motors()

    # Nod head up and down
    mini.goto_target(
        head=create_head_pose(pitch=15, degrees=True),
        duration=0.5
    )
    mini.goto_target(
        head=create_head_pose(pitch=-15, degrees=True),
        duration=0.5
    )

    # Wiggle antennas
    for _ in range(3):
        mini.goto_target(antennas=[0.5, -0.5], duration=0.3)
        mini.goto_target(antennas=[-0.5, 0.5], duration=0.3)

    # Return to neutral
    mini.goto_target(
        head=create_head_pose(),
        antennas=[0.0, 0.0],
        body_yaw=0.0,
        duration=1.0
    )
```

## State Access

### Current Pose

```python
# Get current head pose
current_pose = mini.head_pose
# Returns: HeadPose(x, y, z, roll, pitch, yaw)

print(f"Position: ({current_pose.x}, {current_pose.y}, {current_pose.z})")
print(f"Rotation: ({current_pose.roll}, {current_pose.pitch}, {current_pose.yaw})")
```

### Joint Positions

```python
# Get current joint angles
joint_positions = mini.current_joint_positions
# Returns dict of joint names to angles in radians
```

### Robot State

```python
# Get overall robot state
state = mini.state
# Returns: READY, MOVING, ERROR, etc.

# Check if robot is ready
if state == "READY":
    mini.goto_target(...)
```

## Motor Control

### Enable/Disable Motors

Motors must be enabled before motion commands: ([DeepWiki][2])

```python
# Enable motors for position control
mini.enable_motors()

# Disable motors (become limp)
mini.disable_motors()
```

### Gravity Compensation

Compliant mode for manual manipulation: ([DeepWiki][2])

```python
# Enable gravity compensation (compliant mode)
mini.enable_gravity_compensation()

# Disable gravity compensation
mini.disable_gravity_compensation()
```

**Motor Modes:**

| Mode | Behavior |
|------|----------|
| **Enabled** | Position control with stiffness |
| **Disabled** | Limp (motor power off) |
| **GravityCompensation** | Compliant torque-controlled mode |

## Recording and Playback

### Capture Motion

Record robot movements for later replay: ([DeepWiki][2])

```python
# Start recording
mini.start_recording()

# Perform movements (manual or programmatic)
mini.goto_target(antennas=[0.5, 0.0], duration=1.0)
mini.goto_target(antennas=[-0.5, 0.0], duration=1.0)

# Stop and get recording
recording = mini.stop_recording()

# Access recorded data
positions = recording.positions  # Joint positions over time
timestamps = recording.timestamps  # Corresponding timestamps
```

### Replay Recorded Motion

```python
# Replay at normal speed
mini.replay(recording, speed=1.0)

# Replay at half speed
mini.replay(recording, speed=0.5)

# Replay at double speed
mini.replay(recording, speed=2.0)
```

## Media Access

### Video (Camera)

Access the robot's camera feed: ([DeepWiki][2])

```python
# Get single frame
frame = mini.camera.get_frame()
# Returns: numpy array (H, W, 3) in BGR format

# Use with OpenCV
import cv2
cv2.imshow("Reachy Mini Camera", frame)
cv2.waitKey(1)
```

### Audio (Microphone/Speaker)

```python
# Get audio chunk from microphone
audio_data = mini.microphone.get_audio_chunk()

# Play audio through speaker
mini.speaker.play(audio_buffer)
```

## Error Handling

```python
from reachy_mini import ReachyMini

try:
    with ReachyMini(timeout=10.0) as mini:
        mini.enable_motors()
        mini.goto_target(antennas=[0.5, 0.0], duration=1.0)

except ConnectionError as e:
    print(f"Failed to connect to daemon: {e}")

except TimeoutError as e:
    print(f"Connection timed out: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Complete Example

```python
"""Complete Reachy Mini control example."""
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time

def main():
    # Connect to robot (wireless)
    with ReachyMini(localhost_only=False, timeout=10.0) as mini:
        print(f"Connected! State: {mini.state}")

        # Enable motors
        mini.enable_motors()
        print("Motors enabled")

        # Greeting animation
        print("Starting greeting animation...")

        # Look up and wiggle antennas
        mini.goto_target(
            head=create_head_pose(pitch=10, degrees=True),
            antennas=[0.3, -0.3],
            duration=0.5
        )

        # Nod sequence
        for _ in range(2):
            mini.goto_target(
                head=create_head_pose(pitch=15, degrees=True),
                duration=0.3
            )
            mini.goto_target(
                head=create_head_pose(pitch=5, degrees=True),
                duration=0.3
            )

        # Return to neutral
        mini.goto_target(
            head=create_head_pose(),
            antennas=[0.0, 0.0],
            body_yaw=0.0,
            duration=1.0
        )

        print("Animation complete!")

        # Get camera frame
        frame = mini.camera.get_frame()
        print(f"Camera frame shape: {frame.shape}")

        # Disable motors before exit
        mini.disable_motors()
        print("Motors disabled")

if __name__ == "__main__":
    main()
```

## API Quick Reference

### ReachyMini Class

| Method | Description |
|--------|-------------|
| `goto_target(head, antennas, body_yaw, duration)` | Smooth interpolated movement |
| `set_target(antennas)` | Immediate positioning |
| `look_at_world(x, y, z)` | Point head at world coordinate |
| `enable_motors()` | Enable position control |
| `disable_motors()` | Make motors limp |
| `enable_gravity_compensation()` | Compliant mode |
| `disable_gravity_compensation()` | Exit compliant mode |
| `start_recording()` | Begin motion capture |
| `stop_recording()` | End capture, return recording |
| `replay(recording, speed)` | Play back recorded motion |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `head_pose` | `HeadPose` | Current head position/orientation |
| `current_joint_positions` | `dict` | Joint name to angle mapping |
| `state` | `str` | Robot state (READY, MOVING, etc.) |
| `camera` | `Camera` | Camera interface |
| `microphone` | `Microphone` | Audio input interface |
| `speaker` | `Speaker` | Audio output interface |

### Utility Functions

| Function | Description |
|----------|-------------|
| `create_head_pose(x, y, z, roll, pitch, yaw, mm, degrees)` | Build 4x4 transformation matrix |

## Links

**External Resources:**
- [GitHub Repository](https://github.com/pollen-robotics/reachy_mini)
- [SDK Usage Documentation](https://deepwiki.com/pollen-robotics/reachy_mini/2-sdk-usage)
- [System Architecture](https://deepwiki.com/pollen-robotics/reachy_mini/1.1-system-architecture)

---

[1]: https://github.com/pollen-robotics/reachy_mini "Reachy Mini GitHub Repository"
[2]: https://deepwiki.com/pollen-robotics/reachy_mini/2-sdk-usage "Reachy Mini SDK Usage Documentation"
