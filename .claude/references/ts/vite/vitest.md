---
title: "Vitest Testing Framework Reference"
description: "Vitest next-generation testing framework powered by Vite with Jest compatibility"
type: "tool-reference"
tags: ["vitest", "testing", "vite", "jest", "unit-testing", "coverage", "typescript", "esm"]
category: "frontend"
subcategory: "testing"
version: "4.0.6"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Vitest Documentation"
    url: "https://vitest.dev/"
  - name: "Vitest Guide"
    url: "https://vitest.dev/guide/"
  - name: "Vitest Features"
    url: "https://vitest.dev/guide/features"
  - name: "Vitest Configuration"
    url: "https://vitest.dev/config/"
related: ["vite-7.md", "../react/react-19.md", "vitest-browser-playwright.md"]
author: "unknown"
contributors: []
---

# Vitest Testing Framework Reference

Vitest is a next generation testing framework powered by Vite, designed for speed and compatibility. ([Vitest Guide][2]) It is positioned as a "Vite-native testing framework" that emphasizes performance and developer experience. ([Vitest Documentation][1])

## Overview

Vitest leverages Vite's build tooling to provide a modern testing experience with unified configuration. ([Vitest Guide][2]) The framework reuses Vite's configuration and plugins, maintaining consistency between your application and test environments, though using Vite configuration isn't mandatory. ([Vitest Documentation][1])

### Current Version

Version 4.0.6 is the latest stable release, with access to unreleased builds and historical versions (v0.x through v3.x). ([Vitest Documentation][1])

**License**: MIT License, maintained by VoidZero Inc. and Vitest contributors since 2021. ([Vitest Documentation][1])

## Key Features

### Vite Integration

Vitest reuses Vite's configuration and plugins, maintaining consistency between your application and test environments. ([Vitest Documentation][1]) "Vitest will read it to match with the plugins and setup as your Vite app" when using shared configuration files, ensuring consistency across development and testing environments. ([Vitest Configuration][4])

### Jest Compatibility

The framework provides familiar tools like expectations, snapshot testing, and coverage analysis. ([Vitest Documentation][1]) This compatibility makes migration from Jest "straightforward." ([Vitest Documentation][1])

Vitest provides "Chai built-in for assertions with Jest `expect`-compatible APIs." ([Vitest Features][3]) This dual approach gives developers flexibility in assertion syntax while maintaining Jest compatibility.

### Performance

The framework includes "smart & instant watch mode" that intelligently reruns only affected tests—similar to how hot module replacement works in development. ([Vitest Documentation][1]) Smart watch mode provides instant feedback, similar to HMR for tests. ([Vitest Features][3])

Tests run in multiple processes by default using `node:child_process`, with optional thread-based execution via `node:worker_threads` for improved performance. ([Vitest Features][3]) Environment isolation prevents mutations from affecting other test files. ([Vitest Features][3])

### Language Support

Built-in support for ESM, TypeScript, and JSX is powered by esbuild, eliminating configuration overhead. ([Vitest Documentation][1])

## Requirements

Vitest needs Vite ≥v6.0.0 and Node ≥v20.0.0. ([Vitest Guide][2])

## Installation

Add Vitest to projects using your preferred package manager: ([Vitest Guide][2])

```bash
# npm
npm install -D vitest

# yarn
yarn add -D vitest

# pnpm
pnpm add -D vitest

# bun
bun add -D vitest
```

You can run tests without installing locally by using `npx vitest`, though installing in your project is recommended. ([Vitest Guide][2])

## Getting Started

### Writing Your First Test

"By default, tests must contain `.test.` or `.spec.` in their file name." ([Vitest Guide][2])

**Example source file (`sum.js`):**
```javascript
export function sum(a, b) {
  return a + b;
}
```

**Example test file (`sum.test.js`):**
```javascript
import { test, expect } from 'vitest';
import { sum } from './sum.js';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Adding Test Script

Add a test script to `package.json`: ([Vitest Guide][2])

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

### Running Tests

Execute tests using: ([Vitest Guide][2])

```bash
npm run test
```

For single runs without watching: ([Vitest Guide][2])

```bash
vitest run
```

## Configuration

### Configuration Files

Vitest reads your `vite.config.ts` automatically, making plugins and aliases work out-of-the-box. ([Vitest Guide][2]) You can:

1. Create a dedicated `vitest.config.ts` for test-specific settings - takes priority and overrides `vite.config.ts` ([Vitest Configuration][4])
2. Add a `test` property to `vite.config.ts` ([Vitest Configuration][4])
3. Use the `--config` CLI flag ([Vitest Guide][2]) ([Vitest Configuration][4])
4. Set `process.env.VITEST` conditionally in your Vite config ([Vitest Guide][2])

The framework supports multiple config file formats (`.js`, `.mjs`, `.cjs`, `.ts`, `.cts`, `.mts`) but not `.json`. ([Vitest Guide][2])

### Recommended Configuration Structure

The recommended approach uses `defineConfig` from `vitest/config`: ([Vitest Configuration][4])

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // configuration options here
  },
});
```

### Essential Test Options

**File Patterns:** ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    include: ['**/*.{test,spec}.?(c|m)[jt]s?(x)'],
    exclude: ['**/node_modules/**', '**/.git/**'],
  },
});
```

**Environment:** ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    environment: 'node', // 'node', 'jsdom', 'happy-dom', 'edge-runtime'
    globals: false, // Enable global test APIs like Jest
  },
});
```

**Performance & Execution:** ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    pool: 'forks', // 'threads', 'forks', 'vmThreads', 'vmForks'
    maxWorkers: 4,
    fileParallelism: true,
    testTimeout: 5000, // milliseconds
  },
});
```

### Coverage Configuration

Enable with `coverage.enabled: true` and configure: ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: 'v8', // 'v8' or 'istanbul'
      reporter: ['text', 'html', 'json', 'lcov'],
      include: ['src/**/*.{js,ts,jsx,tsx}'],
      exclude: ['**/*.test.{js,ts,jsx,tsx}'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

### Setup & Teardown

([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    setupFiles: ['./tests/setup.ts'], // Runs before each test file
    globalSetup: './tests/global-setup.ts', // Project-level initialization
  },
});
```

**Global setup example:**
```typescript
// tests/global-setup.ts
export function setup() {
  console.log('Global setup');
  // Initialize database, start servers, etc.
}

export function teardown() {
  console.log('Global teardown');
  // Clean up resources
}
```

## Core Testing Capabilities

### Test Execution & Organization

**Test Control:** ([Vitest Features][3])
- Test filtering to narrow down which tests run, speeding up development cycles
- Concurrent test execution using `.concurrent` markers
- Sequential and parallel test organization within suites
- Support for `.skip`, `.only`, and `.todo` modifiers

```typescript
import { test, describe } from 'vitest';

describe('Math operations', () => {
  test('addition', () => {
    expect(1 + 1).toBe(2);
  });

  test.skip('skipped test', () => {
    // This test will be skipped
  });

  test.only('only this test runs', () => {
    // Only this test executes when .only is present
  });

  test.todo('implement later');

  test.concurrent('runs concurrently 1', async () => {
    // Runs in parallel with other concurrent tests
  });

  test.concurrent('runs concurrently 2', async () => {
    // Runs in parallel with other concurrent tests
  });
});
```

### Assertions & Expectations

Vitest provides "Chai built-in for assertions with Jest `expect`-compatible APIs." ([Vitest Features][3])

```typescript
import { expect } from 'vitest';

// Basic assertions
expect(value).toBe(expected);
expect(value).toEqual(expected);
expect(value).toBeTruthy();
expect(value).toBeNull();
expect(value).toBeUndefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeCloseTo(0.3, 2);

// Strings
expect('hello world').toContain('world');
expect('hello').toMatch(/^h/);

// Arrays
expect([1, 2, 3]).toContain(2);
expect([1, 2, 3]).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toMatchObject({ key: 'value' });

// Functions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('error message');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

### Mocking & Spying

The framework includes Tinyspy for mocking functionality with Jest-compatible APIs through the `vi` object. ([Vitest Features][3])

```typescript
import { vi, test, expect } from 'vitest';

// Mock functions
const mockFn = vi.fn();
mockFn('arg');
expect(mockFn).toHaveBeenCalledWith('arg');

// Spy on methods
const obj = { method: () => 'original' };
const spy = vi.spyOn(obj, 'method');
obj.method();
expect(spy).toHaveBeenCalled();

// Mock modules
vi.mock('./module', () => ({
  exportedFunction: vi.fn(() => 'mocked'),
}));

// Mock timers
vi.useFakeTimers();
setTimeout(() => console.log('delayed'), 1000);
vi.advanceTimersByTime(1000);
vi.useRealTimers();

// Mock dates
vi.setSystemTime(new Date('2025-01-01'));
expect(new Date().getFullYear()).toBe(2025);
vi.useRealTimers();
```

**DOM & Browser APIs:** ([Vitest Features][3])
- Supports happy-dom or jsdom for DOM mocking
- Configurable environment selection in test configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom', // or 'happy-dom'
  },
});
```

## Advanced Features

### Snapshot Testing

Vitest supports "Jest-compatible snapshot support" for testing rendered output consistency. ([Vitest Features][3])

```typescript
import { test, expect } from 'vitest';

test('snapshot test', () => {
  const data = {
    name: 'John',
    age: 30,
    emails: ['john@example.com'],
  };

  expect(data).toMatchSnapshot();
});

// Inline snapshots
test('inline snapshot', () => {
  expect({ name: 'John' }).toMatchInlineSnapshot(`
    {
      "name": "John",
    }
  `);
});
```

**Snapshot Management:** ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    snapshotFormat: {
      printBasicPrototype: false,
      escapeString: false,
    },
    resolveSnapshotPath: (path, extension) => {
      return path.replace(/\.test\.ts$/, `.snap${extension}`);
    },
  },
});
```

### Code Coverage

**Native coverage via v8** and **instrumented coverage via Istanbul** with easy CLI integration using the `--coverage` flag. ([Vitest Features][3])

```bash
# Run tests with coverage
vitest run --coverage

# Watch mode with coverage
vitest --coverage
```

Coverage configuration: ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

### Browser Mode

Run component tests directly in browsers using Playwright or WebdriverIO for realistic testing environments. ([Vitest Features][3])

```typescript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      name: 'chromium', // or 'firefox', 'webkit'
      provider: 'playwright', // or 'webdriverio'
      headless: true,
    },
  },
});
```

### Type Testing

Built-in type regression testing using the expect-type package, allowing developers to verify TypeScript type correctness. ([Vitest Features][3])

```typescript
import { test, expectTypeOf } from 'vitest';

test('type checking', () => {
  expectTypeOf({ a: 1 }).toEqualTypeOf<{ a: number }>();
  expectTypeOf('string').toBeString();
  expectTypeOf(123).toBeNumber();
  expectTypeOf([1, 2, 3]).toMatchTypeOf<number[]>();
});
```

### In-Source Testing

Rust-inspired pattern allowing tests within source files alongside implementations, enabling testing of private states without exports. ([Vitest Features][3])

```typescript
// src/calculator.ts
function add(a: number, b: number) {
  return a + b;
}

if (import.meta.vitest) {
  const { test, expect } = import.meta.vitest;

  test('add', () => {
    expect(add(1, 2)).toBe(3);
  });
}
```

Enable in configuration:
```typescript
export default defineConfig({
  test: {
    includeSource: ['src/**/*.{js,ts}'],
  },
});
```

### Benchmarking

Performance comparison capabilities via Tinybench integration. ([Vitest Features][3])

```typescript
import { bench, describe } from 'vitest';

describe('sorting algorithms', () => {
  bench('sort', () => {
    [3, 2, 1].sort();
  });

  bench('sort with compare function', () => {
    [3, 2, 1].sort((a, b) => a - b);
  });
});
```

### Test Sharding

Distribute tests across machines using `--shard` flag for CI pipelines. ([Vitest Features][3])

```bash
# Run shard 1 of 3
vitest run --shard=1/3

# Run shard 2 of 3
vitest run --shard=2/3

# Run shard 3 of 3
vitest run --shard=3/3
```

## Advanced Configuration Options

### Mocking Defaults

Auto-reset mocks between tests: ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    clearMocks: true,
    mockReset: true,
    restoreMocks: true,
  },
});
```

### Test Organization

Control test ordering, randomization, and hook execution: ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    sequence: {
      shuffle: true, // Randomize test order
      seed: 12345, // Reproducible randomization
      concurrent: false,
      hooks: 'parallel', // 'parallel' or 'stack'
    },
  },
});
```

### Multi-Project Configuration

Isolated settings for multiple projects: ([Vitest Configuration][4])

```typescript
export default defineConfig({
  test: {
    projects: [
      {
        name: 'unit',
        test: {
          include: ['tests/unit/**/*.test.ts'],
          environment: 'node',
        },
      },
      {
        name: 'integration',
        test: {
          include: ['tests/integration/**/*.test.ts'],
          environment: 'jsdom',
        },
      },
    ],
  },
});
```

### Sharing Data Across Tests

Share serializable data via `provide` and `inject`: ([Vitest Configuration][4])

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    provide: {
      apiUrl: 'https://api.example.com',
    },
  },
});

// In tests
import { inject } from 'vitest';

const apiUrl = inject('apiUrl');
```

## Best Practices

### Configuration Management

1. **Use dedicated vitest.config.ts**: Keep test configuration separate from build configuration
2. **Share common settings**: Use Vite config for shared plugins and aliases
3. **Set environment conditionally**: Use `process.env.VITEST` to detect test runs
4. **Enable globals cautiously**: Prefer explicit imports for better IDE support

### Test Organization

1. **Descriptive test names**: Use clear, behavior-focused descriptions
2. **Group related tests**: Use `describe` blocks for logical organization
3. **One assertion per test**: Keep tests focused and easier to debug
4. **Use test.concurrent sparingly**: Only for truly independent async tests

### Mocking Strategy

1. **Mock at module boundaries**: Mock external dependencies, not internal functions
2. **Reset mocks between tests**: Enable `clearMocks`, `mockReset`, `restoreMocks`
3. **Avoid over-mocking**: Test real implementations when possible
4. **Use spies for verification**: Verify calls without changing behavior

### Performance Optimization

1. **Use test filtering**: Run only affected tests during development
2. **Enable parallel execution**: Let Vitest run tests concurrently
3. **Optimize setup**: Move expensive setup to `globalSetup`
4. **Use coverage selectively**: Don't run coverage on every dev cycle

### Coverage Goals

1. **Set realistic thresholds**: Start with achievable targets and improve
2. **Focus on critical paths**: Prioritize business logic coverage
3. **Exclude generated code**: Don't measure coverage for build outputs
4. **Review uncovered lines**: Use HTML reporter to identify gaps

### Browser Testing

1. **Use browser mode for DOM-heavy tests**: Test actual browser behavior
2. **Prefer headless mode in CI**: Faster execution without UI
3. **Test cross-browser**: Validate in Chrome, Firefox, Safari when needed
4. **Mock network requests**: Use MSW or similar for API mocking

## Troubleshooting

### Configuration Issues

**Issue**: Tests not found

**Solution**: Check file patterns in `include` option:
```typescript
export default defineConfig({
  test: {
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
  },
});
```

### Import Errors

**Issue**: Cannot find module or import errors

**Solution**: Ensure Vite config includes proper aliases and resolvers:
```typescript
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Coverage Not Working

**Issue**: Coverage reports show 0%

**Solution**: Install coverage provider:
```bash
# For v8
npm install -D @vitest/coverage-v8

# For istanbul
npm install -D @vitest/coverage-istanbul
```

### Slow Test Execution

**Issue**: Tests run slowly

**Solution**:
1. Check test timeout settings
2. Enable parallel execution
3. Increase max workers
4. Profile tests to find bottlenecks

```typescript
export default defineConfig({
  test: {
    pool: 'threads',
    maxWorkers: 8,
    fileParallelism: true,
  },
});
```

### Mock Not Working

**Issue**: vi.mock() doesn't work

**Solution**: Ensure module is mocked before import:
```typescript
// Mock must come before imports
vi.mock('./module');

import { someFunction } from './module';
```

## VS Code Integration

A VS Code extension is available on the Marketplace to enhance the testing experience. ([Vitest Guide][2])

Features include:
- Run tests from editor
- View results inline
- Debug tests
- Coverage visualization

## Migration from Jest

Vitest's Jest compatibility makes migration "straightforward." ([Vitest Documentation][1])

### Key Differences

1. **Configuration**: Move Jest config to Vitest config
2. **Imports**: Change from `@jest/globals` to `vitest`
3. **Globals**: Disable if using explicit imports
4. **Module mocking**: Similar API, minor syntax differences

### Migration Steps

1. **Install Vitest**:
```bash
npm install -D vitest
npm uninstall jest
```

2. **Update test scripts**:
```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

3. **Update imports**:
```typescript
// Before (Jest)
import { test, expect } from '@jest/globals';

// After (Vitest)
import { test, expect } from 'vitest';
```

4. **Migrate configuration**:
```typescript
// jest.config.js → vitest.config.ts
export default defineConfig({
  test: {
    globals: true, // if you want Jest-like globals
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
  },
});
```

5. **Update mocks**:
```typescript
// Before (Jest)
jest.mock('./module');
jest.fn();

// After (Vitest)
vi.mock('./module');
vi.fn();
```

## Community & Support

**Documentation**: Comprehensive documentation at [vitest.dev](https://vitest.dev)

**GitHub**: [github.com/vitest-dev/vitest](https://github.com/vitest-dev/vitest)

**Community**: Active Discord and GitHub Discussions

## References

[1]: https://vitest.dev/ "Vitest Documentation"
[2]: https://vitest.dev/guide/ "Vitest Guide"
[3]: https://vitest.dev/guide/features "Vitest Features"
[4]: https://vitest.dev/config/ "Vitest Configuration"
