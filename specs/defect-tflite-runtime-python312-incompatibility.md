# defect: tflite-runtime Python 3.12 Incompatibility

## defect Description
When attempting to set up the virtual environment on Reachy Mini using `uv sync` or `uv pip install`, the installation fails with the following error:

```
error: Distribution `tflite-runtime==2.14.0 @ registry+https://pypi.org/simple` can't be installed because it doesn't have a source distribution or wheel for the current platform

hint: You're using CPython 3.12 (`cp312`), but `tflite-runtime` (v2.14.0) only has wheels with the following Python ABI tags: `cp310`, `cp311`
```

**Expected behavior:** The virtual environment should install successfully on Python 3.12.

**Actual behavior:** Installation fails because `tflite-runtime` 2.14.0 does not provide wheels for Python 3.12.

## Problem Statement
The `openwakeword` dependency (v0.6.0) declares `tflite-runtime` as a hard dependency on Linux systems via `marker = "platform_system == 'Linux'"`. However, `tflite-runtime` is an abandoned package that only provides wheels for Python 3.10 and 3.11, not 3.12+. This blocks installation on Reachy Mini which runs Python 3.12 on Linux.

## Solution Statement
Use uv's `override-dependencies` feature with an impossible marker (`sys_platform == 'never'`) to effectively exclude `tflite-runtime` from the dependency resolution. The `openwakeword` library already supports ONNX runtime as an alternative inference framework (and the codebase already configures `inference_framework="onnx"` in `wake_word.py:66`), so excluding `tflite-runtime` will not break functionality.

Note: The `exclude-dependencies` setting exists in newer uv versions but is not available in uv 0.5.x. The `override-dependencies` workaround achieves the same effect.

## Steps to Reproduce
1. Clone the repository on a Linux system with Python 3.12
2. Run `uv sync` or `uv pip install -e .`
3. Observe the error about `tflite-runtime` incompatibility

## Root Cause Analysis
The root cause is a dependency chain issue:

1. `reachy_mini_local_companion` depends on `openwakeword>=0.6.0`
2. `openwakeword` 0.6.0 has a conditional dependency: `tflite-runtime; platform_system == 'Linux'`
3. `tflite-runtime` 2.14.0 (latest version) only ships wheels for `cp310` and `cp311`
4. The Reachy Mini runs Python 3.12 (`cp312`) on Linux
5. uv cannot find a compatible wheel and there's no source distribution to build from

The `tflite-runtime` package is effectively abandoned (last release was October 2023) and Google has stopped providing new builds. The `openwakeword` maintainers are aware of this issue ([GitHub Issue #159](https://github.com/dscripka/openWakeWord/issues/159)) but the package metadata still declares the dependency.

Fortunately, `openwakeword` supports both `onnxruntime` and `tflite-runtime` as inference backends. The codebase already uses ONNX by specifying `inference_framework="onnx"` when creating the Model, so `tflite-runtime` is not actually needed at runtime.

## Relevant Files
Use these files to fix the defect:

- **pyproject.toml** - Add uv configuration to exclude `tflite-runtime` from dependency resolution
- **uv.lock** - Will be regenerated after pyproject.toml changes to exclude the problematic dependency
- **reachy_mini_local_companion/stt/wake_word.py** - Already correctly uses `inference_framework="onnx"` (line 66), no changes needed but confirms ONNX is the intended backend

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add uv override-dependencies configuration
- Open `pyproject.toml`
- Add a `[tool.uv]` section at the end of the file
- Add `override-dependencies = ["tflite-runtime; sys_platform == 'never'"]` to exclude the problematic package
- The impossible marker `sys_platform == 'never'` ensures the package is never installed on any platform

### Step 2: Regenerate the lock file
- Run `uv lock` to regenerate `uv.lock` without `tflite-runtime`
- Verify the lock file no longer contains `tflite-runtime`

### Step 3: Verify the fix
- Run `uv sync` to install dependencies
- Verify installation completes successfully
- Run a quick import test to ensure `openwakeword` works with ONNX backend

## Validation Commands
Execute every command to validate the defect is fixed with zero regressions.

- `grep -c "tflite-runtime" uv.lock` - Should return `0` (no tflite-runtime in lock file)
- `uv sync` - Should complete without errors on Python 3.12
- `uv run python -c "from openwakeword import Model; print('openwakeword imports successfully')"` - Verify openwakeword can be imported
- `uv run python -c "from reachy_mini_local_companion.stt.wake_word import WakeWordDetector; print('WakeWordDetector imports successfully')"` - Verify wake word module works

## Notes
- The `tflite-runtime` package is deprecated and no longer maintained by Google. See [wyoming-openwakeword Issue #40](https://github.com/rhasspy/wyoming-openwakeword/issues/40) for community discussion.
- The `openwakeword` library supports both ONNX and TFLite backends. On Windows, only ONNX is used. This fix aligns the Linux behavior with Windows.
- No code changes are required since the codebase already uses `inference_framework="onnx"` in `wake_word.py`.
- This fix is forward-compatible with future Python versions (3.13+) that will also lack `tflite-runtime` support.
- If `openwakeword` releases a new version that removes the `tflite-runtime` dependency, the `exclude-dependencies` configuration can be removed.
