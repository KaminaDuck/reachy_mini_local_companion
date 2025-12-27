# Feature: Vision System with Face and Object Recognition

## Feature Description

Add a comprehensive vision system to the Reachy Mini Local Companion that enables the robot to see and understand its environment through its onboard camera. The system provides facial detection/recognition and object detection capabilities with a pluggable architecture supporting multiple vision model backends (OpenCV Haar Cascades, DeepFace, YOLO/Ultralytics). The vision data streams to a web UI showing the camera feed with detection overlays, and can trigger robot behaviors (looking at detected faces, reacting to objects).

## User Story

As a **Reachy Mini developer**
I want to **have the robot detect and recognize faces and objects in its camera feed**
So that **the robot can respond to people and its environment intelligently, enabling natural human-robot interaction and awareness**

## Problem Statement

The current Reachy Mini Local Companion has no vision processing capabilities. While the SDK provides camera access (`mini.camera.get_frame()`), the application doesn't use it. Users cannot:

1. See what the robot sees through a web interface
2. Have the robot detect or recognize faces
3. Have the robot identify objects in its environment
4. Trigger behaviors based on visual input

This limits the robot to pre-programmed animations without environmental awareness.

## Solution Statement

Implement a modular vision system that:

1. **Captures camera frames** - Continuously reads from the Reachy Mini camera at configurable FPS
2. **Provides pluggable detection backends**:
   - **OpenCV Haar Cascades** - Fast, lightweight face detection (no GPU required)
   - **DeepFace** - Advanced face detection + recognition + emotion/age/gender analysis
   - **YOLO (Ultralytics)** - State-of-the-art object detection with 80+ object classes
3. **Streams annotated video** - WebSocket or MJPEG stream to web UI with bounding boxes and labels
4. **Exposes detection data** - REST API and real-time events for detected faces/objects
5. **Enables reactive behaviors** - Robot can look at detected faces, react to specific objects
6. **Supports model hot-swapping** - Switch between backends via API without restart

## Relevant Files

Use these files to implement the feature:

- [main.py](reachy_mini_local_companion/main.py) - Core application logic; integrate vision pipeline, add detection event handling, new API endpoints
- [static/index.html](reachy_mini_local_companion/static/index.html) - Web UI; add video stream display, detection overlay canvas, model selector
- [static/main.js](reachy_mini_local_companion/static/main.js) - Frontend JavaScript; add video stream handling, detection visualization, settings controls
- [static/style.css](reachy_mini_local_companion/static/style.css) - Styling; add video container styles, detection overlay styles
- [pyproject.toml](pyproject.toml) - Project config; add new dependencies (opencv-python, deepface, ultralytics)
- [.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md](.claude/references/robotics/pollen-robotics/reachy-mini-sdk.md) - SDK reference for camera API (`mini.camera.get_frame()`)

### New Files

- `reachy_mini_local_companion/vision/__init__.py` - Vision module package init
- `reachy_mini_local_companion/vision/base.py` - Abstract base class for vision backends
- `reachy_mini_local_companion/vision/detections.py` - Detection result dataclasses (Face, Object, BoundingBox)
- `reachy_mini_local_companion/vision/opencv_backend.py` - OpenCV Haar Cascade implementation
- `reachy_mini_local_companion/vision/deepface_backend.py` - DeepFace implementation for advanced face analysis
- `reachy_mini_local_companion/vision/yolo_backend.py` - YOLO/Ultralytics implementation for object detection
- `reachy_mini_local_companion/vision/pipeline.py` - Vision pipeline orchestrator (frame capture, processing, streaming)
- `reachy_mini_local_companion/vision/stream.py` - Video streaming utilities (MJPEG, WebSocket)

## Implementation Plan

### Phase 1: Foundation

Establish the vision module architecture and data models:

1. Create the `vision/` package with base abstractions
2. Define detection result dataclasses that all backends will use
3. Implement the abstract `VisionBackend` base class defining the interface
4. Set up the vision pipeline orchestrator that manages frame capture and processing

### Phase 2: Core Implementation

Implement the three vision backends:

1. **OpenCV Backend** - Lightweight face detection using Haar Cascades
   - Fast startup, no model downloads
   - Face detection only (no recognition)
   - Ideal for resource-constrained environments

2. **DeepFace Backend** - Comprehensive face analysis
   - Face detection with multiple detector options (opencv, ssd, mtcnn, retinaface)
   - Face recognition against registered faces
   - Emotion, age, gender analysis
   - Anti-spoofing detection

3. **YOLO Backend** - General object detection
   - 80+ object classes (COCO dataset)
   - Configurable model size (yolov8n for speed, yolov8l for accuracy)
   - Real-time performance on modern hardware

### Phase 3: Integration

Connect the vision system to the main application:

1. Add video streaming endpoint (MJPEG for simplicity, WebSocket optional)
2. Expose REST API for detection data, backend switching, and configuration
3. Update web UI with video display and detection overlays
4. Implement face-tracking behavior (robot looks at detected faces)
5. Add detection event callbacks for custom behaviors

## Step by Step Tasks

### Step 1: Create Vision Package Structure

- Create `reachy_mini_local_companion/vision/` directory
- Create `__init__.py` with package exports
- This establishes the modular structure for the vision system

### Step 2: Define Detection Data Models

- Create `vision/detections.py` with Pydantic models:
  - `BoundingBox` - x, y, width, height, confidence
  - `FaceDetection` - bounding_box, landmarks (optional), face_id (optional)
  - `FaceAnalysis` - extends FaceDetection with emotion, age, gender
  - `ObjectDetection` - bounding_box, class_name, class_id, confidence
  - `DetectionResult` - timestamp, frame_id, faces list, objects list
- Use Pydantic for JSON serialization to API

### Step 3: Create Abstract Vision Backend

- Create `vision/base.py` with abstract `VisionBackend` class:
  - `name: str` property - backend identifier
  - `capabilities: set[str]` - what this backend can do (face_detection, face_recognition, object_detection, etc.)
  - `initialize()` - load models, prepare backend
  - `process_frame(frame: np.ndarray) -> DetectionResult` - main processing method
  - `shutdown()` - cleanup resources
  - `configure(settings: dict)` - update backend settings
- Define `BackendCapability` enum: FACE_DETECTION, FACE_RECOGNITION, EMOTION_ANALYSIS, OBJECT_DETECTION, etc.

### Step 4: Implement OpenCV Haar Cascade Backend

- Create `vision/opencv_backend.py`:
  - Load Haar Cascade classifiers for face detection
  - Implement `process_frame()` using `cv2.CascadeClassifier.detectMultiScale()`
  - Convert detections to `FaceDetection` objects
  - Configuration: scale_factor, min_neighbors, min_size
- This provides a zero-dependency baseline (OpenCV is already a common dep)

### Step 5: Implement DeepFace Backend

- Create `vision/deepface_backend.py`:
  - Wrap DeepFace library for face detection and analysis
  - Implement `process_frame()` using `DeepFace.analyze()` or `DeepFace.extract_faces()`
  - Support multiple detector backends (opencv, ssd, mtcnn, retinaface, yolo)
  - Extract emotion, age, gender when enabled
  - Configuration: detector_backend, enforce_detection, anti_spoofing
- Lazy-load models on first use to reduce startup time

### Step 6: Implement YOLO Backend

- Create `vision/yolo_backend.py`:
  - Load YOLO model from Ultralytics (`YOLO("yolov8n.pt")`)
  - Implement `process_frame()` using `model.predict()`
  - Convert results to `ObjectDetection` objects
  - Support model size selection (nano, small, medium, large)
  - Configuration: model_size, confidence_threshold, iou_threshold, classes filter
- Download models on first use (cached after)

### Step 7: Create Vision Pipeline Orchestrator

- Create `vision/pipeline.py` with `VisionPipeline` class:
  - Manages frame capture from `ReachyMini.camera`
  - Runs selected backend on each frame
  - Maintains frame buffer for streaming
  - Publishes detection events
  - Handles backend switching
  - Thread-safe operation with processing thread
- Methods:
  - `start(reachy_mini: ReachyMini)` - begin capture and processing
  - `stop()` - halt pipeline
  - `get_latest_frame()` - return last processed frame with annotations
  - `get_latest_detections()` - return most recent DetectionResult
  - `set_backend(backend_name: str)` - switch active backend
  - `add_detection_callback(fn)` - register detection event handler

### Step 8: Implement MJPEG Video Streaming

- Create `vision/stream.py` with streaming utilities:
  - `generate_mjpeg_stream(pipeline: VisionPipeline)` - generator for MJPEG frames
  - Add bounding box overlays to frames before encoding
  - Configure stream FPS and quality
- Uses standard multipart/x-mixed-replace MIME type for browser compatibility

### Step 9: Add Vision Endpoints to Main Application

- In `main.py`, integrate vision pipeline:
  - Import vision module
  - Initialize `VisionPipeline` in app startup
  - Add endpoints:
    - `GET /video_feed` - MJPEG stream endpoint
    - `GET /detections` - Latest detection results as JSON
    - `GET /vision/backends` - List available backends
    - `POST /vision/backend` - Switch active backend
    - `POST /vision/config` - Update backend configuration
    - `POST /vision/start` - Start vision processing
    - `POST /vision/stop` - Stop vision processing
- Pass `reachy_mini` instance to pipeline

### Step 10: Add Face Tracking Behavior

- In `main.py`, add face tracking mode:
  - Register detection callback
  - When face detected, calculate head pose to center face in frame
  - Use `look_at_world()` or `set_target()` to point at face
  - Add toggle for enabling/disabling face tracking
  - Configuration: tracking_speed, smoothing_factor
- Endpoint: `POST /vision/face_tracking` to enable/disable

### Step 11: Update HTML with Vision UI

- In `static/index.html`, add vision section:
  - `<div id="vision-container">` - main container
  - `<img id="video-feed">` - MJPEG stream display
  - `<canvas id="detection-overlay">` - for custom overlays (optional)
  - Backend selector dropdown
  - Face tracking toggle
  - Detection statistics display (FPS, face count, object count)
  - Start/Stop vision buttons

### Step 12: Implement JavaScript Vision Handling

- In `static/main.js`, add vision functions:
  - `startVideoFeed()` - Set img src to `/video_feed`
  - `stopVideoFeed()` - Clear img src
  - `async function switchBackend(name)` - POST to `/vision/backend`
  - `async function toggleFaceTracking(enabled)` - POST to `/vision/face_tracking`
  - `async function fetchDetections()` - Poll `/detections` for stats display
  - Event listeners for all vision controls
  - Error handling for stream disconnection

### Step 13: Style Vision UI

- In `static/style.css`, add:
  - `#vision-container` layout (centered, responsive width)
  - `#video-feed` styling (16:9 aspect ratio, border, shadow)
  - Backend selector dropdown styling
  - Detection stats panel styling
  - Toggle buttons for face tracking
  - Loading/error states for video feed

### Step 14: Update Dependencies

- In `pyproject.toml`, add optional dependencies group:
  ```toml
  [project.optional-dependencies]
  vision = [
      "opencv-python>=4.8.0",
  ]
  vision-advanced = [
      "opencv-python>=4.8.0",
      "deepface>=0.0.89",
      "ultralytics>=8.0.0",
  ]
  ```
- Document that `vision-advanced` requires more disk space for models

### Step 15: Run Validation Commands

- Run all validation commands to ensure zero regressions
- Test each backend individually
- Verify video streaming works in browser
- Test face tracking behavior
- Check API endpoints respond correctly

## Testing Strategy

### Unit Tests

- Test `BoundingBox`, `FaceDetection`, `ObjectDetection` model creation and serialization
- Test each backend's `process_frame()` with sample images
- Test backend switching logic
- Test pipeline start/stop lifecycle
- Mock camera input for deterministic testing

### Integration Tests

- Test MJPEG streaming endpoint returns valid multipart response
- Test `/detections` returns properly formatted JSON
- Test `/vision/backend` switching works without errors
- Test `/vision/config` updates backend settings
- Test face tracking callback integration
- Test simultaneous vision + emotion display operation

### Edge Cases

- No face in frame (should return empty faces list)
- Multiple faces in frame (should detect all)
- Poor lighting conditions (test detection robustness)
- Backend not available (graceful error handling)
- Camera disconnection mid-stream
- Rapid backend switching
- Large objects filling frame
- Face at edge of frame (partial visibility)
- Model download failure (network issues)

## Acceptance Criteria

1. Video feed displays in web UI with <200ms latency
2. OpenCV backend detects faces with >80% accuracy on frontal faces
3. DeepFace backend provides emotion/age/gender analysis
4. YOLO backend detects common objects (person, cup, phone, etc.)
5. Switching backends via API works without restart
6. Detection results available via `/detections` endpoint
7. Bounding boxes rendered on video stream
8. Face tracking mode makes robot look at detected faces
9. Vision system runs concurrently with existing animations
10. Graceful degradation when camera unavailable
11. No regressions in existing antenna, sound, and emotion functionality

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/__init__.py` - Verify vision package syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/base.py` - Verify base module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/detections.py` - Verify detections module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/opencv_backend.py` - Verify OpenCV backend syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/deepface_backend.py` - Verify DeepFace backend syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/yolo_backend.py` - Verify YOLO backend syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/pipeline.py` - Verify pipeline module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/vision/stream.py` - Verify stream module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -m py_compile reachy_mini_local_companion/main.py` - Verify main module syntax
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -c "from reachy_mini_local_companion.vision import VisionPipeline; print('Vision module imports successfully')"` - Verify vision module imports
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -c "from reachy_mini_local_companion.vision.opencv_backend import OpenCVBackend; print('OpenCV backend available')"` - Verify OpenCV backend
- `cd /Users/duck/Projects/reachy_mini_local_companion && python -c "from reachy_mini_local_companion.main import ReachyMiniLocalCompanion; print('Main module imports successfully')"` - Verify main module imports

## Notes

- **New dependencies required**:
  - `opencv-python>=4.8.0` - Base requirement for all vision features
  - `deepface>=0.0.89` - Optional, for advanced face analysis (downloads ~500MB of models)
  - `ultralytics>=8.0.0` - Optional, for YOLO object detection (downloads ~6MB-130MB per model)

- **Model download considerations**:
  - DeepFace downloads models on first use (~500MB for VGG-Face)
  - YOLO downloads models on first use (yolov8n.pt ~6MB, yolov8l.pt ~130MB)
  - Consider pre-downloading models or documenting first-run behavior

- **Performance considerations**:
  - OpenCV Haar Cascades: ~30+ FPS on CPU
  - DeepFace with OpenCV detector: ~5-15 FPS on CPU
  - YOLO nano: ~30+ FPS on CPU, ~100+ FPS on GPU
  - Consider frame skipping for slower backends
  - Run detection in separate thread to not block main loop

- **Camera resolution**:
  - Reachy Mini camera provides frames at ~640x480 or configurable resolution
  - Higher resolution improves small face detection but reduces FPS

- **Future enhancements**:
  - Face database for recognition ("Who is this?")
  - Object memory ("Remember where my cup is")
  - Gesture recognition (hand tracking)
  - QR/barcode scanning
  - GPU acceleration (CUDA/Metal)
  - WebSocket streaming for lower latency
  - Recording and playback of vision sessions

- **External resources used for research**:
  - [DeepFace GitHub](https://github.com/serengil/deepface) - Face recognition library
  - [Ultralytics YOLO](https://www.ultralytics.com/glossary/opencv) - Object detection models
  - [OpenCV Face Detection Tutorial](https://www.datacamp.com/tutorial/face-detection-python-opencv) - Haar Cascade approach
