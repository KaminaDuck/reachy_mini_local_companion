---
title: "Pollen Robotics Reference Index"
description: "Reference documentation for Pollen Robotics platforms and tools"
type: "meta"
tags: ["index", "robotics", "pollen-robotics", "reachy-mini", "humanoid"]
category: "robotics"
subcategory: "pollen-robotics"
version: "1.0"
last_updated: "2025-12-28"
status: "stable"
sources:
  - name: "Pollen Robotics Website"
    url: "https://www.pollen-robotics.com/"
  - name: "Pollen Robotics GitHub"
    url: "https://github.com/pollen-robotics"
related: []
author: "unknown"
contributors: []
---

# Pollen Robotics Reference Index

Reference documentation for Pollen Robotics open-source robotics platforms, focusing on the Reachy Mini humanoid robot.

## Documentation Files

### [Reachy Mini Platform Overview](reachy-mini-overview.md)
Comprehensive guide to the Reachy Mini platform including hardware variants, system architecture, deployment topologies, installation, and application framework.

### [Reachy Mini SDK Reference](reachy-mini-sdk.md)
Python SDK API reference covering initialization, movement control, state access, motor management, recording/playback, and media handling.

### [Hey Reachy Wake Word Detection](hey-reachy-wake-word.md)
Custom wake word detection integration using Edge Impulse ML models. Responds to "Hey Reachy" voice command with robot animations and audio greetings.

## Platform Overview

Reachy Mini is an open-source expressive humanoid robot designed for AI developers. Key features:

- **Hardware Variants**: Wireless (autonomous), Lite (USB tethered), Simulation (MuJoCo)
- **Architecture**: Client-server with Zenoh pub/sub and FastAPI REST
- **Control**: 50Hz control loop with multiple kinematics engines
- **SDK**: Python with high-level movement and media APIs
- **Apps**: Distributed via HuggingFace Spaces

## Quick Start

```python
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

with ReachyMini() as mini:
    mini.enable_motors()
    mini.goto_target(
        head=create_head_pose(z=10, roll=15, degrees=True, mm=True),
        duration=1.0
    )
```

## External Resources

- [Reachy Mini GitHub](https://github.com/pollen-robotics/reachy_mini)
- [Pollen Robotics HuggingFace](https://huggingface.co/pollen-robotics)
- [DeepWiki Documentation](https://deepwiki.com/pollen-robotics/reachy_mini/)
- [Pollen Robotics Website](https://www.pollen-robotics.com/)
