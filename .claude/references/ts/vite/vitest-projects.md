---
title: "Vitest Projects Configuration"
description: "Multi-configuration testing with Vitest Projects for monorepos and complex setups"
type: "config-reference"
tags: ["vitest", "testing", "monorepo", "configuration", "projects", "workspace", "vite", "typescript"]
category: "frontend"
subcategory: "testing"
version: "4.0.6"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "Vitest Projects Guide"
    url: "https://vitest.dev/guide/workspace"
  - name: "Vitest Configuration Reference"
    url: "https://vitest.dev/config/"
related: ["vitest.md", "vitest-browser-playwright.md"]
author: "unknown"
contributors: []
---

# Vitest Projects Configuration

Vitest Projects (formerly called "workspace," deprecated since v3.2) enables running multiple test configurations within a single Vitest process. ([Vitest Projects Guide][1]) This feature is particularly useful for monorepo setups but can also be used to run tests with different configurations such as `resolve.alias`, `plugins`, or `test.browser`. ([Vitest Projects Guide][1])

## Overview

### What Are Projects?

Projects allow developers to define multiple testing environments or configurations that share a single Vitest process. ([Vitest Projects Guide][1]) Each project can have its own:

- Test environment (`jsdom`, `node`, `happy-dom`, browser mode)
- Setup files and global configuration
- Include/exclude patterns
- Plugins and resolvers
- Test-specific options

### When to Use Projects

Projects are ideal for:

- **Monorepos** - Testing multiple packages with different configurations
- **Multi-environment testing** - Running the same tests in different environments (e.g., browser and Node)
- **Separated test types** - Unit, integration, and E2E tests with different setups
- **Cross-browser testing** - Same tests in different browser configurations
- **Performance optimization** - Isolating slow tests from fast ones

## Defining Projects

### Glob Pattern Syntax

The simplest way to define projects is using glob patterns in your root `vitest.config.ts`: ([Vitest Projects Guide][1])

```typescript
export default defineConfig({
  test: {
    projects: ['packages/*'],
  },
})
```

Vitest treats each matching folder as a separate project, even if it doesn't have a config file. ([Vitest Projects Guide][1])

### Valid Config Files

Projects can reference folders or config files matching these patterns: ([Vitest Projects Guide][1])

- `vitest.config.{js,ts,mjs,mts,cjs,cts}`
- `vite.config.{js,ts,mjs,mts,cjs,cts}`
- `vitest.{unit,integration}.config.{js,ts}`
- `vite.{e2e,component}.config.{js,ts}`

### Exclusion Patterns

Use negation patterns to exclude specific folders: ([Vitest Projects Guide][1])

```typescript
projects: ['packages/*', '!packages/excluded']
```

### Nested Structures

Use bracket notation to match specific depths without including parent folders: ([Vitest Projects Guide][1])

```typescript
projects: [
  'packages/!(business)',    // excludes "business" package
  'packages/business/*',      // includes business subfolders
]
```

### Inline Configuration

Projects support mixed syntax combining glob patterns with inline configs: ([Vitest Projects Guide][1])

```typescript
export default defineConfig({
  test: {
    projects: [
      'packages/*',
      {
        extends: true,
        test: {
          name: 'happy-dom',
          environment: 'happy-dom',
          include: ['tests/**/*.{browser}.test.{ts,js}'],
        }
      }
    ]
  }
})
```

### Example: Browser and Node Projects

```typescript
import { defineConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    projects: [
      {
        test: {
          name: 'browser',
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [{ browser: 'chromium' }]
          },
          include: ['tests/**/*.browser.test.ts']
        }
      },
      {
        test: {
          name: 'node',
          environment: 'node',
          include: ['tests/**/*.node.test.ts']
        }
      }
    ]
  }
})
```

## Project Naming

### Naming Requirements

All projects must have unique names; otherwise, Vitest will throw an error. ([Vitest Projects Guide][1])

### Auto-Generated Names

If names aren't explicitly provided, Vitest auto-assigns them: ([Vitest Projects Guide][1])

1. Numbers (for inline configurations without names)
2. Package name from `package.json`
3. Folder name (as fallback)

### Custom Labels

Inline configs can use custom labels for better visualization: ([Vitest Projects Guide][1])

```typescript
{
  test: {
    name: 'node',
    label: { name: 'node', color: 'green' }
  }
}
```

## Configuration Inheritance

### The `extends` Property

Projects can inherit configuration from the root config using `extends`: ([Vitest Projects Guide][1])

- **`extends: true`** - Inherits root config options like plugins and pools
- **`extends: false`** (default) - Doesn't inherit root configuration

```typescript
export default defineConfig({
  plugins: [react()],
  test: {
    pool: 'threads',
    projects: [
      {
        extends: true,  // Inherits plugins and pool
        test: { name: 'unit' }
      },
      {
        extends: false,  // Doesn't inherit
        test: { name: 'integration' }
      }
    ]
  }
})
```

### Manual Merging

For fine-grained control, use `mergeConfig()`: ([Vitest Projects Guide][1])

```typescript
import { defineConfig, mergeConfig } from 'vitest/config'
import baseConfig from './vite.config'

export default defineConfig({
  test: {
    projects: [
      mergeConfig(baseConfig, {
        test: { name: 'custom', environment: 'jsdom' }
      })
    ]
  }
})
```

## Using `defineProject`

For type safety in project-specific config files, use `defineProject` instead of `defineConfig`: ([Vitest Projects Guide][1])

```typescript
// packages/unit/vitest.config.ts
import { defineProject } from 'vitest/config'

export default defineProject({
  test: {
    environment: 'jsdom',
    name: 'unit-tests'
  }
})
```

This prevents using unsupported options like `reporters` or `coverage` at the project level. ([Vitest Projects Guide][1])

## Running Tests

### All Projects

Run all projects with the standard test command: ([Vitest Projects Guide][1])

```bash
npm run test
```

### Specific Projects

Filter by project name using the `--project` flag: ([Vitest Projects Guide][1])

```bash
# Single project
npm run test --project e2e

# Multiple projects
npm run test --project e2e --project unit

# Using vitest directly
vitest --project browser --project node
```

### Project Ordering

Control project execution order with `sequence.groupOrder` (v3.2.0+): ([Vitest Configuration][2])

```typescript
export default defineConfig({
  test: {
    projects: [
      { test: { name: 'unit', sequence: { groupOrder: 1 } } },
      { test: { name: 'integration', sequence: { groupOrder: 2 } } },
    ]
  }
})
```

Projects with the same group number run simultaneously; lower numbers run first. ([Vitest Configuration][2])

## Configuration Constraints

### Root-Only Options

The following options cannot be configured at the project level (marked with `*` in docs): ([Vitest Configuration][2])

**Test Execution:**
- `update`, `watch`, `watchTriggerPatterns`
- `forceRerunTriggers`
- `testNamePattern`, `open`, `api`

**Reporting:**
- `reporters`, `outputFile`
- `onConsoleLog`, `onStackTrace`, `onUnhandledError`

**Coverage:**
- All `coverage.*` options (process-wide only)

**Snapshots:**
- `snapshotFormat`, `snapshotSerializers`, `resolveSnapshotPath`

**Global Settings:**
- `allowOnly`, `dangerouslyIgnoreUnhandledErrors`, `passWithNoTests`
- `sequence.sequencer`, `sequence.seed`
- `projects`, `typecheck`, `slowTestThreshold`
- `diff`, `teardownTimeout`, `silent`, `printConsoleTrace`
- `attachmentsDir`

**Pool Configuration:**
- `pool`, `poolOptions`, `fileParallelism`
- `maxWorkers`, `minWorkers`

### Project-Specific Options

Projects can configure:

- `environment` - Test environment (jsdom, node, happy-dom, custom)
- `browser` - Browser mode settings
- `globals` - Enable global test APIs
- `setupFiles` - Setup file paths
- `include`, `exclude` - Test file patterns
- `testTimeout`, `hookTimeout` - Timeout settings
- `isolate` - Test isolation
- `name` - Project identifier
- Plugin configurations specific to the project

## Root Config Behavior

The root `vitest.config` file is NOT treated as a project unless explicitly specified in the projects array. ([Vitest Projects Guide][1])

**What the root config controls:**

- Global options (reporters, coverage)
- Plugin hooks (apply, config, configResolved, configureServer) execute for all projects

**To make root config a project:**

```typescript
export default defineConfig({
  test: {
    projects: [
      './',  // Root as a project
      'packages/*'
    ]
  }
})
```

## Coverage with Projects

Coverage configuration applies globally across all projects. ([Vitest Configuration][2])

**Automatic exclusions:**

Vitest automatically adds each project's test files (`include` patterns) to coverage's default `exclude` patterns, ensuring proper isolation. ([Vitest Configuration][2])

**Configuration:**

```typescript
export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: 'v8',
      include: ['src/**/*.ts'],
      // Project test files excluded automatically
    },
    projects: [
      { test: { name: 'unit' } },
      { test: { name: 'integration' } }
    ]
  }
})
```

## Best Practices

### 1. Use Explicit Names

Always provide explicit names for inline configurations: ([Vitest Projects Guide][1])

```typescript
// Good
{ test: { name: 'browser-chrome' } }

// Avoid
{ test: { } }  // Auto-assigned number
```

### 2. Leverage `extends` for Shared Config

Use `extends: true` to avoid repeating common options: ([Vitest Projects Guide][1])

```typescript
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    projects: [
      { extends: true, test: { name: 'unit' } },
      { extends: true, test: { name: 'integration' } }
    ]
  }
})
```

### 3. Use `defineProject` for Type Safety

In project-specific config files, use `defineProject`: ([Vitest Projects Guide][1])

```typescript
// packages/ui/vitest.config.ts
import { defineProject } from 'vitest/config'

export default defineProject({
  test: { environment: 'jsdom' }
})
```

### 4. Organize by Test Type

Structure projects around test types:

```typescript
projects: [
  { test: { name: 'unit', include: ['**/*.unit.test.ts'] } },
  { test: { name: 'integration', include: ['**/*.int.test.ts'] } },
  { test: { name: 'e2e', include: ['**/*.e2e.test.ts'] } }
]
```

### 5. Separate Slow Tests

Isolate slow tests for parallel execution:

```typescript
projects: [
  {
    test: {
      name: 'fast',
      include: ['**/*.test.ts'],
      exclude: ['**/*.slow.test.ts']
    }
  },
  {
    test: {
      name: 'slow',
      include: ['**/*.slow.test.ts'],
      testTimeout: 60000
    }
  }
]
```

## Migration from Workspace

### Terminology Change

The "workspace" feature was renamed to "projects" in v3.2 but maintains identical functionality. ([Vitest Projects Guide][1])

### Migration Steps

**Before (workspace file):**

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    workspace: './vitest.workspace.js',
  }
})

// vitest.workspace.js
export default [
  'packages/*'
]
```

**After (projects in config):**

```typescript
// vitest.config.ts only
export default defineConfig({
  test: {
    projects: ['packages/*']
  }
})
```

### Breaking Changes

- Cannot specify a separate file as the source of projects
- Must define projects inline in the main config file
- All functionality otherwise identical

## Common Patterns

### Monorepo Pattern

```typescript
export default defineConfig({
  test: {
    projects: [
      'packages/*',
      '!packages/deprecated'
    ]
  }
})
```

### Multi-Environment Pattern

```typescript
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    projects: [
      {
        test: {
          name: 'browser',
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [
              { browser: 'chromium' },
              { browser: 'firefox' }
            ]
          }
        }
      },
      {
        test: {
          name: 'node',
          environment: 'node'
        }
      }
    ]
  }
})
```

### Test Type Separation Pattern

```typescript
export default defineConfig({
  test: {
    projects: [
      {
        test: {
          name: 'unit',
          include: ['tests/unit/**/*.test.ts'],
          environment: 'node'
        }
      },
      {
        test: {
          name: 'integration',
          include: ['tests/integration/**/*.test.ts'],
          environment: 'jsdom',
          testTimeout: 10000
        }
      }
    ]
  }
})
```

## Troubleshooting

### Project Not Found

**Error:** `No projects matched the filter "project-name"`

**Solutions:**

1. Verify project has a unique `name` property
2. Check glob patterns match existing directories
3. Ensure config files exist in referenced paths
4. Validate project name spelling in CLI command

### Configuration Not Applied

**Symptoms:** Project-specific config seems ignored

**Solutions:**

1. Check if option is marked with `*` (root-only)
2. Verify `extends: true` if inheriting root config
3. Use `defineProject` for type checking
4. Ensure option is in `test` property, not root

### Tests Running Twice

**Symptoms:** Same tests execute multiple times

**Solutions:**

1. Check for overlapping `include` patterns
2. Verify root config isn't also a project
3. Review glob pattern exclusions
4. Ensure projects have unique names

### Coverage Not Working

**Symptoms:** Coverage reports empty or incomplete

**Solutions:**

1. Configure coverage at root level only
2. Verify `include` patterns in coverage config
3. Check that test files are auto-excluded
4. Run with `--coverage` flag

## References

[1]: https://vitest.dev/guide/workspace "Vitest Projects Guide"
[2]: https://vitest.dev/config/ "Vitest Configuration Reference"
