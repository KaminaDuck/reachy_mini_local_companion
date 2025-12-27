---
title: "pytest-xdist Plugin Reference"
description: "pytest plugin for parallel and distributed test execution across multiple CPUs and machines"
type: "tool-reference"
tags: ["pytest", "parallel", "distributed", "testing", "python", "performance", "xdist", "workers"]
category: "python"
subcategory: "dev-tools"
version: "3.8.0"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "pytest-xdist Documentation"
    url: "https://pytest-xdist.readthedocs.io/"
  - name: "pytest-xdist PyPI"
    url: "https://pypi.org/project/pytest-xdist/"
  - name: "pytest-xdist How-To"
    url: "https://pytest-xdist.readthedocs.io/en/stable/how-to.html"
  - name: "pytest-xdist GitHub"
    url: "https://github.com/pytest-dev/pytest-xdist"
  - name: "pytest-xdist Changelog"
    url: "https://pytest-xdist.readthedocs.io/en/latest/changelog.html"
related: ["pytest-tool-reference.md", "pytest-asyncio-plugin.md"]
author: "unknown"
contributors: []
---

# pytest-xdist Plugin Reference

pytest-xdist is a pytest plugin that extends test execution capabilities with distributed testing functionality. Its primary purpose is "distributing tests across multiple CPUs to speed up test execution." The plugin enables developers to run test suites more efficiently by leveraging multiple processors simultaneously. ([pytest-xdist Documentation][1])

## Overview

pytest-xdist enables parallel test execution by spawning multiple worker processes that execute tests concurrently, significantly reducing overall test suite execution time.

### System Requirements

- **Python versions**: 3.9+ ([pytest-xdist PyPI][2])
- **Installation**: `pip install pytest-xdist` or `uv add --dev pytest-xdist`
- **Optional dependency**: Install with `[psutil]` extra for automatic CPU detection
- **Minimum version**: 3.5 recommended

### Key Features

1. **Parallel Test Execution** - Run tests across multiple CPU cores simultaneously
2. **Load Balancing** - Intelligently distribute tests across workers
3. **Remote Execution** - Execute tests on remote machines via SSH
4. **Flexible Distribution** - Multiple strategies for test distribution
5. **Worker Identification** - Access worker info within tests for isolation

## Installation

Install the basic plugin:

```bash
pip install pytest-xdist
```

For CPU detection capabilities, install with the psutil extra:

```bash
pip install pytest-xdist[psutil]
```

([pytest-xdist Documentation][1])

## Basic Usage

### Parallel Execution

The core feature uses the `-n` flag for parallelization:

```bash
pytest -n auto
```

This command spawns worker processes equal to the number of available CPUs and "distribute[s] the tests randomly across them." ([pytest-xdist Documentation][1])

### Specify Number of Workers

```bash
# Run with 4 workers
pytest -n 4

# Run with logical CPU count
pytest -n logical

# Run with auto-detection (requires psutil)
pytest -n auto
```

### Configuration File

Specify default worker counts in pytest configuration:

```ini
[pytest]
addopts = -n auto
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-n auto"
```

([pytest-xdist How-To][3])

## Distribution Modes

The documentation identifies three primary execution modes. ([pytest-xdist Documentation][1])

### 1. Local CPU Distribution (Default)

Tests run across available processor cores on a single machine using the `load` algorithm:

```bash
pytest -n auto
```

### 2. Load Balancing by Scope

The `--dist=loadscope` mode groups tests by module or class and distributes entire groups to workers. This is useful when tests within a scope share expensive setup:

```bash
pytest -n auto --dist=loadscope
```

Version 3.7+ sorts scopes by number of tests to assign largest scopes early, which can improve overall test session running time. ([pytest-xdist Changelog][5])

### 3. Load Balancing by File

The `--dist=loadfile` mode distributes tests by file:

```bash
pytest -n auto --dist=loadfile
```

### 4. Load Balancing by Group

Use the `@pytest.mark.xdist_group` marker to group related tests:

```python
import pytest

@pytest.mark.xdist_group(name="database")
def test_db_operation_1():
    pass

@pytest.mark.xdist_group(name="database")
def test_db_operation_2():
    pass
```

Tests with the same group name run on the same worker, ensuring shared resources don't conflict.

### 5. Each Test in All Workers

The `--dist=each` mode runs each test in every worker (useful for stress testing):

```bash
pytest -n 4 --dist=each
```

## Worker Identification

The documentation provides several methods to identify worker processes during tests. ([pytest-xdist How-To][3])

### worker_id Fixture

```python
def test_worker_id(worker_id):
    # Returns "gw0", "gw1", etc., or "master" when xdist is disabled
    print(f"Running on worker: {worker_id}")
```

### Environment Variables

- **`PYTEST_XDIST_WORKER`**: Set in worker processes (e.g., "gw0", "gw1")
- **`PYTEST_XDIST_WORKER_COUNT`**: Total number of workers
- **`PYTEST_XDIST_TESTRUNUID`**: Unique identifier for the test run across all workers

```python
import os

def test_with_env():
    worker = os.environ.get("PYTEST_XDIST_WORKER", "master")
    worker_count = os.environ.get("PYTEST_XDIST_WORKER_COUNT", "1")
    print(f"Worker {worker} of {worker_count}")
```

### API Functions (Version 2.0+)

```python
from xdist import is_xdist_worker, is_xdist_controller, get_xdist_worker_id

def test_xdist_detection():
    if is_xdist_worker():
        worker_id = get_xdist_worker_id()
        print(f"Running in worker: {worker_id}")
    elif is_xdist_controller():
        print("Running in controller process")
    else:
        print("xdist not active")
```

([pytest-xdist How-To][3])

## Fixture Handling

### Session-Scoped Fixtures

A critical consideration for distributed testing: "each worker process will perform its own collection and execute a subset of all tests," potentially causing session-scoped fixtures to execute multiple times. The documentation recommends using file-based locking (like FileLock) to ensure expensive fixtures run only once across all workers. ([pytest-xdist How-To][3])

```python
import pytest
from filelock import FileLock

@pytest.fixture(scope="session")
def expensive_resource(tmp_path_factory, worker_id):
    if worker_id == "master":
        # Not running with xdist
        return setup_expensive_resource()

    # Get a temp directory shared by all workers
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    lock_file = root_tmp_dir / "resource.lock"
    data_file = root_tmp_dir / "resource.json"

    with FileLock(str(lock_file)):
        if data_file.exists():
            # Another worker already created it
            return load_resource(data_file)
        else:
            # First worker creates the resource
            resource = setup_expensive_resource()
            save_resource(resource, data_file)
            return resource
```

### Per-Worker Fixtures

Use the `worker_id` fixture to create isolated resources per worker:

```python
import pytest

@pytest.fixture(scope="session")
def database_per_worker(worker_id):
    db_name = f"test_db_{worker_id}"
    db = create_database(db_name)
    yield db
    drop_database(db_name)
```

### Module and Class Scoped Fixtures

Module and class-scoped fixtures work naturally with xdist - each worker executes them for the tests it runs.

## Remote Execution

pytest-xdist supports executing tests on remote machines with "rsync" synchronization for source code. ([pytest-xdist Documentation][1])

### SSH Remote Execution

```bash
pytest -d --tx ssh=user@remote.host --rsyncdir myproject
```

### Configuration for Remote Testing

In `pytest.ini`:

```ini
[pytest]
rsyncdirs = myproject tests
rsyncignore = .git *.pyc __pycache__
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
rsyncdirs = ["myproject", "tests"]
rsyncignore = [".git", "*.pyc", "__pycache__"]
```

([pytest-xdist How-To][3])

## Worker Management Features

### Test Run Identification

Version 3.7+ added a `testrun_uid` fixture as a shared value that uniquely identifies a test run among all workers, along with a `PYTEST_XDIST_TESTRUNUID` environment variable and `--testrunuid` command-line option. ([pytest-xdist Changelog][5])

```python
def test_with_testrun_uid(testrun_uid):
    # Unique ID shared across all workers in this test run
    print(f"Test run UID: {testrun_uid}")
```

### Main Thread Execution

pytest-xdist workers now always execute tests in the main thread, which helps avoid problems with async frameworks where the event loop is running in the main thread. ([pytest-xdist Changelog][5])

## Logging and Monitoring

The `PYTEST_XDIST_WORKER` environment variable enables per-worker logging configuration, allowing each worker to generate separate log files. ([pytest-xdist How-To][3])

### Per-Worker Log Files

```python
# conftest.py
import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def configure_worker_logging():
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    log_file = f"tests_{worker_id}.log"

    import logging
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
```

### Progress Reporting

```bash
# Show detailed progress
pytest -n auto -v

# Show summary of all tests
pytest -n auto -ra
```

## Limitations and Considerations

### Output Capture

**Important Limitation:** "Due to how pytest-xdist is implemented, the `-s/--capture=no` option does not work." ([pytest-xdist Documentation][1])

Standard output from tests running in workers is captured and reported by the controller, but live output streaming is not available.

### Test Order and Consistency

"Order and amount of test must be consistent" across workers. ([pytest-xdist Documentation][1]) Tests are distributed dynamically, so:

- Test execution order is non-deterministic
- Tests must be independent and isolated
- Avoid relying on test execution order
- Don't use shared state between tests

### Fixture Scope Considerations

- **function-scoped**: Works normally, each test gets its own
- **class-scoped**: Executed once per class per worker
- **module-scoped**: Executed once per module per worker
- **session-scoped**: Requires special handling (see Fixture Handling section)

### Plugin Compatibility

Some pytest plugins may not work correctly with xdist, especially those that:
- Assume single-process execution
- Modify global state
- Depend on test execution order

## Performance Optimization

### Choosing Worker Count

```bash
# Physical cores (usually optimal)
pytest -n auto

# Logical cores (includes hyperthreading)
pytest -n logical

# Specific count (for tuning)
pytest -n 8
```

### Load Distribution Strategies

Choose the right distribution mode based on your test suite:

- **Default (`load`)**: Best for uniform test distribution
- **`loadscope`**: Best when tests share expensive module/class fixtures
- **`loadfile`**: Best when files represent logical test groups
- **`loadgroup`**: Best for explicit control over test grouping

### Test Collection Performance

For large test suites, consider:

```bash
# Cache test collection between runs
pytest -n auto --cache-show

# Skip slow collection with --collect-only first
pytest --collect-only  # Verify collection
pytest -n auto         # Then run in parallel
```

## Best Practices

### Write Isolated Tests

```python
# Good: Each test is independent
def test_user_creation():
    user = create_user("alice")
    assert user.name == "alice"

def test_user_deletion():
    user = create_user("bob")
    delete_user(user)
    assert not user_exists("bob")

# Bad: Tests depend on execution order
user = None

def test_create():
    global user
    user = create_user("alice")

def test_read():
    global user
    assert user.name == "alice"  # Fails if test_create runs on different worker
```

### Use Appropriate Distribution

```python
# Group database tests together
import pytest

@pytest.mark.xdist_group("database")
class TestDatabaseOperations:
    def test_insert(self):
        pass

    def test_query(self):
        pass

    def test_delete(self):
        pass
```

### Handle Shared Resources

```python
from filelock import FileLock

@pytest.fixture(scope="session")
def shared_data(tmp_path_factory, worker_id):
    if worker_id == "master":
        return {"counter": 0}

    # Use file locking for worker isolation
    root_tmp = tmp_path_factory.getbasetemp().parent
    lock = root_tmp / "data.lock"

    with FileLock(str(lock)):
        # Safely access shared resource
        return {"counter": 0}
```

### Configure Sensible Defaults

```toml
[tool.pytest.ini_options]
# Use auto-detection by default
addopts = "-n auto"

# Use loadscope for test suites with expensive fixtures
# addopts = "-n auto --dist=loadscope"

# Disable xdist for debugging
# addopts = "-n 0"
```

### Debug Parallel Tests

```bash
# Disable parallelization for debugging
pytest -n 0

# Or don't use -n flag at all
pytest

# Run with single worker to maintain serial execution
pytest -n 1

# Increase verbosity to see worker assignments
pytest -n auto -vv
```

## Common Use Cases

### Speed Up CI/CD Pipelines

```yaml
# .github/workflows/test.yml
- name: Run tests in parallel
  run: |
    pip install pytest pytest-xdist[psutil]
    pytest -n auto --maxfail=5
```

### Test Matrix Execution

```bash
# Test on multiple Python versions in parallel
tox -p auto
```

### Stress Testing

```bash
# Run each test 100 times across 4 workers
pytest -n 4 --dist=each --count=100
```

### Isolate Slow Tests

```python
# Mark slow tests
import pytest

@pytest.mark.slow
def test_expensive_operation():
    pass

# Run slow tests separately with more workers
# pytest -m slow -n 8
# pytest -m "not slow" -n auto
```

## Integration with Other Tools

### pytest-asyncio

Async tests work with xdist - each worker gets its own event loop:

```bash
pytest -n auto  # Works with async tests
```

### pytest-cov

For code coverage with parallel execution:

```bash
pytest -n auto --cov=myapp --cov-report=html
```

### pytest-timeout

Timeout per test still works in distributed mode:

```bash
pytest -n auto --timeout=30
```

## Troubleshooting

### Tests Hang or Timeout

- Check for shared state or race conditions
- Verify session-scoped fixtures use proper locking
- Disable xdist to isolate the issue: `pytest -n 0`

### Inconsistent Test Results

- Ensure tests are truly independent
- Remove test execution order dependencies
- Check for global state modifications

### Performance Not Improving

- Profile test suite to identify bottlenecks
- Consider `--dist=loadscope` for fixture-heavy tests
- Check if test collection is the bottleneck
- Verify you have enough independent tests to distribute

### Worker Crashes

- Check logs in individual worker output
- Run with `-vv` to see worker assignments
- Test with single worker: `pytest -n 1`

## Version Information

This reference covers pytest-xdist version 3.8.0, released July 1, 2025. The plugin requires Python 3.9+. ([pytest-xdist PyPI][2])

## References

[1]: https://pytest-xdist.readthedocs.io/ "pytest-xdist Documentation"
[2]: https://pypi.org/project/pytest-xdist/ "pytest-xdist PyPI"
[3]: https://pytest-xdist.readthedocs.io/en/stable/how-to.html "pytest-xdist How-To"
[4]: https://github.com/pytest-dev/pytest-xdist "pytest-xdist GitHub"
[5]: https://pytest-xdist.readthedocs.io/en/latest/changelog.html "pytest-xdist Changelog"
