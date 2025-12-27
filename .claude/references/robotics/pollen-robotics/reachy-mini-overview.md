---
title: "Reachy Mini Platform Overview"
description: "Open-source expressive humanoid robot platform for AI developers"
type: "framework-guide"
tags: ["robotics", "humanoid", "python", "mujoco", "raspberry-pi", "open-source", "pollen-robotics", "ai-robotics"]
category: "robotics"
subcategory: "pollen-robotics"
version: "1.0"
last_updated: "2025-12-26"
status: "stable"
sources:
  - name: "Reachy Mini GitHub Repository"
    url: "https://github.com/pollen-robotics/reachy_mini"
  - name: "Reachy Mini DeepWiki Documentation"
    url: "https://deepwiki.com/pollen-robotics/reachy_mini/"
  - name: "Pollen Robotics HuggingFace Spaces"
    url: "https://huggingface.co/pollen-robotics/spaces"
related:
  - robotics/pollen-robotics/reachy-mini-sdk.md
author: "unknown"
contributors: []
---

# Reachy Mini Platform Overview

Reachy Mini is an open-source, expressive humanoid robot platform designed for AI developers and robotics enthusiasts. The project provides physical hardware kits and software SDKs enabling users to build, program, and deploy robotic applications. ([GitHub][1])

## Hardware Variants

### Reachy Mini (Wireless)

The fully autonomous variant features: ([GitHub][1])

- Onboard Raspberry Pi 4 for standalone operation
- Battery-powered with WiFi connectivity
- IMU (Inertial Measurement Unit) for spatial awareness
- 2-3 hour assembly time from kit format
- Suitable for standalone deployment

### Reachy Mini Lite

Developer-focused variant designed for experimentation: ([GitHub][1])

- Connects via USB to a computer for control
- Powered through wall outlet (7V-5A supply)
- Ideal for prototyping and learning
- Lower cost entry point

### Simulation

Virtual version running in MuJoCo physics engine: ([DeepWiki][2])

- Requires no hardware
- Full physics simulation at 500Hz
- Enables algorithm development and testing before physical deployment
- Start with `reachy-mini-daemon --sim`

## System Architecture

Reachy Mini implements a **client-server architecture** separating user-facing control from hardware abstraction. ([DeepWiki][2])

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   SDK Layer     │────▶│  Daemon Layer   │────▶│ Backend Layer   │
│  (ReachyMini)   │     │   (FastAPI)     │     │ (Robot/MuJoCo)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │    Zenoh (50Hz)       │    Serial/MuJoCo     │
        │◀──────────────────────│◀──────────────────────│
```

### Core Components

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| **SDK** | `ReachyMini` class | High-level Python APIs for control |
| **Daemon** | FastAPI server | Hardware communication, REST/Zenoh APIs |
| **Backend** | `RobotBackend` / `MujocoBackend` | Hardware abstraction, 50Hz control loop |

### Communication Protocols

**Dual-channel design:** ([DeepWiki][2])

| Protocol | Purpose | Frequency | Use Case |
|----------|---------|-----------|----------|
| **Zenoh** | Real-time commands/state | 50Hz | Motion control, immediate feedback |
| **FastAPI REST** | Daemon lifecycle | Request/response | Service management, app operations |
| **WebSocket** | Media streaming | 25Hz video, 20Hz audio | Camera/audio transport |

**Zenoh Topics:**
- `{prefix}/command` - Motion commands
- `{prefix}/joint_positions` - Current joint angles
- `{prefix}/head_pose` - Head position/orientation
- `{prefix}/task` - Task commands
- `{prefix}/task_progress` - Task status updates

## Hardware Specifications

### Robot Hardware (Physical Variants)

| Component | Specification |
|-----------|---------------|
| **Head** | 6-DOF Stewart platform using XL330-M288 Dynamixel motors |
| **Body** | Yaw rotation motor (1-DOF) |
| **Antennas** | 2 independent antenna motors |
| **Camera** | Arducam camera module |
| **Microphone** | ReSpeaker microphone array |

### Motor Control

- **Frequency**: 50Hz control rate (20ms cycles) ([DeepWiki][2])
- **Interface**: Serial communication via USB
- **Motors**: Dynamixel XL330-M288 series
- **Modes**: Enabled (position control), Disabled (limp), GravityCompensation (compliant)

## Deployment Topologies

### Wireless (Autonomous)

```python
from reachy_mini import ReachyMini

# Connect to wireless robot via mDNS
with ReachyMini(localhost_only=False) as mini:
    mini.goto_target(antennas=[0.5, -0.5], duration=1.0)
```

| Property | Value |
|----------|-------|
| Daemon Location | Embedded Raspberry Pi 4 |
| Connection | WiFi via mDNS (`reachy-mini.local`) |
| SDK Initialization | `ReachyMini(localhost_only=False)` |
| Media | WebRTC streaming with GStreamer |
| Power | Internal battery (2-3 hours) |

### Lite (USB Tethered)

```python
from reachy_mini import ReachyMini

# Default localhost connection
with ReachyMini() as mini:
    mini.goto_target(antennas=[0.5, -0.5], duration=1.0)
```

| Property | Value |
|----------|-------|
| Daemon Location | Host computer |
| Connection | USB serial (`/dev/ttyUSB*` or `COM*`) |
| SDK Initialization | `ReachyMini()` (default) |
| Media | OpenCV/GStreamer |
| Power | 7V-5A wall supply |

### Simulation (MuJoCo)

```bash
# Start simulation daemon
reachy-mini-daemon --sim --scene minimal
```

| Property | Value |
|----------|-------|
| Daemon Location | Host computer |
| Connection | localhost physics engine |
| SDK Initialization | `ReachyMini()` |
| Physics | MuJoCo (500Hz sim, 50Hz control) |
| Media | `no_media` backend |

## Kinematics Engines

Three engines available via `--kinematics-engine` flag: ([DeepWiki][2])

| Engine | Implementation | Performance | Use Case |
|--------|----------------|-------------|----------|
| **AnalyticalKinematics** | Rust FFI | Fast closed-form | Production (default) |
| **PlacoKinematics** | C++ wrapper | Iterative with gravity comp | Advanced control |
| **NNKinematics** | ONNX runtime | Approximate | Experimental |

## Media Backends

| Backend | Video Source | Audio Source | Latency | Use Case |
|---------|--------------|--------------|---------|----------|
| **default** | OpenCV VideoCapture | sounddevice | 100-200ms | USB development |
| **gstreamer** | GStreamer pipelines | GStreamer | 30-50ms | Hardware acceleration |
| **webrtc** | GstWebRTC signaling | GstWebRTC | 50-100ms | Wireless streaming |
| **no_media** | Disabled | Disabled | N/A | Control-only mode |

## Installation

### System Requirements

- **Python**: 3.10, 3.11, or 3.12
- **Git**: With Git LFS for large files
- **Package Manager**: `uv` recommended (10-100x faster than pip)

**Platform-specific:**

| Platform | Additional Requirements |
|----------|------------------------|
| Linux | `libportaudio2`, udev rules for serial access |
| macOS | Homebrew for toolchain |
| Windows | PowerShell execution policy for local scripts |

### PyPI Installation

```bash
# Basic SDK + daemon
uv add reachy-mini

# With simulation support
uv add reachy-mini[mujoco]
```

### Source Installation

```bash
git clone https://github.com/pollen-robotics/reachy_mini
cd reachy_mini
uv sync --extra mujoco
```

### Linux Serial Port Configuration

Add udev rules for USB device access: ([DeepWiki][2])

```bash
# USB Device IDs
# CH340 converter: 1a86:55d3
# Dynamixel adapter: 38fb:1001

# Add user to dialout group
sudo usermod -aG dialout $USER
```

## CLI Entry Points

| Command | Purpose |
|---------|---------|
| `reachy-mini-daemon` | Start server process |
| `reachy-mini-make-app` | Create new application templates |
| `reachy-mini-reflash-motors` | Update motor firmware |

### Daemon Startup Options

```bash
reachy-mini-daemon [OPTIONS]

Options:
  --sim                   Use MuJoCo simulation backend
  --wireless-version      Optimize for embedded deployment
  --stream                Enable WebRTC media streaming
  --autostart             Start backend immediately
  --kinematics-engine     Select IK/FK implementation
  --serialport            Specify USB device path
  --scene                 Choose simulation environment
```

## Application Framework

Apps subclass `ReachyMiniApp` and define entry points in `pyproject.toml`: ([DeepWiki][2])

```toml
[project.entry-points.reachy_mini_apps]
my_app = "my_app.main:main"
```

### Creating Applications

```bash
# Generate new app project
reachy-mini-make-app my_app
```

### Distribution via HuggingFace

Apps are distributed through HuggingFace Spaces: ([HuggingFace][3])

1. Create app locally using `reachy-mini-make-app`
2. Push code to HuggingFace Spaces repository
3. Install via daemon's REST API: `POST /api/apps/install`

### Built-in Applications

| App | Description |
|-----|-------------|
| **Conversation App** | Natural language interaction with LLMs |
| **Hand Tracker V2** | Computer vision hand tracking with mirrored responses |
| **Reachy Mini Radio** | Interactive radio listening |
| **Red Light Green Light** | Game demonstrating AI/vision |
| **Greetings App** | Gesture-based greeting system |

## Best Practices

1. **Always use context managers** (`with` statement) for automatic cleanup
2. **Set appropriate timeouts** for wireless connections (default 5 seconds)
3. **Verify dashboard** at `localhost:8000` before SDK initialization
4. **Use simulation mode** (`--sim`) for development without hardware
5. **Combine movements** in single `goto_target()` calls for synchronization
6. **Enable motors explicitly** before motion commands

## Licensing

- **Code**: Apache 2.0 license ([GitHub][1])
- **Hardware Designs**: Creative Commons BY-SA-NC

## Links

**External Resources:**
- [GitHub Repository](https://github.com/pollen-robotics/reachy_mini)
- [HuggingFace Spaces](https://huggingface.co/pollen-robotics)
- [Pollen Robotics Website](https://www.pollen-robotics.com/)
- [DeepWiki Documentation](https://deepwiki.com/pollen-robotics/reachy_mini/)

---

[1]: https://github.com/pollen-robotics/reachy_mini "Reachy Mini GitHub Repository"
[2]: https://deepwiki.com/pollen-robotics/reachy_mini/ "Reachy Mini DeepWiki Documentation"
[3]: https://huggingface.co/pollen-robotics/spaces "Pollen Robotics HuggingFace Spaces"
