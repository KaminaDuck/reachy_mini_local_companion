---
title: "pnpm Reference Index"
description: "Reference documentation for pnpm package manager and workspaces"
type: "meta"
tags: ["index", "pnpm", "package-manager", "monorepo", "reference"]
category: "ts"
subcategory: "dev-tools"
version: "1.0"
last_updated: "2025-08-16"
status: "stable"
sources: []
related: ["pnpm-tool-reference.md", "pnpm-workspaces-guide.md"]
author: "unknown"
contributors: []
---

# pnpm Reference Index

Comprehensive reference documentation for pnpm, a fast, disk space-efficient package manager with built-in monorepo workspace support.

## Documentation Files

### [pnpm Package Manager Reference](pnpm-tool-reference.md)
Complete guide to pnpm package manager, covering:
- Core motivation (disk efficiency, performance, strict dependencies)
- Installation methods (standalone scripts, Corepack, package managers)
- Basic commands (install, add, remove, update)
- Content-addressable store architecture
- Non-flat node_modules structure
- Configuration options (.npmrc, package.json)
- Performance characteristics (2x faster than npm)
- Comparison to npm and Yarn
- Migration guides
- Best practices and troubleshooting

### [pnpm Workspaces Guide](pnpm-workspaces-guide.md)
Comprehensive guide to pnpm monorepo workspaces, covering:
- Workspace configuration (pnpm-workspace.yaml)
- Workspace protocol usage (workspace:*, workspace:^, workspace:~)
- Catalogs for centralized version management
- Filtering capabilities (package names, dependencies, dependents, directories)
- Changed files filtering for CI optimization
- Common workspace commands (build, test, lint)
- Workspace structure best practices
- Advanced patterns (shared configs, parallel execution)
- Release management (Changesets, Rush)
- Production examples (Next.js, Vite, Vue, Nuxt, Material UI, Astro)

## External Resources

- [Official pnpm Documentation](https://pnpm.io/)
- [pnpm Motivation](https://pnpm.io/motivation)
- [pnpm Installation Guide](https://pnpm.io/installation)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [pnpm Filtering](https://pnpm.io/filtering)
- [GitHub Repository](https://github.com/pnpm/pnpm)
- [pnpm CLI Reference](https://pnpm.io/cli/add)

## Quick Start

### Installation

```bash
# Standalone script (POSIX)
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Via Corepack
corepack enable pnpm
corepack use pnpm@latest-10

# Via npm
npm install -g pnpm@latest-10
```

### Basic Usage

```bash
# Install dependencies
pnpm install

# Add dependency
pnpm add <package>

# Add dev dependency
pnpm add -D <package>

# Run scripts
pnpm run <script>

# Update dependencies
pnpm update
```

### Workspace Setup

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'

catalog:
  react: ^18.2.0
  typescript: ^5.3.0
```

```bash
# Install all workspace dependencies
pnpm install

# Add dependency to specific package
pnpm add lodash --filter @myorg/app

# Build all packages
pnpm -r build

# Test changed packages
pnpm --filter "...[origin/main]..." test
```

## Key Features

- **Fast**: Up to 2x faster than npm through parallelized installation
- **Disk Efficient**: Content-addressable store with hard links saves significant disk space
- **Strict**: Non-flat node_modules prevents phantom dependencies
- **Monorepo Ready**: Built-in workspace support with powerful filtering
- **Compatible**: Hoisted mode for legacy tool compatibility
- **Catalog System**: Centralized dependency version management
- **Workspace Protocol**: Type-safe internal package references

## Notable Adoptions

Major projects using pnpm:
- Next.js (React framework monorepo)
- Vite (Build tool ecosystem)
- Vue (Framework and ecosystem)
- Nuxt (Vue framework)
- Material UI (Component library)
- Astro (Static site generator)
