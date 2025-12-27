---
author: unknown
category: dev-tools
contributors: []
description: Extremely fast Python package manager and project management tool
last_updated: '2025-11-01'
related:
- ../../../pydantic-ai/README.md
sources:
- name: uv Official Documentation
  url: https://docs.astral.sh/uv/
- name: uv Getting Started
  url: https://docs.astral.sh/uv/getting-started/
- name: uv Concepts
  url: https://docs.astral.sh/uv/concepts/
- name: uv Project Guide
  url: https://docs.astral.sh/uv/guides/projects/
- name: uv Script Guide
  url: https://docs.astral.sh/uv/guides/scripts/
- name: uv Docker Integration
  url: https://docs.astral.sh/uv/guides/integration/docker/
- name: uv CLI Reference
  url: https://docs.astral.sh/uv/reference/cli/
- name: uv Settings Reference
  url: https://docs.astral.sh/uv/reference/settings/
status: stable
subcategory: python
tags:
- python
- package-manager
- dependency-management
- rust
- pip
- virtualenv
- astral
- performance
- cli
title: 'uv: Python Package and Project Manager'
type: tool-reference
version: 0.9.6
---

# uv: Python Package and Project Manager

uv is an extremely fast Python package and project manager written in Rust, developed by Astral (creators of Ruff). It consolidates functionality from approximately nine traditional Python tools into a single unified interface. ([uv Documentation][1])

## Overview

uv replaces multiple Python development tools including `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, and `virtualenv`. The tool manages dependencies, virtual environments, Python version installation, script execution, and package publishing. ([uv Documentation][1])

### Key Performance Characteristics

uv achieves 10-100x faster speeds compared to pip through its Rust implementation and efficient caching mechanisms. ([uv Documentation][1]) The tool uses a global cache system that reduces disk space usage through dependency deduplication.

### Cross-Platform Support

uv supports macOS, Linux, and Windows with consistent behavior across all platforms. ([uv Documentation][1])

## Core Capabilities

### Project Management

uv provides comprehensive project support with universal lockfiles and workspace capabilities, similar to Poetry or Rye. ([uv Documentation][1]) Projects include full dependency and environment management.

### Script Support

uv executes single-file Python scripts with inline dependency declarations using PEP 723 format. ([uv Script Guide][5]) This allows portable scripts that carry their dependencies as metadata.

### Tool Execution

uv installs and runs command-line tools via Python packages in isolated environments, similar to pipx functionality. ([uv Documentation][1]) The `uvx` command invokes tools without permanent installation. ([uv Tool Guide][9])

### Python Version Management

uv downloads and manages multiple Python versions using distributions from Astral's `python-build-standalone` project. ([uv Python Guide][10]) Python does not need to be explicitly installed—uv automatically downloads required versions. ([uv Python Guide][10])

### pip Interface

uv provides a drop-in replacement for common `pip`, `pip-tools`, and `virtualenv` commands. ([uv pip Documentation][4]) However, uv does not rely on or invoke pip itself—the interface is named for compatibility purposes. ([uv pip Documentation][4])

## Installation

### Standalone Installer

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Additional installation methods include pip, Homebrew, and other distribution channels. ([uv Getting Started][2])

## Project Workflow

### Initialization

Create a new Python project:
```bash
uv init my-project
cd my-project
```

This generates a basic project structure including `.gitignore`, `.python-version`, `README.md`, `main.py`, and `pyproject.toml`. ([uv Project Guide][4])

### Project Structure

**Key components:**

- **`pyproject.toml`**: Contains project metadata and dependency specifications
- **`.python-version`**: Specifies the default Python version
- **`.venv`**: The isolated virtual environment
- **`uv.lock`**: Cross-platform lockfile containing exact dependency information ([uv Project Guide][4])

The `uv.lock` file is a human-readable TOML file that should be version-controlled for reproducible installations. ([uv Project Guide][4])

### Dependency Management

**Adding dependencies:**
```bash
# Basic package
uv add requests

# With version constraint
uv add 'requests==2.31.0'

# From git repository
uv add git+https://github.com/psf/requests

# From requirements.txt
uv add -r requirements.txt
```

**Removing dependencies:**
```bash
uv remove requests
```

**Upgrading packages:**
```bash
uv lock --upgrade-package requests
```

([uv Project Guide][4])

### Running Commands

Execute scripts and commands while automatically syncing the lockfile and environment:
```bash
uv run python main.py
uv run pytest
```

Alternatively, manually update the environment and activate it:
```bash
uv sync
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

([uv Project Guide][4])

### Building Distributions

Create source distributions and wheels:
```bash
uv build
```

Artifacts are placed in a `dist/` subdirectory by default. ([uv Project Guide][4])

## Script Execution

### Basic Script Running

Execute Python scripts with automatic environment management:
```bash
uv run example.py
```

For standard library imports, no dependencies are required. ([uv Script Guide][5])

### Inline Dependency Declaration

uv supports PEP 723 inline script metadata format. Declare dependencies in a comment block at the script's top:

```python
# /// script
# dependencies = [
#     "requests<3",
#     "rich",
# ]
# requires-python = ">=3.11"
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(response.json())
```

([uv Script Guide][5])

### Ad-hoc Dependencies

Install packages for a single invocation:
```bash
uv run --with rich example.py
```

([uv Script Guide][5])

### Executable Scripts

Make scripts directly executable on Unix systems with a shebang:
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///

import requests
```

Then execute directly:
```bash
chmod +x script.py
./script.py
```

([uv Script Guide][5])

### Script Locking

Create reproducible `.lock` files for scripts:
```bash
uv lock --script example.py
```

([uv Script Guide][5])

## Tool Management

### Running Tools Without Installation

The `uvx` command invokes tools in temporary, isolated environments:
```bash
uvx ruff check
uvx black .
```

([uv Tool Guide][9])

### Installing Tools

For frequently-used tools, install permanently:
```bash
uv tool install ruff
```

Installed tools have executables placed in a `bin` directory on your PATH. ([uv Tool Guide][9])

### Version Control

Specify versions using `@` syntax or `--from` option:
```bash
uvx ruff@0.4.0 check
uvx --from 'ruff>0.2.0,<0.3.0' ruff check
```

([uv Tool Guide][9])

### Alternative Sources

Install from git repositories:
```bash
uvx --from git+https://github.com/httpie/cli httpie
```

([uv Tool Guide][9])

### Python Version Selection

Specify interpreter with `--python` flag:
```bash
uvx --python 3.11 black .
```

([uv Tool Guide][9])

## Python Version Management

### Installing Python

Install the latest Python version:
```bash
uv python install
```

Install specific versions:
```bash
uv python install 3.12
uv python install [[email protected]](/cdn-cgi/l/email-protection)
```

Multiple versions can be installed simultaneously, and alternative implementations like PyPy are supported. ([uv Python Guide][10])

### Viewing Installations

List available and installed Python versions:
```bash
uv python list
```

([uv Python Guide][10])

### Automatic Downloads

uv automatically downloads Python versions when required by commands like `uv venv`. Python does not need to be explicitly installed to use uv. ([uv Python Guide][10])

### Upgrading Versions

Update Python patch versions (preview feature):
```bash
uv python upgrade 3.12
```

([uv Python Guide][10])

## Configuration

### Configuration Files

Settings can be declared in `pyproject.toml` under `[tool.uv]` or in separate configuration files. ([uv Settings Reference][8])

### Project Metadata Settings

Key project settings include:

- **Dependency management**: `dev-dependencies`, `dependency-groups`, `constraint-dependencies`, `override-dependencies`
- **Package sources**: `sources`, `index` configurations
- **Project structure**: `package` (distinguishes packages from virtual projects), workspace `members` and `exclude`
- **Build backend settings**: `module-name`, `module-root`, namespace packages

([uv Settings Reference][8])

Packages are built and installed in editable mode, while virtual projects are not built or installed. ([uv Settings Reference][8])

### Runtime Configuration Settings

Options controlling resolution and installation behavior:

- **Index control**: `index-url`, `extra-index-url`, `index-strategy`, `no-index`
- **Resolution strategy**: `resolution` (highest/lowest/lowest-direct), `fork-strategy`, `prerelease` handling
- **Installation**: `link-mode` (clone/copy/hardlink/symlink), `compile-bytecode`, `reinstall`
- **Network**: `offline`, `native-tls`, `allow-insecure-host`, `keyring-provider`
- **Performance**: `concurrent-builds`, `concurrent-downloads`, `concurrent-installs`, `cache-dir`

([uv Settings Reference][8])

### pip-Specific Settings

Located under `[tool.uv.pip]`:

- **Output formatting**: `annotation-style`, `no-annotate`, `emit-index-url`, `emit-hashes`
- **Resolution options**: `all-extras`, `extra`, `group`, `no-deps`
- **Build controls**: `config-settings`, `no-build-isolation-package`, `only-binary`

([uv Settings Reference][8])

## Dependency Resolution

### Resolution Process

Resolution converts a list of requirements into compatible package versions by recursively searching for compatible versions while ensuring all declared dependencies are satisfied. ([uv Resolution Concepts][11])

### Resolution Modes

**Platform-Specific Resolution**: Default mode in `uv pip compile` produces platform-specific results. Target alternate platforms using `--python-platform` and `--python-version` flags. ([uv Resolution Concepts][11])

**Universal Resolution**: The `uv.lock` file uses universal resolution for cross-platform portability. During this process, a package may be listed multiple times with different versions or URLs if needed for different platforms. ([uv Resolution Concepts][11])

### Selection Strategies

By default, uv selects the latest compatible version. Alternative strategies:

- `--resolution lowest`: Install the lowest possible versions for all dependencies
- `--resolution lowest-direct`: Use lowest versions for direct dependencies, latest for transitive

([uv Resolution Concepts][11])

### Handling Conflicts

For optional dependencies or workspace members with incompatible versions, use explicit conflict declarations in `pyproject.toml`:

```toml
[tool.uv]
conflicts = [
    [
      { extra = "extra1" },
      { extra = "extra2" },
    ],
]
```

([uv Resolution Concepts][11])

### Additional Features

- **Pre-release handling**: Requires user opt-in for transitive pre-releases
- **Dependency overrides**: Replace declared requirements to bypass metadata
- **Constraint files**: Narrow acceptable versions without requiring package inclusion
- **Reproducibility**: `--exclude-newer` limits resolution to distributions before a specified date

([uv Resolution Concepts][11])

## Caching

### Cache Strategy

uv implements different caching approaches by dependency type:

- **Registry dependencies**: Respects HTTP caching headers
- **Direct URLs**: Respects HTTP headers and caches by URL
- **Git dependencies**: Caches using fully-resolved commit hashes
- **Local dependencies**: Caches based on modification timestamps

([uv Cache Concepts][12])

### Cache Invalidation

Force cache updates using:

```bash
# Wipe all entries
uv cache clean

# Clean specific package
uv cache clean <package>

# Revalidate all cached dependencies
uv sync --refresh

# Target individual packages
uv sync --refresh-package requests

# Ignore existing installed versions
uv sync --reinstall
```

([uv Cache Concepts][12])

### Dynamic Metadata Handling

Projects with computed metadata can define cache keys in `pyproject.toml` via `tool.uv.cache-keys`. This supports:

- File paths (including glob patterns)
- Git commit hashes and tags
- Environment variables
- Directory presence/absence

Note: Glob patterns can be expensive as uv may need to walk the filesystem. ([uv Cache Concepts][12])

### Cache Safety

uv's cache is thread-safe and append-only for concurrent operations. For CI environments, `uv cache prune --ci` removes pre-built wheels while retaining built-from-source wheels. ([uv Cache Concepts][12])

## Docker Integration

### Available Images

uv offers two image types:

1. **Distroless images**: `ghcr.io/astral-sh/uv:latest` (binary-only, minimal)
2. **Derived images**: Alpine, Debian, and Python-based options

The distroless images contain only the uv binaries. ([uv Docker Guide][6])

### Installation in Docker

**Binary copy (recommended):**
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

**Installer script:**
Requires curl and CA certificates. ([uv Docker Guide][6])

Best practice: Pin specific versions for reproducible builds:
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/
```

([uv Docker Guide][6])

### Best Practices

- **Add `.venv` to `.dockerignore`** to prevent local virtual environments from being included
- **Use intermediate layers** by separating dependency installation from project code via `--no-install-project`
- **Enable bytecode compilation** for production: `--compile-bytecode`
- **Implement cache mounts** to improve build performance
- **Consider multi-stage builds** with `--no-editable` to exclude source code from final images

([uv Docker Guide][6])

### Development Workflow

Mount projects using:
```bash
docker run --volume .:/app --volume /app/.venv
```

Or use Docker Compose `watch` feature (requires Compose 2.22.0+). ([uv Docker Guide][6])

### Image Verification

Docker images include cryptographic attestations verifiable via GitHub CLI or `cosign`, confirming official provenance. ([uv Docker Guide][6])

## CLI Commands Reference

### Core Project Commands

- **`uv init`**: Create a new project
- **`uv add`**: Add dependencies
- **`uv remove`**: Remove dependencies
- **`uv sync`**: Sync environment to specifications
- **`uv lock`**: Update lockfile
- **`uv run`**: Execute commands or scripts

### Dependency Management

- **`uv export`**: Transform lockfile to alternative formats
- **`uv tree`**: Visualize dependency hierarchy
- **`uv pip`**: pip-compatible package management
- **`uv version`**: Access or modify project version

### Python & Environment Management

- **`uv python`**: Manage Python versions
- **`uv venv`**: Create virtual environments
- **`uv tool`**: Deploy and execute tools

### Build & Distribution

- **`uv build`**: Generate distributions
- **`uv publish`**: Upload to package indexes
- **`uv format`**: Format Python code

### Maintenance Commands

- **`uv auth`**: Manage authentication
- **`uv cache`**: Manage cached data
- **`uv self`**: Update uv itself

([uv CLI Reference][7])

## Migration from pip/pip-tools

uv provides a drop-in replacement for pip commands with enhanced features. Key compatibility notes:

- Commands do not exactly replicate pip behavior
- Deviations more likely beyond standard workflows
- Consult pip-compatibility guide for specific differences

([uv pip Documentation][4])

### Common Equivalent Commands

| pip/pip-tools | uv equivalent |
|--------------|---------------|
| `pip install` | `uv pip install` or `uv sync` |
| `pip freeze` | `uv pip freeze` or `uv export` |
| `pip-compile` | `uv pip compile` |
| `pip-sync` | `uv pip sync` |
| `virtualenv` | `uv venv` |

## Best Practices

### Project Organization

- Always commit `uv.lock` for reproducible installations
- Use `.python-version` to specify Python requirements
- Separate development dependencies using `dev-dependencies`
- Use workspaces for monorepo structures

### Dependency Management

- Pin versions for production deployments
- Use constraint files to limit transitive dependencies
- Leverage dependency overrides sparingly for patches
- Test with `--resolution lowest` to ensure minimum version compatibility

### Performance Optimization

- Use cache mounts in Docker for faster builds
- Enable `compile-bytecode` for production images
- Leverage concurrent build/download/install settings
- Use `uv cache prune --ci` in CI environments

### Script Development

- Use inline metadata for portable scripts
- Lock scripts for reproducible execution
- Consider `uvx` for one-off tool execution
- Use shebangs for executable scripts

## Troubleshooting

### Common Issues

**Slow downloads**: Check network settings and consider `concurrent-downloads` setting

**Resolution conflicts**: Use `--resolution lowest-direct` or explicit conflict declarations

**Cache issues**: Run `uv cache clean` to invalidate cache

**Platform compatibility**: Use universal resolution with `uv.lock` for cross-platform projects

### Environment Variables

uv respects standard Python environment variables and provides its own:

- `UV_CACHE_DIR`: Override cache location
- `UV_INDEX_URL`: Set default package index
- `UV_PYTHON`: Specify Python executable

### Getting Help

- Official documentation: https://docs.astral.sh/uv/
- GitHub issues: https://github.com/astral-sh/uv
- Community resources available through documentation site

## References

[1]: https://docs.astral.sh/uv/ "uv Official Documentation"
[2]: https://docs.astral.sh/uv/getting-started/ "uv Getting Started"
[3]: https://docs.astral.sh/uv/concepts/ "uv Concepts"
[4]: https://docs.astral.sh/uv/guides/projects/ "uv Project Guide"
[5]: https://docs.astral.sh/uv/guides/scripts/ "uv Script Guide"
[6]: https://docs.astral.sh/uv/guides/integration/docker/ "uv Docker Integration"
[7]: https://docs.astral.sh/uv/reference/cli/ "uv CLI Reference"
[8]: https://docs.astral.sh/uv/reference/settings/ "uv Settings Reference"
[9]: https://docs.astral.sh/uv/guides/tools/ "uv Tool Guide"
[10]: https://docs.astral.sh/uv/guides/install-python/ "uv Python Installation Guide"
[11]: https://docs.astral.sh/uv/concepts/resolution/ "uv Resolution Concepts"
[12]: https://docs.astral.sh/uv/concepts/cache/ "uv Cache Concepts"