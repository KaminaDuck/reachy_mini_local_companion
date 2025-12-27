---
title: "uv Workspaces: Multi-Project Management"
description: "Managing multiple Python packages together with unified dependencies"
type: "concept-guide"
tags: ["uv", "workspaces", "monorepo", "python", "dependency-management", "multi-package", "cargo", "astral"]
category: "dev-tools"
subcategory: "python"
version: "0.9.6"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "uv Workspaces Documentation"
    url: "https://docs.astral.sh/uv/concepts/projects/workspaces/"
  - name: "uv Settings Reference"
    url: "https://docs.astral.sh/uv/reference/settings/"
  - name: "uv Projects Documentation"
    url: "https://docs.astral.sh/uv/concepts/projects/"
  - name: "uv Dependencies Documentation"
    url: "https://docs.astral.sh/uv/concepts/projects/dependencies/"
  - name: "uv Configuration Documentation"
    url: "https://docs.astral.sh/uv/concepts/projects/config/"
  - name: "uv Project Layout"
    url: "https://docs.astral.sh/uv/concepts/projects/layout/"
related: ["uv-tool-reference.md"]
author: "unknown"
contributors: []
---

# uv Workspaces: Multi-Project Management

uv workspaces, inspired by Rust's Cargo, are a collection of one or more packages, called workspace members, that are managed together. ([uv Workspaces][1]) They enable developers to organize large codebases by splitting them into multiple packages while sharing common dependencies and a single lockfile.

## Overview

Workspaces allow developers to "work on multiple projects at once" by coordinating dependencies and configurations across several related projects simultaneously. ([uv Projects][3]) Rather than treating each package in isolation, workspaces provide unified dependency management while maintaining modularity.

### Key Characteristics

**Unified Dependency Management**: The workspace operates with a consistent set of dependencies through one shared lockfile, even though each package maintains its own `pyproject.toml`. ([uv Workspaces][1])

**Editable Installations**: Dependencies between workspace members are installed as editable installations, meaning source code changes reflect immediately without reinstallation. ([uv Dependencies][4])

**Single Lockfile**: The workspace uses one `uv.lock` file that captures exact resolved package versions across all members and all Python markers (OS, architecture, Python version). ([uv Project Layout][6])

**Independent pyproject.toml**: Each workspace member maintains its own `pyproject.toml` file with its own metadata, dependencies, and configuration. ([uv Workspaces][1])

## Core Concepts

### Workspace Root

The workspace root is the directory containing the `pyproject.toml` file with a `[tool.uv.workspace]` table. This file defines which packages are included as workspace members.

### Workspace Members

Workspace members are individual Python packages within the workspace. Each member:
- Has its own `pyproject.toml` file
- Can declare its own dependencies
- Can depend on other workspace members
- Shares the workspace's lockfile
- Is installed in editable mode by default

### Shared Lockfile

The `uv.lock` file at the workspace root ensures all members use a consistent set of dependencies. The `uv lock` command operates on the entire workspace, resolving dependencies for all members simultaneously. ([uv Workspaces][1])

## Configuration

### Workspace Definition

A workspace requires a `[tool.uv.workspace]` table in the root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

([uv Workspaces][1])

### Configuration Options

#### members

**Required**: Packages to include as workspace members. Supports both globs and explicit paths. ([uv Settings][2])

**Type**: `list[str]`
**Default**: `[]`

**Example**:
```toml
[tool.uv.workspace]
members = ["member1", "path/to/member2", "libs/*"]
```

([uv Settings][2])

#### exclude

**Optional**: Packages to exclude as workspace members. If a package matches both `members` and `exclude`, it will be excluded. ([uv Settings][2])

**Type**: `list[str]`
**Default**: `[]`

**Example**:
```toml
[tool.uv.workspace]
members = ["packages/*"]
exclude = ["packages/seeds"]
```

([uv Workspaces][1], [uv Settings][2])

Both `members` and `exclude` support glob patterns for flexible workspace composition. ([uv Settings][2])

## Workspace Structure

### Example Directory Layout

```
my-workspace/
├── pyproject.toml          # Workspace root with [tool.uv.workspace]
├── uv.lock                 # Shared lockfile for all members
├── .venv/                  # Shared virtual environment
├── packages/
│   ├── core/
│   │   ├── pyproject.toml  # Member: core package
│   │   └── src/
│   │       └── core/
│   ├── api/
│   │   ├── pyproject.toml  # Member: api package
│   │   └── src/
│   │       └── api/
│   └── cli/
│       ├── pyproject.toml  # Member: cli package
│       └── src/
│           └── cli/
```

### Workspace Root pyproject.toml

```toml
[project]
name = "my-workspace"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["packages/*"]
```

### Member pyproject.toml

```toml
[project]
name = "my-workspace-core"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]
```

## Workspace Dependencies

### Declaring Workspace Dependencies

All workspace members must be explicitly stated. ([uv Dependencies][4]) To declare a dependency on another workspace member:

1. Add the member to `project.dependencies` or `project.optional-dependencies`
2. Specify `{ workspace = true }` in `[tool.uv.sources]`
3. Ensure the member is listed in `[tool.uv.workspace.members]`

**Example**:

Root `pyproject.toml`:
```toml
[tool.uv.workspace]
members = ["packages/core", "packages/api"]
```

`packages/api/pyproject.toml`:
```toml
[project]
name = "my-api"
dependencies = [
    "my-core",
    "fastapi>=0.104.0",
]

[tool.uv.sources]
my-core = { workspace = true }
```

([uv Workspaces][1], [uv Dependencies][4])

### Editable Installations

Workspace members are always editable. ([uv Dependencies][4]) This means:
- Changes to source code are immediately available
- No reinstallation is required after code changes
- Development workflow is streamlined

## Command Behavior

### uv lock

The `uv lock` command operates on the entire workspace, resolving dependencies for all members and updating the shared `uv.lock` file. ([uv Workspaces][1])

```bash
uv lock
```

### uv sync

The `uv sync` command defaults to the workspace root but accepts a `--package` argument for targeting specific members. ([uv Workspaces][1])

```bash
# Sync entire workspace
uv sync

# Sync specific member
uv sync --package my-api
```

### uv run

The `uv run` command defaults to the workspace root but accepts a `--package` argument. ([uv Workspaces][1])

```bash
# Run command in workspace root context
uv run python -m my_app

# Run command for specific member
uv run --package my-api python -m my_api
```

### uv add

Add dependencies to workspace members:

```bash
# Add to workspace root
uv add requests

# Add to specific member
cd packages/api
uv add fastapi
```

## Use Cases

### Ideal Use Cases

Workspaces excel for:

**Root projects with accompanying libraries**: A main application with supporting library packages. ([uv Workspaces][1])

**Libraries requiring performance-critical extensions**: Libraries with Rust, C++, or other native extensions that need separate build configurations. ([uv Workspaces][1])

**Plugin systems with separate packages**: Applications with a plugin architecture where each plugin is a separate package. ([uv Workspaces][1])

### Example: Application with Libraries

```
my-app/
├── pyproject.toml          # Main application
├── packages/
│   ├── database/           # Database utilities
│   ├── auth/               # Authentication library
│   └── api-client/         # API client library
```

### Example: Library with Extensions

```
scientific-lib/
├── pyproject.toml          # Pure Python core
├── extensions/
│   ├── rust-compute/       # Rust extension
│   └── cpp-optimize/       # C++ extension
```

## When to Avoid Workspaces

Workspaces aren't suitable when:

**Members have conflicting requirements**: Different packages need incompatible versions of the same dependency. ([uv Workspaces][1])

**Separate virtual environments are desired per member**: Each package needs its own isolated environment. ([uv Workspaces][1])

**Different Python versions must be tested across members**: Testing different Python versions requires separate environments. ([uv Workspaces][1])

In these cases, **path dependencies** offer more flexibility than workspace structure. ([uv Workspaces][1])

## Path Dependencies vs Workspaces

### Path Dependencies

Use path dependencies when you need:
- Separate lockfiles per project
- Different Python versions per project
- Independent virtual environments
- Flexibility to use different dependency versions

**Example**:
```toml
[project]
dependencies = ["my-lib"]

[tool.uv.sources]
my-lib = { path = "../my-lib" }
```

### Workspaces

Use workspaces when you need:
- Unified dependency management
- Single shared lockfile
- Consistent dependency versions across projects
- Editable installations by default
- Coordinated development across packages

## Advanced Configuration

### Conflicting Dependencies

Explicitly declare incompatible dependency groups using `conflicts`: ([uv Configuration][5])

```toml
[tool.uv]
conflicts = [
    [
        { package = "api", extra = "postgres" },
        { package = "api", extra = "mysql" },
    ],
]
```

### Package Control

Override automatic package detection: ([uv Configuration][5])

```toml
[tool.uv]
package = true   # Force packaging
# or
package = false  # Prevent packaging
```

### Build System Configuration

For workspace members with native extensions: ([uv Configuration][5])

```toml
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"
```

### Environment Constraints

Limit lockfile to specific platforms: ([uv Configuration][5])

```toml
[tool.uv]
environments = ["sys_platform == 'linux'", "python_version >= '3.11'"]
```

## Workflows

### Creating a Workspace

**1. Initialize workspace root:**
```bash
mkdir my-workspace
cd my-workspace
uv init --bare
```

**2. Configure workspace:**
```toml
# pyproject.toml
[project]
name = "my-workspace"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["packages/*"]
```

**3. Create workspace members:**
```bash
mkdir -p packages
cd packages
uv init --lib core
uv init --lib api
uv init --app cli
```

**4. Set up dependencies between members:**
```bash
cd api
uv add my-workspace-core
```

Edit `packages/api/pyproject.toml`:
```toml
[tool.uv.sources]
my-workspace-core = { workspace = true }
```

**5. Lock workspace:**
```bash
cd ../..  # Back to workspace root
uv lock
```

### Development Workflow

**Sync entire workspace:**
```bash
uv sync
```

**Run commands in workspace context:**
```bash
uv run python -m my_workspace_cli
uv run --package api python -m tests
```

**Add dependencies to specific members:**
```bash
cd packages/api
uv add fastapi uvicorn
cd ../..
uv lock  # Update workspace lockfile
```

### Building and Publishing

**Build specific workspace member:**
```bash
uv build --package my-workspace-api
```

**Publish workspace member:**
```bash
uv publish --package my-workspace-api
```

## Best Practices

### Project Structure

**1. Use consistent naming**: Name workspace members with a common prefix:
```
my-project-core
my-project-api
my-project-cli
```

**2. Organize by function**: Group related packages in subdirectories:
```
packages/libraries/
packages/services/
packages/tools/
```

**3. Keep workspace root minimal**: The root `pyproject.toml` should primarily define workspace configuration.

### Dependency Management

**1. Declare all workspace dependencies explicitly**: Don't rely on transitive dependencies between workspace members.

**2. Use consistent Python version requirements**: All members should have compatible `requires-python` values.

**3. Leverage shared dependencies**: Put common dependencies in a shared core library.

**4. Version workspace members together**: Use the same version number across related packages.

### Development

**1. Use editable installations**: Leverage the automatic editable installs for fast iteration.

**2. Run tests from workspace root**: Ensure consistent environment:
```bash
uv run pytest packages/*/tests
```

**3. Lock frequently**: Run `uv lock` after adding or updating dependencies.

**4. Use --package for member-specific operations**:
```bash
uv run --package api pytest
uv build --package core
```

### CI/CD

**1. Cache the workspace lockfile**:
```yaml
- uses: actions/cache@v3
  with:
    path: uv.lock
    key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}
```

**2. Sync entire workspace in CI**:
```bash
uv sync --all-extras
```

**3. Test all workspace members**:
```bash
for package in packages/*/; do
  uv run --package $(basename $package) pytest
done
```

## Troubleshooting

### Common Issues

**"Package not found in workspace"**

Ensure:
1. Package directory matches `members` pattern
2. Package `pyproject.toml` has `[project]` table with `name`
3. Workspace `members` list includes the package path

**"Conflicting dependencies between workspace members"**

Solutions:
- Use path dependencies instead of workspaces
- Refactor to use compatible dependency versions
- Use `conflicts` to explicitly declare incompatibility

**"Changes not reflected after editing code"**

Verify:
- Package is installed in editable mode (default for workspaces)
- Running from workspace root or using `--package` flag
- Virtual environment is activated or using `uv run`

**"Different Python versions needed"**

Workspaces share one Python version. For different versions:
- Use separate projects with path dependencies
- Create multiple workspaces
- Use matrix testing in CI with different environments

### Debugging Commands

**Show workspace structure:**
```bash
uv tree
```

**Verify workspace member installation:**
```bash
uv pip list | grep my-workspace
```

**Check lockfile status:**
```bash
uv lock --check
```

**Sync with verbose output:**
```bash
uv sync -v
```

## Migration

### From Separate Projects to Workspace

**1. Create workspace root:**
```bash
mkdir my-workspace
cd my-workspace
uv init --bare
```

**2. Move projects into workspace:**
```bash
mkdir packages
mv ../project1 packages/
mv ../project2 packages/
```

**3. Configure workspace:**
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

**4. Update inter-project dependencies:**

In `packages/project2/pyproject.toml`:
```toml
[project]
dependencies = ["project1"]

[tool.uv.sources]
project1 = { workspace = true }
```

**5. Lock and sync:**
```bash
uv lock
uv sync
```

### From Poetry/PDM to uv Workspace

**1. Convert each project's pyproject.toml to uv format**

**2. Create workspace configuration**

**3. Replace path dependencies with workspace dependencies**

**4. Generate new lockfile:**
```bash
uv lock
```

## Examples

### Example 1: FastAPI Application with Shared Libraries

```
fastapi-workspace/
├── pyproject.toml
├── uv.lock
├── packages/
│   ├── models/         # Pydantic models
│   ├── database/       # Database utilities
│   ├── auth/           # Authentication
│   └── api/            # FastAPI application
```

**Root pyproject.toml:**
```toml
[project]
name = "fastapi-workspace"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["packages/*"]
```

**packages/api/pyproject.toml:**
```toml
[project]
name = "api"
version = "0.1.0"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "models",
    "database",
    "auth",
]

[tool.uv.sources]
models = { workspace = true }
database = { workspace = true }
auth = { workspace = true }
```

### Example 2: Library with Rust Extensions

```
numeric-lib/
├── pyproject.toml
├── uv.lock
├── core/               # Pure Python core
│   ├── pyproject.toml
│   └── src/
└── extensions/
    └── fast-compute/   # Rust extension
        ├── pyproject.toml
        ├── Cargo.toml
        └── src/
```

**Root pyproject.toml:**
```toml
[project]
name = "numeric-lib"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["core", "extensions/*"]
```

**extensions/fast-compute/pyproject.toml:**
```toml
[project]
name = "numeric-lib-fast"
version = "0.1.0"
dependencies = ["numeric-lib-core"]

[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[tool.uv.sources]
numeric-lib-core = { workspace = true }
```

### Example 3: Plugin System

```
app-with-plugins/
├── pyproject.toml
├── uv.lock
├── core/               # Application core
│   └── pyproject.toml
└── plugins/
    ├── database/       # Database plugin
    │   └── pyproject.toml
    ├── cache/          # Cache plugin
    │   └── pyproject.toml
    └── monitoring/     # Monitoring plugin
        └── pyproject.toml
```

**Root pyproject.toml:**
```toml
[project]
name = "app-with-plugins"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["core", "plugins/*"]
```

**core/pyproject.toml:**
```toml
[project]
name = "app-core"
version = "0.1.0"
dependencies = []

[project.entry-points."app.plugins"]
database = "app_plugins_database:plugin"
cache = "app_plugins_cache:plugin"
```

## Comparison with Other Tools

### vs Poetry Workspaces

**Poetry**: No built-in workspace support; uses path dependencies

**uv**: Native workspace support with shared lockfile

### vs Pants/Bazel

**Pants/Bazel**: General-purpose build systems with Python support

**uv**: Python-specific with focus on speed and simplicity

### vs Cargo (Rust)

**Cargo**: Direct inspiration for uv workspaces

**uv**: Adapts Cargo's workspace concept to Python ecosystem

## Related Concepts

### Projects

Workspaces are collections of projects. Each workspace member is a project with its own `pyproject.toml`. ([uv Projects][3])

### Virtual Environments

Workspaces use a single shared virtual environment at the workspace root. ([uv Project Layout][6])

### Lockfiles

The workspace lockfile (`uv.lock`) ensures reproducible installations across all members. ([uv Project Layout][6])

### Dependency Sources

Workspace dependencies use the `{ workspace = true }` source type. ([uv Dependencies][4])

## References

[1]: https://docs.astral.sh/uv/concepts/projects/workspaces/ "uv Workspaces Documentation"
[2]: https://docs.astral.sh/uv/reference/settings/ "uv Settings Reference"
[3]: https://docs.astral.sh/uv/concepts/projects/ "uv Projects Documentation"
[4]: https://docs.astral.sh/uv/concepts/projects/dependencies/ "uv Dependencies Documentation"
[5]: https://docs.astral.sh/uv/concepts/projects/config/ "uv Configuration Documentation"
[6]: https://docs.astral.sh/uv/concepts/projects/layout/ "uv Project Layout"
