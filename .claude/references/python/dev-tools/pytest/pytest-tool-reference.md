---
title: "pytest Testing Framework Reference"
description: "Comprehensive pytest testing framework guide covering fixtures, parametrization, assertions, and configuration"
type: "tool-reference"
tags: ["pytest", "testing", "python", "fixtures", "tdd", "test-automation", "assertions", "parametrization"]
category: "python"
subcategory: "dev-tools"
version: "8.4"
last_updated: "2025-08-16"
status: "stable"
sources:
  - name: "pytest Documentation"
    url: "https://docs.pytest.org/en/stable/"
  - name: "pytest Reference Guide"
    url: "https://docs.pytest.org/en/stable/reference/reference.html"
  - name: "pytest Fixtures Guide"
    url: "https://docs.pytest.org/en/stable/how-to/fixtures.html"
  - name: "pytest Parametrize Guide"
    url: "https://docs.pytest.org/en/stable/how-to/parametrize.html"
  - name: "pytest Assertions Guide"
    url: "https://docs.pytest.org/en/stable/how-to/assert.html"
  - name: "pytest Configuration Guide"
    url: "https://docs.pytest.org/en/stable/reference/customize.html"
related: ["../mypy/mypy-tool-reference.md", "../astral/ruff/ruff-tool-reference.md"]
author: "unknown"
contributors: []
---

# pytest Testing Framework Reference

pytest is a mature testing framework that makes it easy to write small, readable tests and can scale to support complex functional testing for applications and libraries. ([pytest Documentation][1])

## Overview

pytest enables developers to write concise, readable tests while supporting complex functional testing scenarios. As the documentation states: "The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries." ([pytest Documentation][1])

### System Requirements

- **Python versions**: 3.8+ or PyPy3
- **Installation**: `pip install pytest` or `uv add --dev pytest`

### Key Features

1. **Detailed Assertion Introspection** - Uses plain `assert` statements with comprehensive failure reporting, eliminating the need to memorize assertion method names ([pytest Documentation][1])
2. **Automatic Test Discovery** - Intelligently locates test modules and functions without explicit configuration ([pytest Documentation][1])
3. **Modular Fixtures** - Manages test resources efficiently, supporting parametrization for flexible test organization ([pytest Documentation][1])
4. **Backward Compatibility** - Runs existing unittest and trial test suites seamlessly ([pytest Documentation][1])
5. **Extensive Ecosystem** - Supports over 1,300 external plugins with an active community ([pytest Documentation][1])

## Quick Start

A minimal test demonstrates pytest's simplicity:

```python
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4
```

When executed with `pytest`, pytest provides detailed failure information, showing actual vs. expected values with execution context. ([pytest Documentation][1])

## Assertions

### Basic Assertions

pytest enables developers to verify expectations using Python's standard `assert` statement. When assertions fail, pytest provides detailed introspection showing both the failed condition and relevant variable values. ([pytest Assertions Guide][5])

```python
def test_function():
    assert f() == 4
```

### Assertion Introspection

"Reporting details about a failing assertion is achieved by rewriting assert statements before they are run." This mechanism injects introspection data into failure messages automatically. ([pytest Assertions Guide][5])

### Smart Comparison Reporting

pytest automatically provides context-sensitive output for various data types:

- **Strings**: Shows contextual diff
- **Sequences**: Indicates first failing indices
- **Sets/Dicts**: Highlights differences between collections

([pytest Assertions Guide][5])

### Exception Testing

For validating that code raises specific exceptions, pytest offers the `pytest.raises()` context manager:

```python
import pytest

with pytest.raises(ZeroDivisionError):
    1 / 0
```

To capture exception details, use the `as` syntax:

```python
with pytest.raises(RuntimeError) as excinfo:
    problematic_code()
assert "expected message" in str(excinfo.value)
```

The `ExceptionInfo` object provides access to `.type`, `.value`, and `.traceback` attributes. ([pytest Assertions Guide][5])

### Exception Message Matching

The `match` parameter accepts regular expressions to validate error messages: "The match parameter is matched with the re.search() function, so partial patterns work effectively." ([pytest Assertions Guide][5])

```python
with pytest.raises(ValueError, match=r"invalid.*value"):
    raise ValueError("invalid input value")
```

### Exception Groups (Python 3.11+)

For Python 3.11+ exception groups, `pytest.RaisesGroup` provides structured testing:

```python
with pytest.RaisesGroup(ValueError):
    raise ExceptionGroup("group msg", [ValueError("value msg")])
```

([pytest Assertions Guide][5])

## Fixtures

Fixtures in pytest are reusable setup functions that provide test dependencies. When a test function declares a fixture as a parameter, pytest automatically executes that fixture and passes its return value to the test. ([pytest Fixtures Guide][3])

### Basic Fixture Definition

Test functions "request" fixtures by including them as function parameters. pytest matches parameter names to fixture names and executes the fixture before running the test. ([pytest Fixtures Guide][3])

```python
import pytest

@pytest.fixture
def database():
    db = create_database()
    return db

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Fixture Scopes

Fixtures support five scope levels, determining when they're created and destroyed:

- **function** (default): Created and destroyed per test function
- **class**: Persists through all test methods in a class
- **module**: Shared across all tests in a module
- **package**: Shared across packages and subpackages
- **session**: Exists for the entire test session

([pytest Fixtures Guide][3])

```python
@pytest.fixture(scope="session")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### Fixture Dependencies

Fixtures can depend on other fixtures. A fixture may request another fixture as a parameter, creating a dependency chain that pytest resolves automatically. ([pytest Fixtures Guide][3])

```python
@pytest.fixture
def db_connection():
    return create_connection()

@pytest.fixture
def db_session(db_connection):
    session = db_connection.create_session()
    yield session
    session.close()
```

### Autouse Fixtures

Fixtures decorated with `@pytest.fixture(autouse=True)` execute automatically for all tests in their scope—no explicit request needed. This reduces redundant fixture declarations. ([pytest Fixtures Guide][3])

```python
@pytest.fixture(autouse=True)
def reset_database():
    database.reset()
```

### Teardown and Cleanup

#### Yield Fixtures (Recommended)

Modern pytest favors yield fixtures for cleanup:

```python
@pytest.fixture
def resource():
    setup_code()
    yield resource_object
    teardown_code()
```

Code before `yield` executes during setup; code after executes during teardown. pytest manages the order: fixtures teardown in reverse order of their execution. ([pytest Fixtures Guide][3])

#### Finalizers (Alternative)

The `request.addfinalizer()` method adds cleanup functions directly:

```python
@pytest.fixture
def resource(request):
    obj = create_object()
    request.addfinalizer(lambda: cleanup(obj))
    return obj
```

Finalizers execute in LIFO order (last registered, first executed). ([pytest Fixtures Guide][3])

### Parametrized Fixtures

Use `@pytest.fixture(params=[...])` to run dependent tests multiple times with different fixture values:

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    return create_database(request.param)

def test_database_query(database):
    # This test runs three times, once for each database
    result = database.query("SELECT 1")
    assert result is not None
```

Custom test IDs can be specified via the `ids` parameter. ([pytest Fixtures Guide][3])

### Factory Fixtures

Return a callable instead of data directly. This pattern enables generating multiple test objects with flexible parameters:

```python
@pytest.fixture
def user_factory():
    def _make_user(name):
        return {"name": name, "orders": []}
    return _make_user

def test_user_creation(user_factory):
    user1 = user_factory("Alice")
    user2 = user_factory("Bob")
    assert user1["name"] != user2["name"]
```

([pytest Fixtures Guide][3])

### conftest.py

Place shared fixtures in `conftest.py` files. pytest automatically discovers fixtures in conftest files at the current and parent directory levels, making them available to all tests in that scope. ([pytest Fixtures Guide][3])

```
tests/
  conftest.py          # Shared fixtures for all tests
  test_module1.py
  subdir/
    conftest.py        # Additional fixtures for subdir tests
    test_module2.py
```

### Best Practices

- Prefer yield fixtures over finalizers for clearer code
- Structure fixtures atomically—one responsibility per fixture
- Use appropriate scopes to minimize active resources
- Leverage autouse fixtures to reduce boilerplate
- Keep fixture definitions in conftest.py for discoverability
- Use factories when tests need multiple instances of similar objects

([pytest Fixtures Guide][3])

## Parametrization

pytest supports parametrization at multiple levels to run tests with multiple argument sets. ([pytest Parametrize Guide][4])

### @pytest.mark.parametrize Decorator

This is the primary method for running tests with multiple argument sets. As the docs state: "The builtin pytest.mark.parametrize decorator enables parametrization of arguments for a test function." ([pytest Parametrize Guide][4])

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 54),
])
def test_eval(input, expected):
    assert eval(input) == expected
```

This approach creates separate test instances for each parameter tuple, with individual reporting of results. ([pytest Parametrize Guide][4])

### Stacking Parametrization

Multiple `@parametrize` decorators create cartesian products of parameters:

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    # Runs 4 times: (0,2), (0,3), (1,2), (1,3)
    pass
```

([pytest Parametrize Guide][4])

### Marking Individual Parameters

Wrap specific parameter sets with `pytest.param()` to apply marks like `xfail`:

```python
@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    pytest.param("6*9", 42, marks=pytest.mark.xfail),
])
def test_eval(input, expected):
    assert eval(input) == expected
```

([pytest Parametrize Guide][4])

### Module-Level Parametrization

Use the `pytestmark` variable to apply parametrization across entire modules:

```python
import pytest

pytestmark = pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
])

def test_eval(input, expected):
    assert eval(input) == expected

def test_eval_squared(input, expected):
    assert eval(input) ** 2 == expected ** 2
```

([pytest Parametrize Guide][4])

### Important Behavior Note

Parameters are passed directly without copying—mutations affect subsequent test instances: "Parameter values are passed as-is to tests (no copy whatsoever)." ([pytest Parametrize Guide][4])

## Built-in Fixtures

pytest provides several built-in fixtures for common testing needs. ([pytest Reference Guide][2])

### Capturing Output

**`capsys`** – Captures `sys.stdout` and `sys.stderr` as text:

```python
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

**`capfd`** – Captures file descriptors 1 and 2 as text

**`capfdbinary`** – Captures file descriptors 1 and 2 as bytes

([pytest Reference Guide][2])

### Logging

**`caplog`** – Accesses captured logging with properties: `messages`, `text`, `records`, `record_tuples`:

```python
def test_logging(caplog):
    logger.info("test message")
    assert "test message" in caplog.text
```

([pytest Reference Guide][2])

### Temporary Paths

**`tmp_path`** – Provides temporary directory per test as a `pathlib.Path`:

```python
def test_file_creation(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")
    assert file.read_text() == "content"
```

([pytest Reference Guide][2])

### Monkeypatching

**`monkeypatch`** – Temporarily modifies attributes, environment variables, and sys.path; automatically undone after tests:

```python
def test_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert os.environ["API_KEY"] == "test-key"
```

([pytest Reference Guide][2])

### Configuration Access

**`pytestconfig`** – Session-scoped access to the `pytest.Config` object

**`request`** – Provides access to the requesting test context, markers, and fixture parameters

([pytest Reference Guide][2])

## Markers

pytest markers are decorators that add metadata to test functions. ([pytest Reference Guide][2])

### Common Markers

**`@pytest.mark.skip(reason)`** – Unconditionally skips a test:

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass
```

**`@pytest.mark.skipif(condition, reason)`** – Conditionally skips based on boolean or string conditions:

```python
import sys

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_syntax():
    pass
```

**`@pytest.mark.xfail(condition, reason, raises, strict)`** – Marks expected failures; `strict=True` fails if test unexpectedly passes:

```python
@pytest.mark.xfail(reason="Known bug #123")
def test_buggy_feature():
    assert False
```

**`@pytest.mark.usefixtures(*names)`** – Applies named fixtures to test functions without receiving their return values:

```python
@pytest.mark.usefixtures("database", "reset_cache")
def test_operation():
    # database and reset_cache fixtures run before this test
    pass
```

**`@pytest.mark.filterwarnings(filter)`** – Adds warning filters using Python's warning specification syntax:

```python
@pytest.mark.filterwarnings("ignore:deprecated")
def test_legacy_code():
    use_deprecated_function()
```

([pytest Reference Guide][2])

### Custom Markers

Register custom markers in `pytest.ini` or `pyproject.toml`:

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

Apply custom markers to tests:

```python
@pytest.mark.slow
def test_complex_operation():
    pass
```

Run specific marker groups:

```bash
pytest -m slow           # Run only slow tests
pytest -m "not slow"     # Skip slow tests
pytest -m "slow and integration"  # Logical combinations
```

([pytest Reference Guide][2])

## Configuration

pytest supports multiple configuration file formats, checked in this order: ([pytest Configuration Guide][6])

### Configuration File Formats

1. **pytest.ini** - Takes precedence, even when empty. Can use `.pytest.ini` as a hidden alternative.

2. **pyproject.toml** - Uses `[tool.pytest.ini_options]` table (added in version 6.0):

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
]
pythonpath = [
    "src",
]
```

3. **tox.ini** - Requires a `[pytest]` section to be recognized.

4. **setup.cfg** - Requires a `[tool:pytest]` section. "Usage of setup.cfg is not recommended unless for very simple use cases" due to parser differences. ([pytest Configuration Guide][6])

### Common Configuration Options

```ini
[pytest]
# Minimum pytest version
minversion = 8.0

# Test discovery patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Directories to search for tests
testpaths = tests

# Additional command-line options
addopts = -ra -q --strict-markers

# Registered markers
markers =
    slow: marks tests as slow
    integration: marks tests requiring external services

# Ignore directories during collection
norecursedirs = .git .tox dist build

# Timeout for tests
timeout = 300
```

### Root Directory Discovery

The `rootdir` determines:
- Node ID construction for tests
- Location for plugins to store project-specific data (like pytest's `.pytest_cache`)

The discovery algorithm checks for configuration files in ancestor directories, starting from the common ancestor of specified test paths. As noted: "rootdir is NOT used to modify sys.path/PYTHONPATH or influence how modules are imported." ([pytest Configuration Guide][6])

## Command-Line Usage

### Basic Commands

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run tests matching pattern
pytest -k "test_user"

# Run tests with specific marker
pytest -m slow

# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=2

# Run last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff

# Show local variables in tracebacks
pytest -l

# Increase verbosity
pytest -v

# Show summary info for all tests
pytest -ra

# Quiet mode (less output)
pytest -q

# Show print statements
pytest -s
```

### Useful Options

```bash
# Collect tests without running them
pytest --collect-only

# Show available fixtures
pytest --fixtures

# Show available markers
pytest --markers

# Generate coverage report
pytest --cov=src --cov-report=html

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run with specific Python warnings
pytest -W ignore::DeprecationWarning

# Generate JUnit XML report
pytest --junitxml=report.xml
```

## API Reference

### Key Functions

**`pytest.approx()`** – Compares floating-point numbers within specified tolerances (relative: 1e-6, absolute: 1e-12 by default). Supports sequences, numpy arrays, and dictionaries:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
```

**`pytest.fail(reason)`** – Explicitly fails a test with an optional message

**`pytest.skip(reason)`** – Skips test execution; allows module-level skipping with `allow_module_level=True`

**`pytest.importorskip(modname)`** – Imports a module or skips the test if import fails; supports version checking:

```python
numpy = pytest.importorskip("numpy", minversion="1.20")
```

**`pytest.xfail(reason)`** – Marks a test as expected to fail

**`pytest.exit(reason)`** – Terminates the testing process with optional return code

**`pytest.main(args, plugins)`** – Executes pytest programmatically within Python code:

```python
retcode = pytest.main(["-x", "tests/"])
```

**`pytest.warns()`** – Asserts that code produces specific warning types; re-emits unmatched warnings since v8.0:

```python
with pytest.warns(UserWarning, match="deprecated"):
    use_deprecated_function()
```

**`pytest.deprecated_call()`** – Verifies code triggers deprecation, pending deprecation, or future warnings

([pytest Reference Guide][2])

### Key Constants

**`pytest.__version__`** – Returns the current pytest version as a string (e.g., '8.4.0')

**`pytest.version_tuple`** – Provides version as a tuple format

**`pytest.HIDDEN_PARAM`** – (Added v8.4) Hides parameter sets from test names when passed to `ids` or `id` parameters

([pytest Reference Guide][2])

## Plugins and Extension

pytest has an extensive plugin ecosystem with over 1,300 external plugins. ([pytest Documentation][1])

### Installing Plugins

```bash
pip install pytest-cov          # Coverage reporting
pip install pytest-xdist         # Parallel test execution
pip install pytest-mock          # Enhanced mocking
pip install pytest-asyncio       # Async test support
pip install pytest-timeout       # Test timeout enforcement
pip install pytest-benchmark    # Performance benchmarking
```

### Writing Custom Plugins

Create plugins using hooks in `conftest.py`:

```python
def pytest_configure(config):
    """Called after command line options are parsed"""
    config.addinivalue_line("markers", "custom: custom marker")

def pytest_collection_modifyitems(config, items):
    """Modify collected test items"""
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(pytest.mark.timeout(300))
```

### Hook Specifications

pytest provides numerous hooks for customization:

- `pytest_configure` - Configuration setup
- `pytest_collection_modifyitems` - Modify test collection
- `pytest_runtest_setup` - Test setup phase
- `pytest_runtest_call` - Test execution phase
- `pytest_runtest_teardown` - Test teardown phase
- `pytest_assertrepr_compare` - Custom assertion messages

([pytest Documentation][1])

## Best Practices

### Test Organization

```
project/
  src/
    myapp/
      __init__.py
      module.py
  tests/
    conftest.py          # Shared fixtures
    test_module.py       # Tests for module.py
    integration/
      conftest.py        # Integration-specific fixtures
      test_api.py
```

### Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*` (without `__init__` method)
- Test methods in classes: `test_*`

### Writing Effective Tests

1. **Use descriptive test names**: `test_user_login_with_invalid_credentials`
2. **One assertion per test**: Focus on single behavior
3. **Arrange-Act-Assert pattern**: Structure tests clearly
4. **Use fixtures for setup/teardown**: Keep tests clean
5. **Parametrize for multiple cases**: Avoid test duplication
6. **Use appropriate markers**: Categorize tests for selective execution

### Performance Tips

- Use appropriate fixture scopes to minimize setup/teardown overhead
- Run tests in parallel with pytest-xdist: `pytest -n auto`
- Use `--lf` and `--ff` flags to focus on failing tests during development
- Skip slow tests during rapid development: `pytest -m "not slow"`

### Debugging Tests

```bash
# Drop into debugger on failures
pytest --pdb

# Drop into debugger at test start
pytest --trace

# Show local variables in tracebacks
pytest -l

# Increase verbosity for more context
pytest -vv

# Show print statements and logging
pytest -s --log-cli-level=INFO
```

## Version Information

This reference covers pytest version 8.4 features. The documentation notes that pytest maintains backward compatibility and supports Python 3.8+. ([pytest Documentation][1])

## References

[1]: https://docs.pytest.org/en/stable/ "pytest Documentation"
[2]: https://docs.pytest.org/en/stable/reference/reference.html "pytest Reference Guide"
[3]: https://docs.pytest.org/en/stable/how-to/fixtures.html "pytest Fixtures Guide"
[4]: https://docs.pytest.org/en/stable/how-to/parametrize.html "pytest Parametrize Guide"
[5]: https://docs.pytest.org/en/stable/how-to/assert.html "pytest Assertions Guide"
[6]: https://docs.pytest.org/en/stable/reference/customize.html "pytest Configuration Guide"
