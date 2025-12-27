---
title: "Ruff: Python Linter and Formatter"
description: "Extremely fast Python linter and code formatter written in Rust"
type: "tool-reference"
tags: ["python", "linter", "formatter", "rust", "flake8", "black", "isort", "astral", "performance", "code-quality"]
category: "dev-tools"
subcategory: "python"
version: "0.5.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Ruff Official Documentation"
    url: "https://docs.astral.sh/ruff/"
  - name: "Ruff Tutorial"
    url: "https://docs.astral.sh/ruff/tutorial/"
  - name: "Ruff Linter Documentation"
    url: "https://docs.astral.sh/ruff/linter/"
  - name: "Ruff Formatter Documentation"
    url: "https://docs.astral.sh/ruff/formatter/"
  - name: "Ruff Configuration Guide"
    url: "https://docs.astral.sh/ruff/configuration/"
  - name: "Ruff Rules Reference"
    url: "https://docs.astral.sh/ruff/rules/"
  - name: "Ruff Integrations"
    url: "https://docs.astral.sh/ruff/integrations/"
  - name: "Ruff FAQ"
    url: "https://docs.astral.sh/ruff/faq/"
  - name: "Ruff Installation"
    url: "https://docs.astral.sh/ruff/installation/"
related: ["../uv/uv-tool-reference.md"]
author: "unknown"
contributors: []
---

# Ruff: Python Linter and Formatter

Ruff is an extremely fast Python linter and code formatter written in Rust, developed by Astral. It consolidates functionality from multiple traditional Python tools into a single, unified interface, achieving 10-100x faster speeds than existing tools. ([Ruff Documentation][1])

## Overview

Ruff can replace Flake8, Black, isort, pydocstyle, pyupgrade, and autoflake—executing orders of magnitude faster than these tools combined. ([Ruff Documentation][1]) The tool is backed by Astral and represents a fundamental shift toward faster Python tooling infrastructure.

### Key Performance Characteristics

Ruff achieves 10-100x faster speeds compared to existing linters like Flake8 and formatters like Black. ([Ruff Documentation][1]) It processes the entire CPython codebase from scratch with remarkable speed and includes built-in caching to avoid re-analyzing unchanged files. ([Ruff Documentation][1])

### Adoption

Major open-source projects including Apache Airflow, FastAPI, Hugging Face, Pandas, and SciPy actively use Ruff. ([Ruff Documentation][1])

## Core Capabilities

### Linting

Ruff provides an extremely fast linter designed as a drop-in replacement for Flake8 (plus dozens of plugins), isort, pydocstyle, pyupgrade, autoflake, and more. ([Ruff Linter][3]) The tool includes over 800 built-in rules with native implementations of popular plugins. ([Ruff Documentation][1])

### Formatting

The Ruff formatter is an extremely fast Python code formatter designed as a drop-in replacement for Black. ([Ruff Formatter][4]) Testing on extensive projects like Django and Zulip shows that more than 99.9% of lines are formatted identically to Black. ([Ruff Formatter][4])

### Import Organization

Ruff provides isort-equivalent functionality for import sorting. ([Ruff Documentation][1]) The import sorting aims for near-equivalence with isort's `profile = "black"` mode. ([Ruff FAQ][8])

### Automatic Error Correction

Ruff supports automatic error correction through fix capabilities. ([Ruff Documentation][1]) Fixes are categorized as safe (preserve runtime behavior) or unsafe (may alter exception types or remove comments). ([Ruff Linter][3])

## Installation

### Recommended Installation (with uv)

**Global installation:**
```bash
uv tool install ruff@latest
```

**Project-specific:**
```bash
uv add --dev ruff
```

([Ruff Installation][9])

### Alternative Package Managers

```bash
# pip
pip install ruff

# pipx
pipx install ruff

# Homebrew
brew install ruff

# Conda
conda install -c conda-forge ruff

# Arch Linux
pacman -S ruff

# Alpine
apk add ruff

# openSUSE
sudo zypper install python3-ruff
```

([Ruff Installation][9])

### Standalone Installers (v0.5.0+)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/ruff/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/ruff/install.ps1 | iex"
```

([Ruff Installation][9])

### Quick Execution Without Installation

Use `uvx` to run Ruff directly without installation:
```bash
uvx ruff check
uvx ruff format
```

([Ruff Installation][9])

### Docker

Docker image available at `ghcr.io/astral-sh/ruff`, tagged by release version and "latest":
```bash
docker run ghcr.io/astral-sh/ruff:latest check .
```

([Ruff Installation][9])

## Getting Started

### Basic Usage

**Linting:**
```bash
ruff check .
```

**Formatting:**
```bash
ruff format .
```

([Ruff Installation][9])

### Tutorial Workflow

1. Initialize a project (e.g., with `uv init --lib numbers`)
2. Add Ruff as a dev dependency (`uv add --dev ruff`)
3. Run the linter: `ruff check`
4. Fix issues automatically: `ruff check --fix`
5. Format code: `ruff format`

([Ruff Tutorial][2])

### First Configuration

Create a `pyproject.toml` or `ruff.toml` file:

```toml
[tool.ruff]
line-length = 79
target-version = "py311"

[tool.ruff.lint]
extend-select = ["UP", "D"]
```

([Ruff Tutorial][2])

## Linting

### Primary Command

The `ruff check` command serves as the main entry point. It accepts files or directories and recursively searches for Python files to lint. ([Ruff Linter][3])

### Rule Selection System

Ruff uses Flake8's code system where rules consist of a letter prefix (one to three characters) plus three digits (e.g., F401). ([Ruff Linter][3])

**Selection options:**
- `lint.select` - Explicitly enable specific rules
- `lint.extend-select` - Add rules to existing configuration
- `lint.ignore` - Exclude particular rules

([Ruff Linter][3])

**Example:**
```toml
[tool.ruff.lint]
select = ["E", "F", "W", "I"]
ignore = ["E501"]  # Line too long
```

The documentation recommends preferring `select` over `extend-select` for clarity and cautions against using `ALL` without consideration. ([Ruff Linter][3])

### Default Rule Set

By default, Ruff enables Pyflakes' `F` rules plus select `E` rules, excluding stylistic checks that overlap with formatters like Black. ([Ruff Rules][6])

### Fix Capabilities

Ruff supports automatic fixes categorized as:

- **Safe fixes**: Preserve runtime behavior and code meaning
- **Unsafe fixes**: May alter exception types or remove comments

Only safe fixes are enabled by default; unsafe fixes require the `--unsafe-fixes` flag. ([Ruff Linter][3])

**Example:**
```bash
# Apply safe fixes
ruff check --fix

# Apply all fixes including unsafe
ruff check --fix --unsafe-fixes
```

### Error Suppression

Violations can be suppressed through several methods:

**Inline suppression:**
```python
# Suppress specific rule
import unused_module  # noqa: F401

# Suppress multiple rules
x = 1  # noqa: F841, E501

# Suppress all rules (not recommended)
problematic_code()  # noqa
```

**File-level suppression:**
```python
# ruff: noqa: F401
import unused_module
```

**Configuration-based:**
```toml
[tool.ruff.lint]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*.py" = ["S101"]  # Allow assert in tests
```

([Ruff Linter][3])

The `RUF100` rule detects unused suppression directives. ([Ruff Linter][3])

### Adopting New Rules

When adopting new rules in existing codebases, the `--add-noqa` flag automatically adds suppression comments to all current violations:

```bash
ruff check --select D --add-noqa
```

This allows forward-looking enforcement without fixing existing violations. ([Ruff Tutorial][2])

### Exit Codes

- `0`: No violations or all fixed
- `1`: Violations found
- `2`: Abnormal termination (configuration/internal errors)

([Ruff Linter][3])

## Formatting

### Primary Command

The `ruff format` command formats Python code according to Black's style principles. ([Ruff Formatter][4])

### Black Compatibility

Ruff targets near-identical output to Black when processing existing Black-formatted code. Testing shows that more than 99.9% of lines are formatted identically on projects like Django and Zulip. ([Ruff Formatter][4])

The formatter adheres to Black's stable code style principles emphasizing consistency, generality, and readability. ([Ruff Formatter][4])

### Configuration Options

The formatter supports several configuration settings:

```toml
[tool.ruff.format]
quote-style = "single"  # or "double" (default)
indent-style = "space"  # or "tab"
line-ending = "auto"    # or "lf", "cr-lf"
docstring-code-format = true  # Format code in docstrings
```

([Ruff Formatter][4])

### Key Features

**Docstring Formatting**: Automatically formats Python code examples in docstrings, recognizing:
- Doctest format
- CommonMark fenced code blocks
- reStructuredText literal blocks

([Ruff Formatter][4])

**Format Suppression**: Supports pragma comments to disable formatting selectively:
```python
# fmt: off
x = [1,2,3]  # Won't be reformatted
# fmt: on

# fmt: skip
y = [4,5,6]  # This line only
```

Also supports `# yapf: disable/enable`. ([Ruff Formatter][4])

**F-string Formatting**: Ruff formats expressions within f-string curly braces—a known deviation from Black. It applies configured quote styles and implements line-break heuristics for Python 3.12+. ([Ruff Formatter][4])

### Import Sorting

The formatter does not sort imports automatically. Users must run both commands:

```bash
ruff check --select I --fix  # Sort imports
ruff format                   # Format code
```

([Ruff Formatter][4])

### Lint Rule Conflicts

Certain linter rules conflict with the formatter and should be disabled:

- **Quotes**: Q000-Q003
- **Indentation**: W191, E111, E114, E117
- **Trailing commas**: COM812, COM819
- **Implicit string concatenation**: ISC002

([Ruff Formatter][4])

### Exit Codes

- `0`: Successful completion
- `1`: (--check only) Files would be reformatted
- `2`: Configuration or internal errors

([Ruff Formatter][4])

## Rule Categories

Ruff organizes over 800 rules into prefixed categories. ([Ruff Rules][6])

### Major Rule Categories

**Error & Style Rules:**
- **Pycodestyle (E, W)**: Core PEP 8 compliance covering indentation, whitespace, and line length
- **Pyflakes (F)**: Detects undefined variables, unused imports, and syntax problems

**Framework-Specific Rules:**
- **Django (DJ)**: Identifies anti-patterns in Django model and view code
- **FastAPI (FAST)**: Catches redundant arguments and missing type annotations
- **Pytest (PT)**: Enforces pytest conventions and fixture best practices

**Code Quality & Security:**
- **Bandit (S)**: Security vulnerability detection including hardcoded credentials and unsafe operations
- **Bugbear (B)**: Catches subtle bugs and "gotchas" in Python code
- **Simplify (SIM)**: Suggests clearer, more readable code patterns

**Type & Import Management:**
- **Type-Checking (TC)**: Organizes imports within conditional blocks for runtime efficiency
- **Future Annotations (FA)**: Modernizes type hints using `from __future__ import annotations`

**Code Modernization:**
- **pyupgrade (UP)**: Modernizes Python syntax to use newer language features

**Documentation:**
- **pydocstyle (D)**: Enforces documentation standards and docstring conventions

([Ruff Rules][6])

### Rule Indicators

Ruff uses metadata badges to clarify rule status:
- "🧪" marks unstable, preview-phase rules
- "🛠️" indicates automatically fixable violations
- "⚠️" and "❌" denote deprecated or removed rules

([Ruff Rules][6])

### Example Rule Selection

```toml
[tool.ruff.lint]
select = [
    "E",     # pycodestyle errors
    "W",     # pycodestyle warnings
    "F",     # Pyflakes
    "I",     # isort
    "B",     # flake8-bugbear
    "UP",    # pyupgrade
    "D",     # pydocstyle
    "S",     # Bandit
    "PT",    # flake8-pytest-style
]

ignore = [
    "E501",  # Line too long (handled by formatter)
    "D203",  # Conflicts with D211
    "D213",  # Conflicts with D212
]
```

## Configuration

### Configuration Files

Ruff supports three configuration file formats with equivalent schemas:

- `pyproject.toml` (with `[tool.ruff]` section)
- `ruff.toml`
- `.ruff.toml`

When multiple files exist in the same directory, `.ruff.toml` takes precedence, followed by `ruff.toml`, then `pyproject.toml`. ([Ruff Configuration][5])

### Default Configuration

If no configuration is specified, Ruff applies sensible defaults:

- Line length of 88 characters (matching Black)
- Python 3.9 as target version
- Exclusion of common directories (`.git`, `.venv`, `__pycache__`, etc.)
- Enable Pyflakes and select pycodestyle codes by default

([Ruff Configuration][5])

### Configuration Hierarchy

Ruff implements hierarchical configuration where the "closest" config file applies to each analyzed file. ([Ruff Configuration][5])

**Key rules:**
1. **File discovery**: Ruff ignores `pyproject.toml` files lacking a `[tool.ruff]` section
2. **Direct config**: Settings passed via `--config` apply to all files
3. **Fallback**: If no config exists, Ruff uses defaults or a user-level config
4. **Override precedence**: Command-line settings override all configuration files

([Ruff Configuration][5])

### Configuration Sections

```toml
[tool.ruff]
# General settings
line-length = 88
target-version = "py311"
exclude = [".venv", "build", "dist"]

[tool.ruff.lint]
# Linting rules and enforcement
select = ["E", "F", "I"]
ignore = ["E501"]

[tool.ruff.format]
# Formatter behavior
quote-style = "double"
indent-style = "space"

[tool.ruff.lint.per-file-ignores]
# Rule exceptions by file pattern
"__init__.py" = ["F401"]
"tests/*.py" = ["S101"]
```

([Ruff Configuration][5])

### Python Version Inference

When `target-version` isn't specified, Ruff attempts to infer it from the `requires-python` field in nearby `pyproject.toml` files. ([Ruff Configuration][5])

### File Discovery

By default, Ruff discovers `*.py`, `*.pyi`, `*.ipynb`, and `pyproject.toml` files. Use `extend-include` to add additional file extensions:

```toml
[tool.ruff]
extend-include = ["*.pyw"]
```

([Ruff Configuration][5])

### Command-Line Override

The `--config` flag accepts either file paths or TOML key-value pairs:

```bash
# Use specific config file
ruff check --config path/to/ruff.toml

# Override specific settings
ruff check --config "lint.select=['E','F']"
```

([Ruff Configuration][5])

## Integrations

### Pre-commit Hooks

Integrate Ruff with pre-commit framework via `ruff-pre-commit`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

When running with `--fix`, Ruff's lint hook should be placed before Ruff's formatter hook. ([Ruff Integrations][7])

### GitHub Actions

**Using pip:**
```yaml
- name: Install Ruff
  run: pip install ruff
- name: Lint
  run: ruff check .
- name: Format
  run: ruff format --check .
```

**Using dedicated action:**
```yaml
- uses: astral-sh/ruff-action@v1
  with:
    version: 0.5.0
    args: check --fix
```

([Ruff Integrations][7])

### GitLab CI/CD

Configuration via `.gitlab-ci.yml` using Docker images:

```yaml
ruff:
  image: ghcr.io/astral-sh/ruff:latest
  parallel:
    matrix:
      - COMMAND: ["format --check", "check"]
  script:
    - ruff $COMMAND .
```

Supports GitLab's codequality reporting. ([Ruff Integrations][7])

### Editor Support

Ruff provides first-party editor integrations for VS Code and other editors. ([Ruff Documentation][1]) The documentation includes setup, features, settings, and migration guidance from the legacy ruff-lsp tool. ([Ruff Integrations][7])

### Additional Tools

**mdformat**: The `mdformat-ruff` plugin enables formatting of Python code blocks within Markdown files. ([Ruff Integrations][7])

**Jupyter Notebooks**: Built-in notebook support for `*.ipynb` files; integrates with nbQA for additional functionality. ([Ruff FAQ][8])

## Comparison with Other Tools

### vs. Black (Formatter)

Ruff's formatter is designed as a drop-in replacement for Black with >99.9% identical formatting on existing Black-formatted projects. ([Ruff FAQ][8])

### vs. Flake8 (Linter)

Ruff can replace Flake8 when used without numerous plugins, alongside Black, and on Python 3 code. It implements all Flake8 rules plus reimplements popular plugins natively, including flake8-bugbear and flake8-bandit. ([Ruff FAQ][8])

### vs. Pylint

While Pylint implements ~409 rules and Ruff over 800, they enforce different rule sets. Many users have migrated successfully, especially when pairing Ruff with a type checker, though Pylint offers more sophisticated type inference. ([Ruff FAQ][8])

### vs. Type Checkers (Mypy/Pyright/Pyre)

Ruff is a linter, not a type checker—the tools are complementary. Using both together provides faster lint feedback plus detailed type error detection. ([Ruff FAQ][8])

### vs. isort

Ruff's import sorting aims for near-equivalence with isort's `profile = "black"` mode, with minor differences in aliased imports and inline comments. ([Ruff FAQ][8])

## Best Practices

### Project Setup

1. **Add Ruff as a dev dependency**
   ```bash
   uv add --dev ruff
   ```

2. **Create configuration file**
   ```toml
   [tool.ruff]
   line-length = 88
   target-version = "py311"

   [tool.ruff.lint]
   select = ["E", "F", "I", "B", "UP"]
   ignore = ["E501"]
   ```

3. **Set up pre-commit hooks**
   ```yaml
   - repo: https://github.com/astral-sh/ruff-pre-commit
     hooks:
       - id: ruff
         args: [--fix]
       - id: ruff-format
   ```

### Migration Strategy

When migrating from existing tools:

1. **Start with defaults**: Run Ruff with default settings
2. **Add rules incrementally**: Use `extend-select` to add rule families
3. **Use --add-noqa for new rules**: Suppress existing violations for new rules
4. **Combine linting and formatting**:
   ```bash
   ruff check --select I --fix  # Sort imports
   ruff check --fix              # Fix other issues
   ruff format                   # Format code
   ```

### CI/CD Integration

**Recommended CI workflow:**
```bash
# Check formatting (don't modify files)
ruff format --check

# Lint without fixes (report only)
ruff check

# For auto-fix branches
ruff check --fix
ruff format
```

### Rule Selection

- **Start minimal**: Begin with default rules (F, E)
- **Add by category**: Enable rule families that match your needs
- **Avoid ALL**: Don't use `select = ["ALL"]` without careful consideration
- **Use per-file-ignores**: Disable specific rules for specific files (e.g., S101 for tests)

### Performance Optimization

- **Use caching**: Ruff automatically caches results
- **Run in parallel**: Ruff automatically parallelizes across files
- **Exclude unnecessary paths**: Configure `exclude` to skip vendored code

## Common Workflows

### Development Workflow

```bash
# During development
ruff check --fix .
ruff format .

# Watch mode (requires external tool like watchexec)
watchexec -e py -- ruff check --fix .
```

### CI Workflow

```bash
# Fail if code isn't formatted
ruff format --check .

# Fail if linting issues exist
ruff check .
```

### Pre-commit Workflow

Configured via `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### IDE Integration

Most editors support Ruff through language server integration:

**VS Code**: Install the official Ruff extension
**PyCharm**: Configure as external tool or use File Watchers
**Vim/Neovim**: Use with coc.nvim, ALE, or native LSP

## Troubleshooting

### Common Issues

**Conflicting rules between linter and formatter:**
- Disable formatter-conflicting rules: Q000-Q003, W191, E111, COM812, ISC002

**Different output than Black:**
- Check version compatibility
- Review f-string formatting behavior (known difference)
- Verify line-length settings match

**Rules not being applied:**
- Check configuration file is being discovered
- Verify rule codes are correct (case-sensitive)
- Use `--verbose` to see configuration loading

**Performance issues:**
- Check exclusion patterns
- Verify caching is enabled
- Review file discovery patterns

### Getting Help

**Configuration debugging:**
```bash
ruff check --show-settings
```

**Rule documentation:**
```bash
ruff rule E501
```

**Version information:**
```bash
ruff version
```

### Resources

- Official documentation: https://docs.astral.sh/ruff/
- GitHub repository: https://github.com/astral-sh/ruff
- VS Code extension: Search "Ruff" in VS Code marketplace
- Community support: GitHub Discussions

## Python Version Support

Ruff lints Python 3.7+ code and is installable on Python 3.7+. ([Ruff FAQ][8]) No Rust toolchain is required for installation. ([Ruff FAQ][8])

## Advanced Features

### Configuration via pyproject.toml

Beyond `pyproject.toml`, Ruff supports `ruff.toml` with identical schemas for projects that prefer dedicated tool configuration. ([Ruff FAQ][8])

### Jupyter Notebook Support

Built-in support for `*.ipynb` files with integration for nbQA for additional functionality. ([Ruff FAQ][8])

### Custom Rule Development

While Ruff implements rules internally in Rust, the project welcomes contributions for new rules matching popular Flake8 plugins.

## References

[1]: https://docs.astral.sh/ruff/ "Ruff Official Documentation"
[2]: https://docs.astral.sh/ruff/tutorial/ "Ruff Tutorial"
[3]: https://docs.astral.sh/ruff/linter/ "Ruff Linter Documentation"
[4]: https://docs.astral.sh/ruff/formatter/ "Ruff Formatter Documentation"
[5]: https://docs.astral.sh/ruff/configuration/ "Ruff Configuration Guide"
[6]: https://docs.astral.sh/ruff/rules/ "Ruff Rules Reference"
[7]: https://docs.astral.sh/ruff/integrations/ "Ruff Integrations"
[8]: https://docs.astral.sh/ruff/faq/ "Ruff FAQ"
[9]: https://docs.astral.sh/ruff/installation/ "Ruff Installation"
