---
title: "Hey Reachy Wake Word Detection"
description: "Custom wake word detection for Reachy Mini using Edge Impulse ML models"
type: "integration-guide"
tags:
  - wake-word
  - edge-impulse
  - audio
  - speech-recognition
  - reachy-mini
  - mfcc
  - machine-learning
  - keyword-spotting
category: "robotics"
subcategory: "reachy-mini"
version: "0.1.0"
last_updated: "2025-12-28"
status: "stable"
sources:
  - name: "HuggingFace Space Repository"
    url: "https://huggingface.co/spaces/luisomoreau/hey_reachy_wake_word_detection"
  - name: "Edge Impulse Public Project"
    url: "https://studio.edgeimpulse.com/public/855375/latest"
  - name: "Edge Impulse Keyword Spotting Tutorial"
    url: "https://docs.edgeimpulse.com/tutorials/end-to-end/keyword-spotting"
related:
  - robotics/pollen-robotics/reachy-mini-overview.md
  - robotics/pollen-robotics/reachy-mini-sdk.md
author: "luisomoreau"
contributors: []
---

# Hey Reachy Wake Word Detection

A custom wake word detection application for Reachy Mini that responds to the "Hey Reachy" voice command using Edge Impulse ML models. When the wake word is detected, the robot performs a friendly animation and responds with a greeting sound. ([HuggingFace Space][1])

## Overview

This project provides on-device wake word detection using an Edge Impulse model trained on synthetic voice data. The system is designed as a base project for modification and experimentation. ([HuggingFace Space][1])

**Key Characteristics:**
- On-device inference (no cloud required)
- ~2.5 hours of synthetic training data
- 98.2% validation accuracy, 97.2% test accuracy ([Edge Impulse Project][2])
- Cross-platform support (macOS ARM64/x86_64, Linux aarch64/armv7l/x86_64)

## Technical Architecture

### Dataset Generation

The training dataset was generated using:
- **Kyutai TTS 1.6** for synthetic voice generation ([HuggingFace Space][1])
- **Freesound LAION 640k dataset** for background noise augmentation
- Dataset generation tooling: [example-synthetic-keywords-using-kyutai-tts-1.6b-en_fr](https://github.com/edgeimpulse/example-synthetic-keywords-using-kyutai-tts-1.6b-en_fr)

### Model Training

The model was trained on Edge Impulse with the following specifications ([Edge Impulse Project][2]):

| Property | Value |
|----------|-------|
| Total Samples | 6,752 |
| Training Data | 3 hours, 2 minutes |
| Sampling Rate | 24 kHz |
| Classification Labels | `hey_reachy`, `noise`, `other` |
| Validation Accuracy | 98.2% |
| Test Accuracy | 97.2% |

**Impulse Pipeline:**
1. **Signal Processing:** MFCC (Mel-Frequency Cepstral Coefficients) - extracts frequency patterns common in human speech ([Edge Impulse Tutorial][3])
2. **Classification:** Keras neural network classifier

### Model Deployment

Edge Impulse models are exported as `.eim` files (Edge Impulse Model) which are platform-specific executables. The application automatically selects the appropriate model based on the detected OS and architecture. ([HuggingFace Space][1])

**Supported Platforms:**
```
darwin/arm64    → hey-reachy-wake-word-detection-mac-arm64.eim
darwin/x86_64   → hey-reachy-wake-word-detection-mac-x86_64.eim
linux/aarch64   → hey-reachy-wake-word-detection-linux-aarch64.eim
linux/armv7l    → hey-reachy-wake-word-detection-linux-armv7.eim
linux/x86_64    → hey-reachy-wake-word-detection-linux-x86_64.eim
```

## Implementation

### Dependencies

```toml
# pyproject.toml
dependencies = [
    "edge-impulse-linux>=1.2.1",
    "numpy>=2.2.6",
    "pyaudio>=0.2.14",
    "reachy-mini",
    "six>=1.17.0",
]
```

Note: The implementation uses `sounddevice` for audio input rather than `pyaudio` due to issues with `mini.media.get_audio_sample()`. ([HuggingFace Space][1])

### Core Components

#### Data Models

```python
from pydantic import BaseModel

class WakeWordSettings(BaseModel):
    threshold: float = 0.7
    device_id: int | None = None

class DetectionStatus(BaseModel):
    last_detection: str | None = None
    detection_count: int = 0
    is_detecting: bool = False
```

#### Main Application Class

The application extends `ReachyMiniApp` and provides:
- REST API endpoints for configuration
- Audio device management
- Multi-threaded classifier execution
- Robot interaction on detection

```python
class HeyReachyWakeWordDetection(ReachyMiniApp):
    custom_app_url: str | None = "http://0.0.0.0:8042"
    request_media_backend: str | None = None

    def __init__(self):
        super().__init__()
        self.runner = None
        self.settings = WakeWordSettings()
        self.detection_status = DetectionStatus()
        # ... threading management
```

#### Classification Loop

The classifier runs in a separate daemon thread to avoid blocking the main application:

```python
for res, audio in runner.classifier(device_id=device_id):
    if stop_event.is_set():
        break

    if "classification" in res["result"]:
        score = res['result']['classification'].get("hey_reachy", 0)
        if score > self.settings.threshold:
            # Trigger robot greeting
            self.greet(reachy_mini)
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/audio_devices` | GET | List available audio input devices |
| `/settings` | GET | Get current threshold and device settings |
| `/settings` | POST | Update settings (triggers classifier restart) |
| `/detection_status` | GET | Get detection count and last detection time |

### Robot Response

When the wake word is detected, the robot:
1. Moves head (z=20mm, roll=10 degrees)
2. Wiggles antennas alternately
3. Plays a random greeting sound from `greetings-audio/` directory
4. Returns to neutral position

Greeting audio files were generated using [Gradium](https://gradium.ai/) for Reachy's voice. ([HuggingFace Space][1])

## Setup

### Prerequisites

- Python 3.10+
- Reachy Mini robot (or simulator)
- Microphone/audio input device

### Installation

```bash
# Clone repository
git clone git@hf.co:spaces/luisomoreau/hey_reachy_wake_word_detection
cd hey_reachy_wake_word_detection

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Start Reachy Mini daemon (in separate terminal)
reachy-mini-daemon

# Run application
python hey_reachy_wake_word_detection/main.py
```

### Entry Point Registration

The application registers as a Reachy Mini app via setuptools entry points:

```toml
[project.entry-points."reachy_mini_apps"]
hey_reachy_wake_word_detection = "hey_reachy_wake_word_detection.main:HeyReachyWakeWordDetection"
```

## Creating Custom Keywords

### Step 1: Train on Edge Impulse

1. Follow the [Edge Impulse Keyword Spotting Tutorial][3]
2. Collect/generate 10+ minutes of keyword audio samples
3. Include "noise" and "unknown/other" classes for robustness
4. Use MFCC feature extraction with Classification (Keras) learning block
5. Set minimum confidence rating to 0.6

### Step 2: Export Model

1. Go to "Deployment" section in Edge Impulse Studio
2. Select target platform (Linux or macOS, with architecture)
3. Download `.eim` model file
4. Place in `models/` directory with naming convention:
   - `your-keyword-mac-arm64.eim`
   - `your-keyword-linux-x86_64.eim`
   - etc.

### Step 3: Update Configuration

Modify `model_mapping` in `main.py`:

```python
model_mapping = {
    ('darwin', 'arm64'): "your-keyword-mac-arm64.eim",
    ('darwin', 'x86_64'): "your-keyword-mac-x86_64.eim",
    ('linux', 'aarch64'): "your-keyword-linux-aarch64.eim",
    ('linux', 'armv7l'): "your-keyword-linux-armv7.eim",
    ('linux', 'x86_64'): "your-keyword-linux-x86_64.eim"
}
```

Update the classification label:

```python
score = res['result']['classification'].get("your_keyword", 0)
```

## Troubleshooting

### Audio Device Issues

The implementation switched from `mini.media.get_audio_sample()` to `sounddevice` library due to compatibility issues. ([HuggingFace Space][1])

To check available audio devices:
```python
import sounddevice as sd
for i, device in enumerate(sd.query_devices()):
    if device['max_input_channels'] > 0:
        print(f"ID {i}: {device['name']}")
```

### Multi-threading Issues

The Edge Impulse Python SDK classifier function has multi-threading constraints. The implementation uses a separate daemon thread with proper stop event handling to manage this. ([HuggingFace Space][1])

### Model Permission Errors

The `.eim` model files must be executable. The application automatically sets executable permissions on first load:

```python
os.chmod(model_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
```

## Performance Considerations

- **Detection Threshold:** Default 0.7 (adjustable via API). Lower values increase sensitivity but may cause false positives.
- **Classification Rate:** Results logged every 1 second to reduce console spam
- **Detection Cooldown:** 2-second visual feedback period after each detection
- **On-device Performance:** 6ms latency, 65.6KB flash on Arduino UNO Q ([Edge Impulse Project][2])

## Limitations

- Not intended to match commercial wake word systems (Alexa, OK Google)
- Model trained on synthetic data (~2.5h) - real voice data would improve accuracy
- Windows is not supported
- Requires Reachy Mini daemon running

## References

[1]: https://huggingface.co/spaces/luisomoreau/hey_reachy_wake_word_detection "HuggingFace Space Repository"
[2]: https://studio.edgeimpulse.com/public/855375/latest "Edge Impulse Public Project"
[3]: https://docs.edgeimpulse.com/tutorials/end-to-end/keyword-spotting "Edge Impulse Keyword Spotting Tutorial"
