---
title: "mypy: Static Type Checker for Python"
description: "Static type checker that catches bugs before runtime using type hints"
type: "tool-reference"
tags: ["python", "type-checker", "static-analysis", "type-hints", "pep-484", "gradual-typing", "code-quality", "testing"]
category: "dev-tools"
subcategory: "python"
version: "1.13"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "mypy Official Documentation"
    url: "https://mypy.readthedocs.io/en/stable/"
  - name: "mypy Getting Started"
    url: "https://mypy.readthedocs.io/en/stable/getting_started.html"
  - name: "mypy Type Inference and Annotations"
    url: "https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html"
  - name: "mypy Configuration File"
    url: "https://mypy.readthedocs.io/en/stable/config_file.html"
  - name: "mypy Command Line"
    url: "https://mypy.readthedocs.io/en/stable/command_line.html"
  - name: "mypy Running Guide"
    url: "https://mypy.readthedocs.io/en/stable/running_mypy.html"
  - name: "mypy Common Issues"
    url: "https://mypy.readthedocs.io/en/stable/common_issues.html"
  - name: "mypy Error Codes"
    url: "https://mypy.readthedocs.io/en/stable/error_codes.html"
  - name: "mypy Existing Code"
    url: "https://mypy.readthedocs.io/en/stable/existing_code.html"
  - name: "mypy Protocols"
    url: "https://mypy.readthedocs.io/en/stable/protocols.html"
related: ["../astral/ruff/ruff-tool-reference.md"]
author: "unknown"
contributors: []
---

# mypy: Static Type Checker for Python

mypy is a static type checker for Python that helps developers catch bugs before runtime. ([mypy Documentation][1]) The tool analyzes code without executing it to identify type-related errors using type hints added via PEP 484 syntax.

## Overview

mypy examines type hints in Python code to detect type-related errors during development rather than at runtime. ([mypy Documentation][1]) Type hints function similarly to comments and don't interfere with normal program execution—you can still run code through the Python interpreter even if mypy reports errors. ([mypy Documentation][1])

### Key Characteristics

**Gradual Typing**: mypy embraces gradual typing, allowing developers to incrementally add type hints to existing codebases. You can mix typed and untyped code, making adoption flexible for projects of any size. ([mypy Documentation][1])

**Static Analysis**: mypy performs type checking without executing code, enabling early bug detection during development.

**PEP 484 Compatibility**: Follows Python's official type hinting standard (PEP 484) ensuring compatibility with other type-aware tools.

## Core Features

### Type System Capabilities

mypy's type system includes several powerful features:

- **Type inference**: Reduces annotation requirements by automatically deducing types
- **Generic types**: Enables flexible, reusable code patterns
- **Union and Optional types**: Supports nullable and multi-type values
- **Structural subtyping and protocols**: Enables duck typing compatibility
- **Callable types**: Defines function signatures
- **Tuple types**: Represents fixed-length sequences

([mypy Documentation][1])

### Use Cases

mypy suits multiple scenarios:
- Catching errors in new code before deployment
- Gradually typing existing Python projects
- Improving code documentation and maintainability
- Enabling IDE features like autocompletion and refactoring

([mypy Documentation][1])

## Installation

mypy requires Python 3.9 or later. ([mypy Getting Started][2])

### Using pip

```bash
python3 -m pip install mypy
```

([mypy Getting Started][2])

### Using uv

```bash
# Global installation
uv tool install mypy

# Project-specific
uv add --dev mypy
```

### Using other package managers

```bash
# pipx
pipx install mypy

# Conda
conda install -c conda-forge mypy
```

## Getting Started

### Basic Usage

Once installed, run mypy on a Python file to perform static type checking:

```bash
mypy program.py
```

This command makes mypy type check your `program.py` file and print out any errors it finds without executing the code. ([mypy Getting Started][2])

### Adding Type Annotations

Functions without annotations are treated as dynamically typed and receive minimal checking by default. ([mypy Getting Started][2])

To enable checking, annotate function parameters and return types:

```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```

([mypy Getting Started][2])

### Complex Types

Use generic types like `list[str]` or `Iterable[str]` for more expressive annotations. The `typing` module provides additional type constructs, including union types (`int | str`). ([mypy Getting Started][2])

### First Run

```bash
# Basic check
mypy program.py

# Strict mode
mypy --strict program.py

# Check specific module
mypy -m mymodule

# Check package recursively
mypy -p mypackage
```

## Type Inference and Annotations

### Automatic Type Inference

mypy automatically determines variable types based on initial assignments. For example, assigning `1` to a variable infers it as `int`, and `[1, 2]` becomes `list[int]`. ([mypy Type Inference][3])

**Important limitation**: mypy will not use type inference in dynamically typed functions (those without a function type annotation)—every local variable defaults to `Any` in unchecked functions. ([mypy Type Inference][3])

### Explicit Type Annotations

You can override inferred types using annotations:

```python
x: int | str = 1
```

This sets the variable's type to the broader union rather than just `int`. mypy validates that assigned values match the declared type, rejecting incompatible assignments. ([mypy Type Inference][3])

### Collections and Context

Empty collections require explicit type hints since mypy cannot infer their element types:

```python
l: list[int] = []
d: dict[str, int] = {}
```

([mypy Type Inference][3])

mypy uses **bidirectional type inference**, considering context from assignment targets. When assigning `[1, 2]` to a variable typed as `list[object]`, mypy infers the expression as `list[object]` rather than `list[int]`. ([mypy Type Inference][3])

### Silencing Errors

Use `# type: ignore` comments to suppress specific type errors, optionally with error codes:

```python
app.run(8000)  # type: ignore[arg-type]
```

You can also disable checking file-wide, per-module, or using the `@typing.no_type_check` decorator. ([mypy Type Inference][3])

## Configuration

### Configuration File Discovery

mypy locates configuration files by searching upward through the filesystem hierarchy. The search order is:

1. `mypy.ini`
2. `.mypy.ini`
3. `pyproject.toml` (with `[tool.mypy]` section)
4. `setup.cfg` (with `[mypy]` section)

If none are found locally, mypy checks `$XDG_CONFIG_HOME/mypy/config`, `~/.config/mypy/config`, and `~/.mypy.ini`. ([mypy Configuration][4])

The `--config-file` command-line flag overrides all other discovery methods. ([mypy Configuration][4])

### Configuration Structure

The configuration uses INI format with:
- A required `[mypy]` section for global settings
- Optional `[mypy-PATTERN]` sections for module-specific overrides using fully-qualified names with wildcard support (e.g., `foo.bar.*`)

([mypy Configuration][4])

**Important**: There is no merging of configuration files, as it would lead to ambiguity. ([mypy Configuration][4])

### Example Configuration (mypy.ini)

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-third_party.*]
ignore_missing_imports = True
```

### Example Configuration (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

Boolean values must be lowercase in TOML format. ([mypy Configuration][4])

### Key Configuration Categories

**Import Discovery**: `mypy_path`, `files`, `modules`, `packages`, `exclude`

**Platform Settings**: `python_version`, `platform`, `always_true`, `always_false`

**Type Checking Strictness**: `disallow_any_unimported`, `disallow_untyped_calls`, `disallow_untyped_defs`, `strict_optional`

**Error Handling**: `ignore_errors`, `warn_return_any`, `warn_unused_ignores`, `warn_unreachable`

**Caching**: `incremental`, `cache_dir`, `sqlite_cache`

([mypy Configuration][4])

## Command-Line Interface

### Core Usage

Basic invocation specifies files or directories to check:

```bash
mypy foo.py bar.py some_directory
```

([mypy Command Line][5])

### Specifying Code to Check

**Module checking:**
```bash
mypy -m MODULE
```

**Package checking (recursive):**
```bash
mypy -p PACKAGE
```

**Inline code:**
```bash
mypy -c "def foo(x: int) -> int: return x + 1"
```

**File lists:**
```bash
mypy @file_of_files.txt
```

**Exclusion:**
```bash
mypy --exclude 'vendor|build' .
```

([mypy Command Line][5])

### Configuration Options

**Custom config file:**
```bash
mypy --config-file custom.ini
```

**Warn about unused config:**
```bash
mypy --warn-unused-configs
```

([mypy Command Line][5])

### Import Handling

**Follow imports behavior:**
```bash
mypy --follow-imports {normal,silent,skip,error}
```

**Ignore missing imports:**
```bash
mypy --ignore-missing-imports
```

**Specify Python executable:**
```bash
mypy --python-executable /path/to/python
```

([mypy Command Line][5])

### Type Checking Strictness

**Comprehensive checking:**
```bash
mypy --strict
```

**Specific strictness flags:**
```bash
mypy --disallow-untyped-calls
mypy --disallow-untyped-defs
mypy --disallow-any-expr
```

([mypy Command Line][5])

### Platform & Version

**Target Python version:**
```bash
mypy --python-version 3.11
```

**Target platform:**
```bash
mypy --platform linux
```

([mypy Command Line][5])

### Error Display

**Show error context:**
```bash
mypy --show-error-context
```

**Column numbers:**
```bash
mypy --show-column-numbers
```

**Pretty output:**
```bash
mypy --pretty
```

**Hide error codes:**
```bash
mypy --hide-error-codes
```

([mypy Command Line][5])

### Performance

**Disable incremental caching:**
```bash
mypy --no-incremental
```

**Custom cache directory:**
```bash
mypy --cache-dir .mypy_cache
```

([mypy Command Line][5])

### Reports

mypy can generate HTML, XML, Cobertura, and coverage reports. ([mypy Command Line][5])

## Running mypy

### Execution Modes

mypy supports several ways to specify what code to type check:

1. **File/Directory paths**: `mypy file_1.py foo/file_2.py some/directory`
2. **Module specification**: `mypy -m html.parser`
3. **Package recursion**: `mypy -p package_name`
4. **Inline code**: `mypy -c "code string"`
5. **File lists**: `mypy @file_of_files.txt`

([mypy Running Guide][6])

### Import Handling Strategies

When mypy encounters imports, it can produce three outcomes:

- **Unable to follow**: Module doesn't exist or lacks type hints
- **Follows but shouldn't**: Module is type checked when you didn't want it
- **Ideal case**: Module is successfully followed and type checked

([mypy Running Guide][6])

### Error Reporting for Imports

Three main error categories occur with missing imports:

- **Missing library stubs**: "Skipping analyzing X: module is installed, but missing library stubs or py.typed marker"
- **Uninstalled stubs**: "Library stubs not installed for [module]"
- **Module not found**: "Cannot find implementation or library stub for module named [module]"

([mypy Running Guide][6])

### Follow-Imports Configuration

The `--follow-imports` flag accepts four values:

- **normal** (default): Checks all top-level code and annotated functions
- **silent**: Identical to normal but suppresses error messages
- **skip**: Replaces modules with `Any` type without following imports
- **error**: Same as skip but flags imports as errors

The documentation recommends the default behavior for new codebases and advises against using `skip` unless absolutely necessary. ([mypy Running Guide][6])

### Third-Party Library Support

For libraries without built-in type hints, install stub packages (typically named `types-<distribution>`) to provide type information. ([mypy Getting Started][2])

```bash
# Install stubs for requests
pip install types-requests

# With uv
uv add --dev types-requests
```

## Error Codes

### Purpose

mypy error codes serve two primary functions: they enable targeted error suppression and provide documentation references. ([mypy Error Codes][8])

### Suppression Methods

**Line-level suppression:**
```python
from foolib import foo  # type: ignore[attr-defined]
```

**Multiple error codes:**
```python
x = foo()  # type: ignore[no-untyped-call, misc]
```

**Global configuration:**
```bash
mypy --enable-error-code=truthy-bool
mypy --disable-error-code=misc
```

**Module-specific rules:**
```ini
[mypy-tests.*]
disable_error_code = no-untyped-def
```

([mypy Error Codes][8])

### Configuration Hierarchy

mypy applies error code settings through this priority chain:

1. Global settings (command line and main config section)
2. Module-specific adjustments (config sections for particular modules)
3. File-level inline comments (`# mypy: enable-error-code="..."`)

([mypy Error Codes][8])

### Requiring Error Codes

You can enforce that `type: ignore` comments include specific error codes using the `ignore-without-code` setting. ([mypy Error Codes][8])

## Common Issues and Solutions

### Undetected Errors

Functions without type annotations bypass checking entirely. Functions that do not have any annotations are not type-checked, and even the most blatant type errors pass silently. ([mypy Common Issues][7])

**Solution**: Add annotations or use the `--check-untyped-defs` flag. ([mypy Common Issues][7])

### Type Inference Problems

When variables have `Any` type (often from untyped imports or the `--ignore-missing-imports` flag), type safety erodes. ([mypy Common Issues][7])

**Solution**: Avoid broad ignore flags in favor of per-module settings. ([mypy Common Issues][7])

### Performance Concerns

Slow mypy runs can be addressed through the mypy daemon, which offers "a factor of 10 or more" speedup for incremental checks. ([mypy Common Issues][7])

As of mypy 1.13, using the orjson library via `mypy[faster-cache]` improves cache performance. ([mypy Common Issues][7])

```bash
pip install mypy[faster-cache]
```

### Practical Workarounds

**Local suppression**: Use `# type: ignore` comments or `# type: ignore[error_code]` for specific issues

**Collection typing**: Always annotate empty lists/dicts with explicit types like `list[int]`

**Type narrowing**: Leverage `isinstance()` checks or assertions to refine types within conditional blocks

**Platform awareness**: Use `sys.version_info` and `sys.platform` checks for version-specific code paths

([mypy Common Issues][7])

### Debugging Type Inference

Use `reveal_type()` to inspect inferred types during development:

```python
reveal_type(x)  # Reveals type of x
```

This helps debug complex type inference scenarios. ([mypy Common Issues][7])

## Protocols and Structural Subtyping

### Core Concepts

mypy supports two approaches to type compatibility:

**Nominal subtyping** relies on class hierarchy. If class `Dog` inherits class `Animal`, it's a subtype of `Animal`. ([mypy Protocols][10]) This is Python's predominant approach and matches how `isinstance()` works.

**Structural subtyping** bases compatibility on available operations. Class `Dog` is a structural subtype of class `Animal` if the former has all attributes and methods of the latter, and with compatible types. ([mypy Protocols][10]) This mirrors duck typing, which is familiar to Python developers.

### Defining Protocols

Create custom protocols by inheriting from `Protocol`:

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...
```

Any class with a compatible `close()` method qualifies as a `SupportsClose` subtype—no explicit inheritance needed. ([mypy Protocols][10]) This enables flexible, interface-based design.

### Key Features

- **Predefined protocols** exist in `collections.abc` and `typing` (like `Iterable[T]`, `Iterator[T]`, `Sized`)
- **Subprotocols** can extend existing protocols through inheritance
- **Recursive protocols** support self-referential structures like trees
- **Runtime checking** via `@runtime_checkable` decorator enables `isinstance()` with protocols
- **Callback protocols** define complex function signatures using `__call__`

([mypy Protocols][10])

### Example: Callback Protocol

```python
from typing import Protocol

class Combiner(Protocol):
    def __call__(self, *vals: bytes, maxlen: int | None = None) -> list[bytes]: ...

def batch_proc(data: Iterable[bytes], cb_results: Combiner) -> bytes:
    for item in data:
        ...
```

### Runtime Checking

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

if isinstance(Circle(), Drawable):
    print("Circle is drawable")
```

## Adding mypy to Existing Codebases

### Migration Approaches

**Start Small and Incremental**: Rather than attempting comprehensive type checking immediately, pick a subset of your codebase (say, 5,000 to 50,000 lines) and get mypy to run successfully only on this subset at first, before adding annotations. ([mypy Existing Code][9])

**Phased Strictness**: Begin with basic error suppression using `# type: ignore` comments, then gradually progress toward stricter configurations. The guide suggests eventually targeting `mypy --strict` as an ideal endpoint. ([mypy Existing Code][9])

### Key Best Practices

**1. Standardized Execution**: Ensure consistent mypy invocation across your team by checking configuration files into your repository and pinning the mypy version in development requirements. ([mypy Existing Code][9])

**2. Selective Module Checking**: Use per-module configuration to ignore errors in modules not yet ready for type checking, leveraging the `ignore_errors` setting for specific packages. ([mypy Existing Code][9])

**3. Strategic Annotation Priorities**: Focus early annotation efforts on widely-imported modules like utilities and model classes, maximizing downstream type-checking benefits. ([mypy Existing Code][9])

**4. Continuous Integration**: Integrate mypy into your CI pipeline immediately to prevent regression of new type errors. ([mypy Existing Code][9])

**5. Gradual Coverage Growth**: Establish coding conventions requiring annotations for new code and encouraging them during modifications to existing code. ([mypy Existing Code][9])

**6. Automation Support**: Consider tools like MonkeyType or PyAnnotate to generate draft annotations from runtime data or static analysis. ([mypy Existing Code][9])

**7. Performance Optimization**: Utilize mypy daemon for faster incremental checking, especially for projects exceeding 100,000 lines. ([mypy Existing Code][9])

### Example Migration Configuration

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True

# Gradually enable strict checking
disallow_untyped_defs = False  # Start False, enable later

# Ignore legacy modules
[mypy-legacy.*]
ignore_errors = True

# Allow missing imports for third-party without stubs
[mypy-third_party.*]
ignore_missing_imports = True
```

## Best Practices

### Project Setup

**1. Add mypy as a dev dependency:**
```bash
uv add --dev mypy
```

**2. Create configuration file:**
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**3. Add to CI/CD:**
```yaml
# GitHub Actions example
- name: Type check with mypy
  run: uv run mypy .
```

### Type Annotation Strategy

**Start with public APIs:**
- Annotate function signatures first
- Add type hints to class attributes
- Progressively add internal annotations

**Use type aliases for clarity:**
```python
from typing import TypeAlias

UserId: TypeAlias = int
UserName: TypeAlias = str

def get_user(user_id: UserId) -> UserName:
    ...
```

**Leverage generics:**
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()
```

### Performance Optimization

**Enable incremental mode** (default):
```ini
[mypy]
incremental = True
cache_dir = .mypy_cache
```

**Use mypy daemon for large projects:**
```bash
dmypy run -- program.py
```

**Install faster-cache for improved performance:**
```bash
pip install mypy[faster-cache]
```

### CI/CD Integration

**Recommended workflow:**
```bash
# Fail on type errors
mypy --strict src/

# Generate reports
mypy --html-report mypy-report src/
```

**Pre-commit hook:**
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## Common Workflows

### Development Workflow

```bash
# Quick check during development
mypy changed_file.py

# Full project check
mypy .

# Watch mode with daemon
dmypy run -- .
```

### CI Workflow

```bash
# Fail if any type errors
mypy --strict src/

# Generate coverage report
mypy --html-report htmlcov --cobertura-xml-report coverage.xml src/
```

### Pre-commit Workflow

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies:
          - types-requests
          - types-pyyaml
```

## IDE Integration

### VS Code

Install the Pylance extension which includes mypy integration:

```json
{
  "python.linting.mypyEnabled": true,
  "python.linting.enabled": true
}
```

### PyCharm

PyCharm has built-in type checking. Enable mypy plugin for additional checks:
- Install "Mypy" plugin from marketplace
- Configure in Settings → Tools → Mypy

### Vim/Neovim

Use ALE or coc.nvim with mypy:

```vim
let g:ale_linters = {'python': ['mypy']}
```

## Troubleshooting

### Common Issues

**"Cannot find implementation or library stub":**
- Install type stubs: `pip install types-<package>`
- Add to `mypy.ini`: `ignore_missing_imports = True`

**"Incompatible types in assignment":**
- Check variable type annotations
- Use `reveal_type()` to debug inference
- Consider using union types or type guards

**Slow performance:**
- Use mypy daemon: `dmypy run`
- Install faster-cache: `pip install mypy[faster-cache]`
- Check cache directory permissions

**False positives:**
- Use `# type: ignore[error-code]` for specific suppressions
- Consider using `assert` for type narrowing
- Use `cast()` when you know better than mypy

### Debugging Commands

**Reveal inferred types:**
```python
reveal_type(variable)  # Shows inferred type
```

**Show configuration:**
```bash
mypy --show-config program.py
```

**Verbose output:**
```bash
mypy -v program.py
```

**Clear cache:**
```bash
rm -rf .mypy_cache
```

### Resources

- Official documentation: https://mypy.readthedocs.io/
- GitHub repository: https://github.com/python/mypy
- Type stub packages: https://github.com/python/typeshed
- Community Gitter chat: https://gitter.im/python/typing

## Python Version Support

mypy requires Python 3.9 or later for installation. ([mypy Getting Started][2]) It can check code targeting older Python versions using the `--python-version` flag.

## Advanced Features

### mypy Daemon (dmypy)

For large projects, use the mypy daemon for faster incremental checks:

```bash
# Start daemon and run check
dmypy run -- program.py

# Subsequent runs (much faster)
dmypy run -- program.py

# Stop daemon
dmypy stop

# Restart daemon
dmypy restart
```

The daemon offers "a factor of 10 or more" speedup for incremental checks. ([mypy Common Issues][7])

### Stub Files

Create stub files (`.pyi`) for gradual typing without modifying source code:

```python
# mymodule.pyi
def process(data: str) -> int: ...

class MyClass:
    def method(self, x: int) -> str: ...
```

### Type Aliases

Create reusable type definitions:

```python
from typing import TypeAlias

Vector: TypeAlias = list[float]
ConnectionOptions: TypeAlias = dict[str, str | int]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]
```

### Literal Types

Restrict values to specific literals:

```python
from typing import Literal

Mode = Literal["r", "w", "a"]

def open_file(path: str, mode: Mode) -> None:
    ...
```

## References

[1]: https://mypy.readthedocs.io/en/stable/ "mypy Official Documentation"
[2]: https://mypy.readthedocs.io/en/stable/getting_started.html "mypy Getting Started"
[3]: https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html "mypy Type Inference and Annotations"
[4]: https://mypy.readthedocs.io/en/stable/config_file.html "mypy Configuration File"
[5]: https://mypy.readthedocs.io/en/stable/command_line.html "mypy Command Line"
[6]: https://mypy.readthedocs.io/en/stable/running_mypy.html "mypy Running Guide"
[7]: https://mypy.readthedocs.io/en/stable/common_issues.html "mypy Common Issues"
[8]: https://mypy.readthedocs.io/en/stable/error_codes.html "mypy Error Codes"
[9]: https://mypy.readthedocs.io/en/stable/existing_code.html "mypy Existing Code"
[10]: https://mypy.readthedocs.io/en/stable/protocols.html "mypy Protocols"
