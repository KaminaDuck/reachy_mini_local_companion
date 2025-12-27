---
title: "pnpm Package Manager Reference"
description: "Fast, disk-efficient package manager with monorepo workspace support"
type: "tool-reference"
tags: ["pnpm", "package-manager", "monorepo", "workspaces", "npm", "node", "dependency-management"]
category: "ts"
subcategory: "dev-tools"
version: "10.9"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "pnpm Motivation"
    url: "https://pnpm.io/motivation"
  - name: "pnpm Documentation"
    url: "https://pnpm.io/"
  - name: "pnpm Installation"
    url: "https://pnpm.io/installation"
  - name: "pnpm CLI Add"
    url: "https://pnpm.io/cli/add"
  - name: "pnpm CLI Install"
    url: "https://pnpm.io/cli/install"
related: ["pnpm-workspaces-guide.md"]
author: "unknown"
contributors: []
---

# pnpm Package Manager Reference

pnpm is a fast, disk space-efficient package manager for JavaScript projects that is "up to 2x faster than npm" with efficient file storage through content-addressable mechanisms. ([pnpm Docs][2])

## Core Motivation

pnpm addresses three fundamental inefficiencies in npm and Yarn Classic: disk space waste, slow installation performance, and loose dependency management. ([pnpm Motivation][1])

### Disk Space Efficiency

pnpm uses a **content-addressable store** to dramatically reduce disk space consumption. Rather than duplicating dependencies across projects, it:

- Stores all packages in a single centralized location on disk
- Uses hard links to reference the same files across multiple projects
- Only adds new files to storage when versions differ (not entire packages)

"If you have 100 projects using a dependency, you will have 100 copies" with npm, versus pnpm's unified approach. This architecture enables significant storage savings proportional to the number of projects and shared dependencies. ([pnpm Motivation][1])

### Installation Performance

pnpm implements a **three-stage installation process** that overlaps operations:

1. Dependency resolution and fetching to the store
2. `node_modules` directory structure calculation
3. Linking dependencies via hard links

This parallel approach is considerably faster than traditional sequential installation methods used by npm and Yarn Classic, which resolve, fetch, and write all dependencies before proceeding to the next step. ([pnpm Motivation][1])

### Stricter Dependency Management

Unlike npm and Yarn Classic, pnpm creates a **non-flat `node_modules` structure**. Direct project dependencies appear as symlinks in the root, while transitive dependencies live in `.pnpm/`. This prevents accidental access to undeclared packages and enforces explicit dependency declarations in `package.json`. ([pnpm Motivation][1])

**Symlink Strategy**: Projects can only access declared dependencies at the root level. This encourages proper dependency management and reduces coupling. ([pnpm Motivation][1])

**Fallback Option**: Tools incompatible with symlinks can use the `nodeLinker: hoisted` setting to generate npm/Yarn-compatible flat structures when necessary. ([pnpm Motivation][1])

## Installation

### Prerequisites

"Node.js (at least v18.12)" is required unless using standalone scripts or @pnpm/exe. ([pnpm Installation][3])

pnpm supports Node.js 18, 20, 22, and 24. Earlier versions (14-16) have limited or no support depending on pnpm version. ([pnpm Installation][3])

### Installation Methods

**Standalone Scripts**:

POSIX systems:
```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

Windows PowerShell:
```powershell
Invoke-WebRequest https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression
```

([pnpm Installation][3])

**Corepack (Node.js 16.13+)**:

```bash
corepack enable pnpm
corepack use pnpm@latest-10
```

This adds a `packageManager` field to `package.json` to pin the version. ([pnpm Installation][3])

**Package Managers**:

```bash
# npm
npm install -g pnpm@latest-10

# Homebrew
brew install pnpm
```

Scoop, Chocolatey, Volta, and winget are also supported. ([pnpm Installation][3])

**@pnpm/exe Alternative**:

"packaged with Node.js into an executable, so it may be used on a system with no Node.js installed" ([pnpm Installation][3])

### Updating pnpm

```bash
pnpm self-update
```

([pnpm Installation][3])

## Basic Commands

### Install Dependencies

Install all project dependencies:

```bash
pnpm install
```

In workspaces, this "installs all dependencies in all the projects" unless `recursive-install` is set to `false`. ([pnpm Install][5])

**Common options**:

```bash
# Production dependencies only
pnpm install --prod

# Dev dependencies only
pnpm install --dev

# Skip optional dependencies
pnpm install --no-optional

# Offline mode (use cache only)
pnpm install --offline

# Frozen lockfile (CI mode, fails if updates needed)
pnpm install --frozen-lockfile

# Update lockfile without modifying node_modules
pnpm install --lockfile-only

# Force reinstall
pnpm install --force
```

([pnpm Install][5])

### Add Dependencies

Install packages and add to `package.json`:

```bash
# Add to dependencies
pnpm add <pkg>

# Add to devDependencies
pnpm add -D <pkg>

# Add to optionalDependencies
pnpm add -O <pkg>

# Global installation
pnpm add -g <pkg>

# Save exact version (no semver range)
pnpm add -E <pkg>
```

([pnpm Add][4])

### Installation Sources

**NPM Registry** (default):
```bash
pnpm add express@nightly
```

**JSR Registry** (v10.9.0+):
```bash
pnpm add jsr:@hono/hono@4
```

**Git Repositories**:
```bash
# Specific commit/branch/tag
pnpm add zkochan/is-negative

# With semver constraint
pnpm add zkochan/is-negative#semver:^1.0.0

# Subdirectory
pnpm add github:user/repo#path:packages/pkg
```

**Local Filesystem**:
```bash
# Tarball or directory (creates symlink)
pnpm add ./local-package
pnpm add ../my-package.tgz
```

**Remote Tarballs**:
```bash
pnpm add https://example.com/package.tgz
```

([pnpm Add][4])

### Other Common Commands

```bash
# Remove dependencies
pnpm remove <pkg>

# Update dependencies
pnpm update

# Run scripts
pnpm run <script>
pnpm <script>  # shorthand

# Execute binaries
pnpm exec <command>
pnpm dlx <pkg>  # execute without installing

# List dependencies
pnpm list

# Audit dependencies
pnpm audit
```

## Key Features

### Content-Addressable Store

All packages are stored in a centralized location and hard-linked into project `node_modules`. This provides:

- **Significant disk space savings** across multiple projects
- **Faster installations** by reusing already-downloaded packages
- **Integrity verification** through content addressing

([pnpm Motivation][1])

### Non-Flat node_modules

pnpm creates a structured `node_modules` directory where:

- Direct dependencies appear as symlinks at the root
- Transitive dependencies are stored in `.pnpm/`
- Packages can only access declared dependencies

This prevents "phantom dependencies" where code accidentally relies on undeclared packages. ([pnpm Motivation][1])

**Example structure**:
```
node_modules/
├── .pnpm/
│   ├── express@4.18.0/
│   └── lodash@4.17.21/
├── express -> .pnpm/express@4.18.0/node_modules/express
└── lodash -> .pnpm/lodash@4.17.21/node_modules/lodash
```

### Monorepo Support

Built-in support for multiple packages within a single repository through workspaces. ([pnpm Docs][2])

See [pnpm Workspaces Guide](pnpm-workspaces-guide.md) for detailed workspace documentation.

### Compatibility Modes

**Hoisted Mode**: For tools incompatible with symlinks:

```json
{
  ".npmrc": "node-linker=hoisted"
}
```

This generates npm/Yarn-compatible flat structures. ([pnpm Motivation][1])

## Configuration

### .npmrc

pnpm uses `.npmrc` files for configuration. Common settings:

```ini
# Hoist mode for compatibility
node-linker=hoisted

# Disable recursive workspace installs
recursive-install=false

# Store location
store-dir=~/.pnpm-store

# Shamefully hoist (legacy compatibility)
shamefully-hoist=true

# Public hoist pattern
public-hoist-pattern[]=*eslint*
public-hoist-pattern[]=*prettier*
```

### package.json

**pnpm-specific fields**:

```json
{
  "pnpm": {
    "overrides": {
      "lodash": "^4.17.21"
    },
    "packageExtensions": {
      "react": {
        "peerDependencies": {
          "react-dom": "*"
        }
      }
    }
  }
}
```

**Package manager pinning** (via Corepack):

```json
{
  "packageManager": "pnpm@10.9.0"
}
```

## Advanced Options

### Build and Script Execution

**Allow build scripts for specific packages**:
```bash
pnpm add <pkg> --allow-build
```

This permits postinstall scripts for specified packages. ([pnpm Add][4])

### Architecture Overrides (v10.14.0+)

Override native module platform specifications:

```bash
pnpm install --cpu=arm64 --os=darwin --libc=musl
```

([pnpm Install][5], [pnpm Add][4])

### Workspace-Specific Options

```bash
# Only add if found in workspace
pnpm add <pkg> --workspace

# Target specific workspace packages
pnpm add <pkg> --filter <package-name>

# Prevent root package installation (default behavior)
pnpm add <pkg>  # fails in workspace root without --ignore-workspace-root-check
```

([pnpm Add][4])

## Performance Characteristics

### Speed Comparison

pnpm is "up to 2x faster than npm" through parallelized installation stages. ([pnpm Docs][2])

### Disk Space Savings

Proportional savings based on:
- Number of projects using pnpm
- Number of shared dependencies across projects
- Dependency version overlap

Example: 100 projects using the same dependency version consume the disk space of one copy plus hard link overhead.

### Installation Stages

1. **Resolution and fetching**: Happens in parallel
2. **Structure calculation**: Determines `node_modules` layout
3. **Linking**: Creates hard links and symlinks

These stages overlap, unlike sequential npm/Yarn approaches. ([pnpm Motivation][1])

## Notable Adoptions

Major projects using pnpm include:

- Next.js
- Vite
- Vue
- Nuxt
- Material UI
- Astro

This demonstrates production-readiness across large-scale projects. ([pnpm Docs][2])

## Comparison to Other Package Managers

### vs npm

**Advantages**:
- 2x faster installation
- Significantly reduced disk usage
- Stricter dependency resolution (no phantom dependencies)
- Better monorepo support

**Considerations**:
- Non-flat `node_modules` may require compatibility adjustments
- Different lockfile format (`pnpm-lock.yaml`)

### vs Yarn Classic

**Advantages**:
- More efficient disk usage (Yarn Classic also duplicates)
- Faster installation through parallel stages
- Stricter dependency access control

**Considerations**:
- Different workspace configuration (`pnpm-workspace.yaml`)
- Workspace protocol syntax differs

### vs Yarn Berry (v2+)

**Advantages**:
- More compatible with existing tooling (Yarn Berry uses PnP by default)
- Simpler mental model (traditional `node_modules` structure, just optimized)

**Considerations**:
- Both support monorepos well
- Both have efficient disk usage strategies (different approaches)

## Troubleshooting

### Symlink Issues

**Problem**: Tools fail with symlinked dependencies

**Solution**: Use hoisted mode:
```ini
# .npmrc
node-linker=hoisted
```

### Phantom Dependencies

**Problem**: Code works with npm but fails with pnpm

**Solution**: Add missing dependencies to `package.json`:
```bash
pnpm add <missing-package>
```

This is actually correct behavior—pnpm exposes missing declarations.

### Peer Dependency Warnings

**Problem**: Excessive peer dependency warnings

**Solution**: Use `packageExtensions` to declare peer dependencies:
```json
{
  "pnpm": {
    "packageExtensions": {
      "problematic-package": {
        "peerDependencies": {
          "react": "*"
        }
      }
    }
  }
}
```

### Store Corruption

**Problem**: Unexpected installation failures

**Solution**: Verify and prune store:
```bash
pnpm store prune
```

Force reinstall if needed:
```bash
pnpm install --force
```

## Best Practices

### Project Setup

1. **Initialize with pnpm**: Use `pnpm init` for new projects
2. **Pin version**: Use Corepack to pin pnpm version in `package.json`
3. **Commit lockfile**: Always commit `pnpm-lock.yaml`
4. **Configure CI**: Use `pnpm install --frozen-lockfile` in CI

### Dependency Management

1. **Declare all dependencies**: Don't rely on transitive dependencies
2. **Use exact versions for critical deps**: `pnpm add -E <pkg>`
3. **Regular updates**: Run `pnpm update` periodically
4. **Audit security**: Use `pnpm audit` regularly

### Monorepo Projects

1. **Use workspaces**: Create `pnpm-workspace.yaml`
2. **Leverage workspace protocol**: Use `workspace:*` for internal deps
3. **Filter commands**: Use `--filter` for targeted operations
4. **Shared configurations**: Use catalogs for consistent versions

### Performance Optimization

1. **Offline mode**: Use `--offline` when possible
2. **Prefer offline**: Use `--prefer-offline` for faster installs
3. **Store location**: Configure store on fastest disk
4. **Prune regularly**: Run `pnpm store prune` to clean unused packages

## Migration

### From npm

1. **Remove npm artifacts**: Delete `node_modules` and `package-lock.json`
2. **Install pnpm**: Follow installation instructions
3. **Install dependencies**: Run `pnpm install`
4. **Update scripts**: Replace `npm` with `pnpm` in scripts
5. **Update CI**: Configure CI to use pnpm

### From Yarn

1. **Remove Yarn artifacts**: Delete `node_modules` and `yarn.lock`
2. **Convert workspace config**: Rename `workspaces` in `package.json` to `pnpm-workspace.yaml`
3. **Install dependencies**: Run `pnpm install`
4. **Update scripts**: Replace `yarn` with `pnpm` in scripts
5. **Review compatibility**: Check for Yarn-specific features that need replacement

## References

[1]: https://pnpm.io/motivation "pnpm Motivation"
[2]: https://pnpm.io/ "pnpm Documentation"
[3]: https://pnpm.io/installation "pnpm Installation"
[4]: https://pnpm.io/cli/add "pnpm CLI Add"
[5]: https://pnpm.io/cli/install "pnpm CLI Install"
