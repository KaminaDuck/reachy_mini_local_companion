---
title: "pnpm Workspaces Guide"
description: "Comprehensive guide to pnpm monorepo workspaces configuration and usage"
type: "config-reference"
tags: ["pnpm", "workspaces", "monorepo", "workspace-protocol", "filtering", "catalogs"]
category: "ts"
subcategory: "dev-tools"
version: "10.9"
last_updated: "2025-08-16"
status: "stable"
sources:
  - name: "pnpm Workspace YAML"
    url: "https://pnpm.io/pnpm-workspace_yaml"
  - name: "pnpm Workspaces"
    url: "https://pnpm.io/workspaces"
  - name: "pnpm Filtering"
    url: "https://pnpm.io/filtering"
  - name: "pnpm CLI Add"
    url: "https://pnpm.io/cli/add"
  - name: "pnpm CLI Install"
    url: "https://pnpm.io/cli/install"
related: ["pnpm-tool-reference.md"]
author: "unknown"
contributors: []
---

# pnpm Workspaces Guide

pnpm enables monorepo support through workspaces, requiring a `pnpm-workspace.yaml` file at the repository root. This allows multiple packages to coexist in a single repository with unified dependency management. ([pnpm Workspaces][2])

## Workspace Configuration

### pnpm-workspace.yaml

`pnpm-workspace.yaml` "defines the root of the workspace and enables you to include / exclude directories from the workspace." ([pnpm Workspace YAML][1])

**Basic configuration**:

```yaml
packages:
  # Direct subdirectories
  - 'apps/*'
  - 'packages/*'

  # Nested directories
  - 'components/**'

  # Specific directory
  - 'tools/cli'

  # Exclusions
  - '!**/test/**'
  - '!**/__fixtures__/**'
```

**Important**: "The root package is always included, even when custom location wildcards are used." ([pnpm Workspace YAML][1])

### Glob Pattern Syntax

- `packages/*` - Direct subdirectories only
- `packages/**` - All nested subdirectories
- `!pattern` - Exclude specific paths
- Specific paths like `my-app` are supported

([pnpm Workspace YAML][1])

## Workspace Protocol

The `workspace:` protocol is central to pnpm's monorepo capabilities. It ensures packages reference local workspace dependencies rather than external registry versions. ([pnpm Workspaces][2])

### Basic Usage

**Exact version reference**:
```json
{
  "dependencies": {
    "foo": "workspace:*"
  }
}
```

This references the exact version of `foo` in the workspace. ([pnpm Workspaces][2])

**Semver range references**:
```json
{
  "dependencies": {
    "foo": "workspace:~",
    "bar": "workspace:^"
  }
}
```

These use semver ranges while ensuring workspace resolution. ([pnpm Workspaces][2])

**Aliased references**:
```json
{
  "dependencies": {
    "bar": "workspace:foo@*"
  }
}
```

Creates an alias `bar` that points to workspace package `foo`. ([pnpm Workspaces][2])

**Path-based references**:
```json
{
  "dependencies": {
    "foo": "workspace:../foo"
  }
}
```

Reference packages using relative paths. ([pnpm Workspaces][2])

### Version Validation

"If you set `'foo': 'workspace:2.0.0'`, installation will fail because `'foo@2.0.0'` isn't present in the workspace." This prevents version mismatches within the monorepo. ([pnpm Workspaces][2])

### Publishing Behavior

When packages are published, workspace dependencies are automatically converted to standard semver ranges. For example, `"foo": "workspace:^"` becomes `"foo": "^1.5.0"` in the published `package.json`, allowing consumers to install published workspace packages normally while maintaining semver guarantees. ([pnpm Workspaces][2])

## Catalogs

Catalogs enable consistent version management across workspace packages. ([pnpm Workspace YAML][1])

### Single Catalog

Define shared dependency versions:

```yaml
packages:
  - 'packages/*'

catalog:
  react: ^18.2.0
  react-dom: ^18.2.0
  typescript: ^5.3.0
  '@types/react': ^18.2.0
```

**Usage in package.json**:
```json
{
  "dependencies": {
    "react": "catalog:",
    "react-dom": "catalog:"
  },
  "devDependencies": {
    "typescript": "catalog:",
    "@types/react": "catalog:"
  }
}
```

The `catalog:` protocol references the version defined in `pnpm-workspace.yaml`.

### Multiple Catalogs

Define different dependency sets for various use cases:

```yaml
packages:
  - 'packages/*'

catalogs:
  react18:
    react: ^18.2.0
    react-dom: ^18.2.0

  react17:
    react: ^17.0.2
    react-dom: ^17.0.2

  testing:
    vitest: ^1.0.0
    '@testing-library/react': ^14.0.0
```

**Usage in package.json**:
```json
{
  "dependencies": {
    "react": "catalog:react18",
    "react-dom": "catalog:react18"
  },
  "devDependencies": {
    "vitest": "catalog:testing",
    "@testing-library/react": "catalog:testing"
  }
}
```

([pnpm Workspace YAML][1])

### Benefits of Catalogs

1. **Centralized version management**: Update versions in one place
2. **Consistency**: Ensure all packages use compatible versions
3. **Multiple configurations**: Support different version sets for migration or testing
4. **Simplified updates**: Change catalog version to update all consuming packages

## Installing Dependencies

### Workspace-Wide Installation

Install all dependencies across all workspace packages:

```bash
pnpm install
```

This "installs all dependencies in all the projects" unless `recursive-install` is set to `false`. ([pnpm Install][5])

**Disable recursive installation**:
```ini
# .npmrc
recursive-install=false
```

### Adding Dependencies to Workspace Packages

**Add to specific package**:
```bash
pnpm add lodash --filter @myorg/package-a
```

**Add to multiple packages**:
```bash
pnpm add lodash --filter @myorg/*
```

**Add workspace dependency**:
```bash
# From package-b directory, add package-a as dependency
pnpm add @myorg/package-a

# Or using filter
pnpm add @myorg/package-a --filter @myorg/package-b
```

This automatically uses the `workspace:` protocol. ([pnpm Add][4])

**Only add if found in workspace**:
```bash
pnpm add <pkg> --workspace
```

This ensures the package exists in the workspace before adding. ([pnpm Add][4])

**Add to root workspace**:
```bash
pnpm add -w <pkg>
# or
pnpm add <pkg> --ignore-workspace-root-check
```

By default, adding to the root fails to prevent accidental root installations. ([pnpm Add][4])

## Filtering

pnpm's filtering feature allows you to "restrict commands to specific subsets of packages" using a rich selector syntax. The `--filter` (or `-F`) flag enables targeted command execution. ([pnpm Filtering][3])

### Package Name Filtering

**Exact match**:
```bash
pnpm --filter @babel/core test
```

**Pattern matching**:
```bash
# All @babel packages
pnpm --filter "@babel/*" build

# Packages ending in "core"
pnpm --filter "*core" test
```

([pnpm Filtering][3])

### Dependency Selection

**Package and all dependencies**:
```bash
pnpm --filter foo... test
```

Appending ellipsis (`...`) after a package name selects that package plus all dependencies. ([pnpm Filtering][3])

**Only dependencies (exclude package itself)**:
```bash
pnpm --filter foo^... build
```

The chevron variant (`foo^...`) selects only dependencies, excluding the package itself. ([pnpm Filtering][3])

### Dependent Packages

**Package and all dependents**:
```bash
pnpm --filter ...foo test
```

Prefixing with ellipsis (`...foo`) selects a package and all packages dependent on it. ([pnpm Filtering][3])

**Only dependents (exclude package itself)**:
```bash
pnpm --filter ...^foo build
```

The `...^foo` syntax selects only dependents. ([pnpm Filtering][3])

### Directory-Based Filtering

Filter by file system location:

```bash
# Current directory
pnpm --filter . build

# Specific directory pattern
pnpm --filter "./packages/**" test

# Combine with dependency selection
pnpm --filter "./apps/web..." build
```

Glob patterns are relative to the current directory and can combine with ellipsis/chevron operators. ([pnpm Filtering][3])

### Changed Files Filtering

Select packages modified since a specific commit or branch:

```bash
# Changed since origin/main
pnpm --filter "...[origin/main]" test

# Changed since specific commit
pnpm --filter "...[abc123]" build

# Changed packages and their dependents
pnpm --filter "...[origin/main]..." build
```

([pnpm Filtering][3])

### Multiple Filters

Combine filters with OR logic:

```bash
pnpm --filter ...foo --filter bar --filter baz... test
```

This runs tests on:
- Package `foo` and its dependents
- Package `bar`
- Package `baz` and its dependencies

([pnpm Filtering][3])

### Exclusions

Exclude packages using `!` prefix:

```bash
# Run on all packages except foo
pnpm --filter "!foo" test

# Run on all @myorg packages except admin
pnpm --filter "@myorg/*" --filter "!@myorg/admin" build
```

([pnpm Filtering][3])

### Advanced Filtering Options

**Production dependencies only**:
```bash
pnpm --filter-prod ...foo build
```

Functions like `--filter` but excludes devDependencies. ([pnpm Filtering][3])

**Test pattern matching**:
```bash
pnpm --filter "...[origin/main]" --test-pattern "*.spec.ts" test
```

Identifies test-related changes to refine dependent package selection. ([pnpm Filtering][3])

**Ignore file patterns**:
```bash
pnpm --filter "...[origin/main]" --changed-files-ignore-pattern "**/*.md" build
```

Excludes specific file patterns from change detection. ([pnpm Filtering][3])

**Fail if no match**:
```bash
pnpm --filter @myorg/critical-package --fail-if-no-match test
```

Causes CLI failure when no packages match filters. ([pnpm Filtering][3])

## Common Workspace Commands

### Build Commands

```bash
# Build all packages
pnpm -r build

# Build specific package and dependencies
pnpm --filter @myorg/app... build

# Build changed packages since main
pnpm --filter "...[origin/main]" build

# Build in topological order
pnpm -r --workspace-concurrency=1 build
```

### Test Commands

```bash
# Test all packages
pnpm -r test

# Test specific package
pnpm --filter @myorg/utils test

# Test changed packages and dependents
pnpm --filter "...[origin/main]..." test

# Parallel testing
pnpm -r --parallel test
```

### Lint and Format

```bash
# Lint all packages
pnpm -r lint

# Format specific packages
pnpm --filter "@myorg/*" format

# Lint changed files
pnpm --filter "...[origin/main]" lint
```

### Script Execution

```bash
# Run script across all packages
pnpm -r run custom-script

# Run in parallel
pnpm -r --parallel run dev

# Run with stream output
pnpm -r --stream run build
```

### Dependency Management

```bash
# Update all dependencies
pnpm -r update

# Update specific dependency across workspace
pnpm -r update lodash

# Add dependency to multiple packages
pnpm --filter "@myorg/*" add react

# Remove from specific package
pnpm --filter @myorg/app remove unused-dep
```

## Workspace Structure Best Practices

### Directory Layout

**Recommended structure**:
```
my-monorepo/
├── pnpm-workspace.yaml
├── package.json
├── .npmrc
├── apps/
│   ├── web/
│   │   └── package.json
│   └── api/
│       └── package.json
├── packages/
│   ├── ui/
│   │   └── package.json
│   ├── utils/
│   │   └── package.json
│   └── config/
│       └── package.json
└── tools/
    └── scripts/
        └── package.json
```

**Configuration**:
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

### Package Naming

**Use scoped packages**:
```json
{
  "name": "@myorg/package-name",
  "version": "1.0.0"
}
```

Benefits:
- Clear ownership
- Namespace isolation
- Easier filtering
- Publishable to npm

### Dependency Management Strategy

**1. Use catalogs for shared dependencies**:
```yaml
catalog:
  react: ^18.2.0
  typescript: ^5.3.0
```

**2. Use workspace protocol for internal deps**:
```json
{
  "dependencies": {
    "@myorg/utils": "workspace:*"
  }
}
```

**3. Pin critical dependencies**:
```json
{
  "dependencies": {
    "critical-lib": "1.2.3"
  }
}
```

**4. Separate dev dependencies**:
```json
{
  "devDependencies": {
    "typescript": "catalog:",
    "vitest": "catalog:testing"
  }
}
```

### Versioning Strategy

**1. Independent versioning**: Each package has its own version
```json
// packages/ui/package.json
{ "version": "2.1.0" }

// packages/utils/package.json
{ "version": "1.5.3" }
```

**2. Fixed versioning**: All packages share the same version
```json
// All packages
{ "version": "1.0.0" }
```

**3. Hybrid approach**: Related packages share versions, others independent

### Release Management

pnpm doesn't provide built-in versioning. Recommended tools:

**Changesets**:
```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
```

Handles versioning and supports pnpm workflows. ([pnpm Workspaces][2])

**Rush**:
Comprehensive monorepo tooling with pnpm support. ([pnpm Workspaces][2])

## Advanced Patterns

### Shared Configuration Packages

Create config packages for shared tooling:

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'config/*'
```

```json
// config/eslint-config/package.json
{
  "name": "@myorg/eslint-config",
  "version": "1.0.0",
  "main": "index.js"
}

// packages/app/package.json
{
  "devDependencies": {
    "@myorg/eslint-config": "workspace:*"
  }
}
```

### Workspace Scripts

Define scripts in root `package.json`:

```json
{
  "scripts": {
    "build": "pnpm -r --filter \"./packages/**\" build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "dev": "pnpm -r --parallel --filter \"./apps/**\" dev",
    "clean": "pnpm -r exec rm -rf dist node_modules",
    "release": "changeset publish"
  }
}
```

### Conditional Dependencies

Use catalogs for environment-specific dependencies:

```yaml
catalogs:
  prod:
    express: ^4.18.0
    pg: ^8.11.0

  dev:
    nodemon: ^3.0.0
    '@types/node': ^20.0.0
```

```json
{
  "dependencies": {
    "express": "catalog:prod",
    "pg": "catalog:prod"
  },
  "devDependencies": {
    "nodemon": "catalog:dev",
    "@types/node": "catalog:dev"
  }
}
```

### Parallel vs Sequential Execution

**Parallel** (faster, no order guarantee):
```bash
pnpm -r --parallel run build
```

**Sequential topological** (respects dependency order):
```bash
pnpm -r run build
```

**Limited concurrency**:
```bash
pnpm -r --workspace-concurrency=2 run build
```

### Private Packages

Prevent accidental publication:

```json
{
  "name": "@myorg/internal-utils",
  "version": "1.0.0",
  "private": true
}
```

## Troubleshooting

### Workspace Resolution Issues

**Problem**: Package not found in workspace

**Solution**: Verify package is listed in `pnpm-workspace.yaml` and has correct name:
```bash
pnpm list --depth 0
```

### Hoisting Issues

**Problem**: Package not accessible from root

**Solution**: Configure public hoisting:
```ini
# .npmrc
public-hoist-pattern[]=*eslint*
public-hoist-pattern[]=*prettier*
```

### Circular Dependencies

**Problem**: Packages depend on each other cyclically

**Solution**:
1. Refactor to remove circular dependency
2. Or use `workspace:*` protocol which handles it:
```json
// package-a
{ "dependencies": { "package-b": "workspace:*" } }

// package-b
{ "dependencies": { "package-a": "workspace:*" } }
```

### Workspace Protocol Not Resolving

**Problem**: `workspace:` dependencies not found during publish

**Solution**: Ensure packages are built before publishing:
```bash
pnpm -r build
pnpm -r publish
```

The workspace protocol is converted to semver during publish.

### Filter Not Matching

**Problem**: `--filter` command matches no packages

**Solution**:
1. Check package names: `pnpm list --depth 0`
2. Use `--fail-if-no-match` for debugging
3. Verify glob patterns are correct

## Notable Adoptions

Major projects using pnpm workspaces:

- **Next.js** - React framework monorepo
- **Vite** - Build tool and plugins
- **Vue** - Framework core and ecosystem
- **Nuxt** - Vue framework
- **Material UI** - Component library
- **Astro** - Static site generator

This demonstrates production-readiness across large-scale monorepos. ([pnpm Workspaces][2])

## Best Practices Summary

### Configuration

1. **Keep workspace config minimal**: Only include necessary packages
2. **Use exclusions liberally**: Exclude test and fixture directories
3. **Leverage catalogs**: Centralize version management
4. **Pin pnpm version**: Use `packageManager` field

### Development Workflow

1. **Install once**: Run `pnpm install` at root
2. **Filter commands**: Use `--filter` for targeted operations
3. **Build in order**: Let pnpm handle topological sorting
4. **Test changes**: Use `--filter "...[origin/main]..."` for affected packages

### CI/CD

1. **Frozen lockfile**: Use `pnpm install --frozen-lockfile`
2. **Cache store**: Cache `~/.pnpm-store` for faster builds
3. **Parallel jobs**: Split workspace packages across CI jobs
4. **Changed packages only**: Test only affected packages in PRs

### Publishing

1. **Use changesets**: Automate versioning and changelogs
2. **Build before publish**: Ensure all packages are built
3. **Verify workspace protocol**: Check protocol conversion
4. **Test published packages**: Verify in clean environment

## References

[1]: https://pnpm.io/pnpm-workspace_yaml "pnpm Workspace YAML"
[2]: https://pnpm.io/workspaces "pnpm Workspaces"
[3]: https://pnpm.io/filtering "pnpm Filtering"
[4]: https://pnpm.io/cli/add "pnpm CLI Add"
[5]: https://pnpm.io/cli/install "pnpm CLI Install"
