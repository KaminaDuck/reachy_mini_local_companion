---
title: "pytest-asyncio Plugin Reference"
description: "pytest plugin for testing asyncio code with async fixtures and event loop management"
type: "tool-reference"
tags: ["pytest", "asyncio", "testing", "python", "async", "fixtures", "coroutines"]
category: "python"
subcategory: "dev-tools"
version: "1.2.0"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "pytest-asyncio Documentation"
    url: "https://pytest-asyncio.readthedocs.io/"
  - name: "pytest-asyncio PyPI"
    url: "https://pypi.org/project/pytest-asyncio/"
  - name: "pytest-asyncio Concepts"
    url: "https://pytest-asyncio.readthedocs.io/en/stable/concepts.html"
  - name: "pytest-asyncio GitHub"
    url: "https://github.com/pytest-dev/pytest-asyncio"
  - name: "pytest-asyncio Changelog"
    url: "https://pytest-asyncio.readthedocs.io/en/stable/reference/changelog.html"
related: ["pytest-tool-reference.md", "pytest-xdist-plugin.md"]
author: "unknown"
contributors: []
---

# pytest-asyncio Plugin Reference

pytest-asyncio is a pytest plugin designed to facilitate testing of code utilizing Python's asyncio library. It "provides support for coroutines as test functions," enabling developers to use await syntax within test code. ([pytest-asyncio Documentation][1])

## Overview

pytest-asyncio enables asynchronous test functions through the `@pytest.mark.asyncio` decorator, allowing coroutines to be executed as test items by pytest. ([pytest-asyncio Documentation][1])

### System Requirements

- **Python versions**: 3.9 through 3.14 ([pytest-asyncio PyPI][2])
- **Installation**: `pip install pytest-asyncio` or `uv add --dev pytest-asyncio`
- **Minimum version**: 1.1.0 recommended

### Key Features

1. **Async Test Functions** - Write test functions using async/await syntax
2. **Async Fixtures** - Define fixtures that use asyncio operations
3. **Event Loop Management** - Automatic event loop creation and cleanup per test scope
4. **Flexible Loop Scoping** - Control event loop lifetime from function to session level
5. **Multiple Modes** - Auto and strict modes for different project needs

## Basic Usage

### Simple Async Test

The documentation demonstrates a simple implementation:

```python
import pytest

@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

([pytest-asyncio Documentation][1])

### Async Fixtures

Define async fixtures using the `@pytest_asyncio.fixture` decorator:

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def async_database():
    db = await create_async_database()
    yield db
    await db.close()

@pytest.mark.asyncio
async def test_database_query(async_database):
    result = await async_database.query("SELECT 1")
    assert result is not None
```

## Event Loop Management

pytest-asyncio provides one asyncio event loop per pytest collector level (Session, Package, Module, Class, or Function). By default, tests run in the Function-scoped loop for maximum isolation. You can adjust this using the `loop_scope` parameter in the `@pytest.mark.asyncio` decorator to share loops across tests with common ancestors. ([pytest-asyncio Concepts][3])

### Loop Scopes

Available loop scopes:

- **function** (default): New event loop for each test function
- **class**: Shared event loop for all tests in a class
- **module**: Shared event loop for all tests in a module
- **package**: Shared event loop for all tests in a package
- **session**: Single event loop for entire test session

```python
import pytest

@pytest.mark.asyncio(loop_scope="module")
async def test_with_module_scope():
    # Shares event loop with other module-scoped tests
    await asyncio.sleep(0.1)
    assert True

@pytest.mark.asyncio(loop_scope="session")
async def test_with_session_scope():
    # Shares event loop across entire test session
    await asyncio.sleep(0.1)
    assert True
```

The documentation states: "It's highly recommended for neighboring tests to use the same event loop scope." Mixing different scopes among related tests can reduce code clarity and maintainability. ([pytest-asyncio Concepts][3])

## Test Discovery Modes

pytest-asyncio supports two modes for test discovery and fixture handling. ([pytest-asyncio Concepts][3])

### Strict Mode (Default)

- Only executes tests marked with `@pytest.mark.asyncio`
- Only processes async fixtures decorated with `@pytest_asyncio.fixture`
- Enables coexistence with other async testing libraries

Configure in `pytest.ini`:

```ini
[pytest]
asyncio_mode = strict
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "strict"
```

([pytest-asyncio Concepts][3])

### Auto Mode

- Automatically marks all async test functions
- Takes ownership of all async fixtures regardless of decorator type
- Simplifies configuration for asyncio-only projects

The documentation notes: "Auto mode makes for the simplest test and fixture configuration and is the recommended default." ([pytest-asyncio Concepts][3])

Configure in `pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

With auto mode, you can simplify test code:

```python
# No decorator needed in auto mode
async def test_automatically_marked():
    await asyncio.sleep(0.1)
    assert True
```

## Execution Model

pytest-asyncio runs async tests sequentially, not concurrently. This preserves test isolation and prevents race conditions, mirroring how pytest handles synchronous tests. Sequential execution ensures reliable, debuggable results. ([pytest-asyncio Concepts][3])

## Version 1.0+ Changes

Version 1.0.0 was released on May 25, 2025, introducing significant changes aimed at simplifying the API, improving performance, and aligning more closely with modern asyncio practices. ([pytest-asyncio Changelog][5])

### Major Changes

1. **Event Loop Fixture Removal**: The `event_loop` fixture has been completely removed, pushing towards a more standardized way of handling event loops. ([pytest-asyncio Changelog][5])

2. **Performance Improvements**: Scoped event loops (e.g. module-scoped loops) are created once rather than per scope (e.g. per module), which reduces the number of fixtures and speeds up collection time, especially for large test suites. ([pytest-asyncio Changelog][5])

3. **Enhanced Flexibility**: The `loop_scope` argument to `pytest.mark.asyncio` no longer forces that a pytest Collector exists at the level of the specified scope. For example, a test function marked with `pytest.mark.asyncio(loop_scope="class")` no longer requires a class surrounding the test. ([pytest-asyncio Changelog][5])

4. **Bug Fixes**: Fixed RuntimeError: "There is no current event loop in thread 'MainThread'" when any test unsets the event loop (such as when using `asyncio.run` and `asyncio.Runner`). ([pytest-asyncio Changelog][5])

## Configuration Options

### asyncio_mode

Sets the test discovery mode (auto or strict):

```ini
[pytest]
asyncio_mode = auto
```

### asyncio_default_fixture_loop_scope

Sets the default loop scope for async fixtures:

```ini
[pytest]
asyncio_default_fixture_loop_scope = function
```

### Command-Line Options

pytest-asyncio adds command-line options to pytest:

```bash
# Run with auto mode
pytest --asyncio-mode=auto

# Run with strict mode
pytest --asyncio-mode=strict
```

## Common Patterns

### Testing Async Context Managers

```python
import pytest

@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncResource() as resource:
        result = await resource.operation()
        assert result == "expected"
```

### Testing Async Generators

```python
import pytest

@pytest.mark.asyncio
async def test_async_generator():
    async def async_gen():
        for i in range(3):
            yield i

    results = []
    async for value in async_gen():
        results.append(value)

    assert results == [0, 1, 2]
```

### Async Fixture Dependencies

```python
import pytest_asyncio

@pytest_asyncio.fixture
async def async_connection():
    conn = await create_connection()
    yield conn
    await conn.close()

@pytest_asyncio.fixture
async def async_session(async_connection):
    session = await async_connection.create_session()
    yield session
    await session.close()

@pytest.mark.asyncio
async def test_with_session(async_session):
    result = await async_session.execute("SELECT 1")
    assert result is not None
```

### Module-Scoped Setup

```python
import pytest_asyncio

@pytest_asyncio.fixture(scope="module")
async def database():
    """Expensive database setup shared across module tests"""
    db = await setup_database()
    yield db
    await db.teardown()

@pytest.mark.asyncio(loop_scope="module")
async def test_one(database):
    await database.query("INSERT INTO users VALUES (1, 'Alice')")

@pytest.mark.asyncio(loop_scope="module")
async def test_two(database):
    result = await database.query("SELECT * FROM users")
    assert len(result) == 1
```

## Limitations

### unittest Compatibility

The documentation explicitly notes that "test classes subclassing the standard unittest library are not supported." For unittest-based testing, the documentation recommends either:
- Using `unittest.IsolatedAsyncioTestCase`
- Adopting async frameworks like asynctest

([pytest-asyncio Documentation][1])

### Sequential Execution

Tests run sequentially, not concurrently. If you need concurrent test execution for performance, this must be combined with pytest-xdist for parallel execution across multiple processes.

## Best Practices

### Use Appropriate Loop Scopes

- Use **function scope** (default) for tests that modify shared state
- Use **module or class scope** for expensive setup operations
- Use **session scope** sparingly, only for truly shared resources
- Keep neighboring tests at the same scope level for clarity

### Choose the Right Mode

- Use **auto mode** for asyncio-only test suites to reduce boilerplate
- Use **strict mode** when mixing multiple async frameworks or libraries
- Configure mode globally in pytest.ini rather than per-test

### Fixture Best Practices

- Always use `@pytest_asyncio.fixture` for async fixtures in strict mode
- Properly cleanup resources with yield or finalizers
- Avoid mixing sync and async fixtures when possible
- Use appropriate fixture scopes to minimize overhead

### Error Handling

```python
import pytest

@pytest.mark.asyncio
async def test_async_exception():
    with pytest.raises(ValueError, match="invalid value"):
        await async_function_that_raises()
```

### Testing Timeouts

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_with_timeout():
    async with asyncio.timeout(1.0):  # Python 3.11+
        await slow_operation()
```

Or for earlier Python versions:

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_with_timeout():
    try:
        await asyncio.wait_for(slow_operation(), timeout=1.0)
    except asyncio.TimeoutError:
        pytest.fail("Operation timed out")
```

## Debugging Async Tests

### Enable Asyncio Debug Mode

```bash
PYTHONASYNCIODEBUG=1 pytest tests/
```

### Show Async Warnings

```python
import warnings
import pytest

@pytest.mark.asyncio
async def test_with_warnings():
    warnings.simplefilter("always")
    await potentially_problematic_code()
```

### Use Verbose Output

```bash
pytest -vv --log-cli-level=DEBUG
```

## Integration with Other Tools

### pytest-cov

```bash
pytest --cov=myapp --cov-report=html tests/
```

### pytest-xdist

For parallel execution of async tests:

```bash
pytest -n auto tests/
```

Note: Each worker process gets its own event loop, maintaining test isolation.

## Migration from Older Versions

### From versions < 1.0

If migrating from pre-1.0 versions:

1. Remove any direct usage of the `event_loop` fixture
2. Update `loop_scope` usage - it no longer requires matching pytest collector structure
3. Review fixture scoping - performance improvements may allow broader scopes
4. Test for any assumptions about event loop creation timing

### Legacy Mode (Deprecated)

Legacy mode from older versions is deprecated. Migrate to auto or strict mode:

```ini
# Old (deprecated)
[pytest]
asyncio_mode = legacy

# New (recommended)
[pytest]
asyncio_mode = auto
```

## Version Information

This reference covers pytest-asyncio version 1.2.0, released September 12, 2025. The plugin requires Python 3.9+ and supports Python through 3.14. ([pytest-asyncio PyPI][2])

## References

[1]: https://pytest-asyncio.readthedocs.io/ "pytest-asyncio Documentation"
[2]: https://pypi.org/project/pytest-asyncio/ "pytest-asyncio PyPI"
[3]: https://pytest-asyncio.readthedocs.io/en/stable/concepts.html "pytest-asyncio Concepts"
[4]: https://github.com/pytest-dev/pytest-asyncio "pytest-asyncio GitHub"
[5]: https://pytest-asyncio.readthedocs.io/en/stable/reference/changelog.html "pytest-asyncio Changelog"
