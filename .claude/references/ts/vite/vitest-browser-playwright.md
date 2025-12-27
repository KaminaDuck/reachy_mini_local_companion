---
title: "Vitest Browser Mode with Playwright"
description: "Vitest 4 browser mode integration with Playwright for cross-browser component testing"
type: "integration-guide"
tags: ["vitest", "playwright", "browser-testing", "testing", "vite", "e2e", "typescript", "ci-cd", "cross-browser", "troubleshooting", "configuration"]
category: "frontend"
subcategory: "testing"
version: "4.0.6"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "Vitest Browser Mode Guide"
    url: "https://vitest.dev/guide/browser/"
  - name: "Vitest Browser Configuration"
    url: "https://vitest.dev/guide/browser/config"
  - name: "Vitest Playwright Integration"
    url: "https://vitest.dev/guide/browser/playwright"
  - name: "Vitest Configuration"
    url: "https://vitest.dev/config/"
  - name: "Playwright Documentation"
    url: "https://playwright.dev/"
  - name: "Production Troubleshooting Experience"
    url: "internal://ai-eng-sandbox/vitest-browser-mode-fix"
related: ["vitest.md", "../playwright/playwright-framework-guide.md", "../playwright/playwright-mcp-integration.md"]
author: "unknown"
contributors: []
---

# Vitest Browser Mode with Playwright

Vitest Browser Mode enables running tests directly in actual browsers rather than Node.js environments, providing access to native browser APIs without simulation or mocking. ([Vitest Browser Mode Guide][1])

## Overview

### What is Browser Mode?

Browser Mode runs Vitest tests in actual browsers, providing access to native browser globals and APIs like `window`, `document`, and the DOM. ([Vitest Browser Mode Guide][1]) Tests execute within iframes in a browser UI, with communication handled through Chrome DevTools Protocol (Playwright) or WebDriver protocols (WebdriverIO). ([Vitest Browser Mode Guide][1])

### Key Capabilities

Browser Mode provides the following capabilities: ([Vitest Browser Mode Guide][1])

- **Native browser testing** without simulation or mocking
- **Access to genuine browser APIs** (window, document, DOM)
- **Multiple framework support** (Vue, React, Svelte, Solid)
- **Built-in Locators API** for element querying
- **Interactivity API** for user interactions
- **Assertion API** forked from @testing-library/jest-dom
- **Headless mode** for CI environments
- **Screenshot and trace capture** capabilities
- **Cross-browser testing** (Chromium, Firefox, WebKit, Edge)

### Browser Compatibility

Minimum browser requirements are based on native ESM, dynamic import, and BroadcastChannel support: ([Vitest Browser Mode Guide][1])

- Chrome ≥87
- Firefox ≥78
- Safari ≥15.4
- Edge ≥88

### Provider Options

Vitest supports three browser providers: ([Vitest Browser Mode Guide][1])

1. **@vitest/browser-preview** - Development/visualization only, simulates events
2. **@vitest/browser-playwright** - Recommended for CI, supports parallel execution, uses Chrome DevTools Protocol
3. **@vitest/browser-webdriverio** - Alternative automation framework using WebDriver protocol

The Playwright provider is recommended for production use due to its performance and parallel execution support. ([Vitest Browser Mode Guide][1])

## Installation and Setup

### Installing Playwright Provider

Install Vitest and the Playwright browser provider: ([Vitest Playwright Integration][3])

```bash
npm install -D vitest @vitest/browser-playwright
```

The Playwright provider will automatically install browser binaries on first use. ([Vitest Playwright Integration][3]) To manually install browsers:

```bash
npx playwright install
```

### Basic Configuration

Configure Vitest to use browser mode with the Playwright provider: ([Vitest Browser Configuration][2])

```typescript
import { playwright } from '@vitest/browser-playwright'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      instances: [
        { browser: 'chromium' }
      ]
    }
  }
})
```

### Configuration File Formats

Vitest reads your `vite.config.ts` automatically, or you can create a dedicated `vitest.config.ts` file. ([Vitest Configuration][4]) Supported formats include `.js`, `.mjs`, `.cjs`, `.ts`, `.cts`, `.mts`. ([Vitest Configuration][4])

## Configuration Reference

### Core Browser Settings

**browser.enabled** (boolean, default: false)

Run all tests inside a browser environment. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: { enabled: true }
  }
})
```

**browser.instances** (BrowserConfig[], default: [])

Define multiple browser configurations for cross-browser testing. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      instances: [
        { browser: 'chromium' },
        { browser: 'firefox' },
        { browser: 'webkit' }
      ]
    }
  }
})
```

**browser.provider** (BrowserProviderOption, default: 'preview')

Choose the browser automation provider: `'preview'`, `'playwright'`, or `'webdriverio'`. ([Vitest Browser Configuration][2])

```typescript
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      provider: playwright()
    }
  }
})
```

**browser.headless** (boolean, default: process.env.CI)

Run browser in headless mode without visible UI. ([Vitest Browser Configuration][2]) Automatically enabled when `process.env.CI` is detected. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      headless: true // Force headless mode
    }
  }
})
```

**browser.isolate** (boolean, default: true)

Run every test in a separate iframe for better isolation. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      isolate: true // Each test gets fresh iframe
    }
  }
})
```

### Viewport and Display Settings

**browser.viewport** (object, default: { width: 414, height: 896 })

Configure the default iframe viewport dimensions. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      viewport: {
        width: 1280,
        height: 720
      }
    }
  }
})
```

**browser.ui** (boolean, default: !isCI)

Controls whether Vitest UI should be injected into the page. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      ui: false // Disable UI overlay
    }
  }
})
```

### Screenshots and Tracing

**browser.screenshotDirectory** (string, default: '__screenshots__')

Directory path for storing test failure screenshots. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      screenshotDirectory: './test-screenshots'
    }
  }
})
```

**browser.screenshotFailures** (boolean, default: !browser.ui)

Automatically capture screenshots when tests fail. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      screenshotFailures: true
    }
  }
})
```

**browser.trace** (string | object, default: 'off')

Configure browser test trace capture for debugging. ([Vitest Browser Configuration][2]) Options:

- `'on'` - Capture traces for all tests
- `'off'` - Disable trace capture
- `'on-first-retry'` - Capture only on first retry
- `'on-all-retries'` - Capture on every retry
- `'retain-on-failure'` - Keep traces only for failed tests

```typescript
export default defineConfig({
  test: {
    browser: {
      trace: 'on-first-retry'
    }
  }
})
```

### Advanced Settings

**browser.api** (number | object, default: 63315)

Configure the Vite server options for browser communication. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      api: {
        port: 8080,
        host: '0.0.0.0'
      }
    }
  }
})
```

**browser.connectTimeout** (number, default: 60000)

Browser connection timeout in milliseconds. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      connectTimeout: 120000 // 2 minutes
    }
  }
})
```

**browser.trackUnhandledErrors** (boolean, default: true)

Track uncaught errors and unhandled promise rejections. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      trackUnhandledErrors: true
    }
  }
})
```

**browser.locators.testIdAttribute** (string, default: 'data-testid')

Configure the attribute used by `getByTestId` locator. ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      locators: {
        testIdAttribute: 'data-test-id'
      }
    }
  }
})
```

## Playwright Provider Integration

### Provider Configuration

The Playwright provider accepts options that are passed to Playwright's launch and context methods: ([Vitest Playwright Integration][3])

```typescript
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      provider: playwright({
        launch: {
          // Playwright launch options
          args: ['--disable-gpu'],
          timeout: 60000
        },
        context: {
          // Browser context options
          locale: 'en-US',
          timezoneId: 'America/New_York'
        }
      })
    }
  }
})
```

### Launch Options

Launch options are passed to `playwright[browser].launch()`. ([Vitest Playwright Integration][3]) Common options:

- **args** (string[]) - Additional browser launch arguments
- **timeout** (number) - Maximum launch time in milliseconds
- **devtools** (boolean) - Open browser DevTools
- **slowMo** (number) - Slow down operations by specified milliseconds

```typescript
provider: playwright({
  launch: {
    args: ['--disable-web-security', '--disable-features=IsolateOrigins'],
    timeout: 30000,
    slowMo: 100
  }
})
```

### Context Options

Context options customize the browser context via `browser.newContext()`. ([Vitest Playwright Integration][3]) Vitest automatically enables:

- `ignoreHTTPSErrors: true` - Accept self-signed certificates
- `serviceWorkers: 'allow'` - Enable service workers

Common context options:

```typescript
provider: playwright({
  context: {
    locale: 'en-US',
    timezoneId: 'America/New_York',
    geolocation: { longitude: 12.4924, latitude: 41.8902 },
    permissions: ['geolocation'],
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Custom User Agent'
  }
})
```

**Important:** Prefer `test.browser.viewport` over context viewport to avoid headless mode issues. ([Vitest Playwright Integration][3])

### Connect Options

Connect to an existing Playwright server instead of launching a new browser: ([Vitest Playwright Integration][3])

```typescript
provider: playwright({
  connect: {
    wsEndpoint: 'ws://localhost:3000'
  }
})
```

### Action Timeout

Configure the default timeout for Playwright actions: ([Vitest Playwright Integration][3])

```typescript
provider: playwright({
  context: {
    actionTimeout: 10000 // 10 seconds
  }
})
```

## Writing Browser Tests

### Basic Test Structure

Tests run in actual browsers with access to native APIs: ([Vitest Browser Mode Guide][1])

```typescript
import { test, expect } from 'vitest'

test('basic browser test', async () => {
  // Test runs in actual browser
  expect(window).toBeDefined()
  expect(document.body).toBeInTheDocument()
})
```

### File Naming Conventions

By default, tests must contain `.test.` or `.spec.` in their file name. ([Vitest Configuration][4])

```
components/Button.test.ts
components/Button.spec.tsx
utils/helpers.test.js
```

### Accessing Page Context

Import the page context to access Playwright APIs: ([Vitest Browser Mode Guide][1])

```typescript
import { page } from '@vitest/browser/context'

test('interact with elements', async () => {
  const button = page.getByRole('button', { name: 'Submit' })
  await button.click()
})
```

### Using Locators API

Vitest provides a built-in Locators API for element querying: ([Vitest Browser Mode Guide][1])

```typescript
import { page } from '@vitest/browser/context'

test('locators', async () => {
  // By role
  const button = page.getByRole('button', { name: 'Submit' })

  // By text
  const heading = page.getByText('Welcome')

  // By label
  const input = page.getByLabel('Email')

  // By placeholder
  const search = page.getByPlaceholder('Search...')

  // By test ID
  const element = page.getByTestId('custom-element')

  // By CSS selector
  const div = page.locator('.container')
})
```

### Interactivity API

Perform user interactions using the Interactivity API: ([Vitest Browser Mode Guide][1])

```typescript
import { page } from '@vitest/browser/context'

test('user interactions', async () => {
  const button = page.getByRole('button')

  // Click
  await button.click()

  // Double click
  await button.dblclick()

  // Fill input
  const input = page.getByRole('textbox')
  await input.fill('Hello World')

  // Hover
  await button.hover()

  // Focus
  await input.focus()

  // Select option
  const select = page.getByRole('combobox')
  await select.selectOption('value')
})
```

### Assertions API

Vitest provides browser-specific assertions forked from @testing-library/jest-dom: ([Vitest Browser Mode Guide][1])

```typescript
import { expect } from 'vitest'
import { page } from '@vitest/browser/context'

test('browser assertions', async () => {
  const element = page.getByRole('button')

  // Visibility
  await expect(element).toBeVisible()
  await expect(element).toBeHidden()

  // Text content
  await expect(element).toHaveText('Submit')
  await expect(element).toContainText('Sub')

  // Attributes
  await expect(element).toHaveAttribute('disabled')
  await expect(element).toHaveAttribute('type', 'submit')

  // Classes
  await expect(element).toHaveClass('btn-primary')

  // Value
  const input = page.getByRole('textbox')
  await expect(input).toHaveValue('test')
})
```

### Test Isolation

Vitest opens a single page to run all tests defined in the same file. ([Vitest Browser Mode Guide][1]) Test isolation applies at the file level, not individual tests, unless `browser.isolate: true` is enabled. ([Vitest Browser Configuration][2])

```typescript
// All tests in this file share the same page context
test('test 1', async () => {
  // Runs in shared page
})

test('test 2', async () => {
  // Runs in same page as test 1
})
```

With `browser.isolate: true`, each test gets its own iframe:

```typescript
export default defineConfig({
  test: {
    browser: {
      isolate: true // Each test gets fresh iframe
    }
  }
})
```

## Debugging and Tooling

### Trace Viewer

Enable trace capture for detailed debugging information: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      trace: 'on-first-retry'
    }
  }
})
```

Trace options:
- `'on'` - Always capture traces
- `'on-first-retry'` - Capture on first retry only
- `'on-all-retries'` - Capture on every retry
- `'retain-on-failure'` - Keep traces only for failed tests

### Headed Browser Mode

Disable headless mode to see the browser UI while tests run: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      headless: false
    }
  }
})
```

Or use CLI flag:

```bash
vitest --browser.headless=false
```

### Vitest UI Mode

Vitest UI is automatically injected unless disabled: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      ui: true // Enable UI overlay
    }
  }
})
```

### Screenshot Capture

Automatically capture screenshots on test failures: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      screenshotFailures: true,
      screenshotDirectory: './screenshots'
    }
  }
})
```

### Slow Motion

Slow down Playwright operations for visual debugging: ([Vitest Playwright Integration][3])

```typescript
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      provider: playwright({
        launch: {
          slowMo: 500 // 500ms delay between operations
        }
      })
    }
  }
})
```

### DevTools Integration

Open browser DevTools automatically: ([Vitest Playwright Integration][3])

```typescript
provider: playwright({
  launch: {
    devtools: true
  }
})
```

## Cross-Browser Testing

### Supported Browsers

Playwright supports four browser engines: ([Vitest Browser Mode Guide][1])

- **chromium** - Chrome, Edge, and other Chromium-based browsers
- **firefox** - Mozilla Firefox
- **webkit** - Safari
- **edge** - Microsoft Edge (uses Chromium)

### Multi-Browser Configuration

Configure multiple browser instances for cross-browser testing: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      instances: [
        { browser: 'chromium' },
        { browser: 'firefox' },
        { browser: 'webkit' }
      ]
    }
  }
})
```

### Per-Instance Configuration

Override provider options for specific browser instances: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      provider: playwright(),
      instances: [
        {
          browser: 'chromium',
          launch: {
            args: ['--disable-gpu', '--no-sandbox']
          }
        },
        {
          browser: 'firefox',
          launch: {
            firefoxUserPrefs: {
              'network.proxy.type': 1
            }
          }
        },
        {
          browser: 'webkit',
          context: {
            locale: 'en-GB'
          }
        }
      ]
    }
  }
})
```

**Important:** Per-instance configurations do not merge with parent settings—they completely override them. ([Vitest Browser Configuration][2])

### Running Specific Browsers

Use CLI flags to run tests in specific browsers:

```bash
# Run in single browser
vitest --browser.name=chromium

# Run in multiple browsers
vitest --browser.name=chromium,firefox
```

## CI/CD Integration

### Automatic Headless Mode

Headless mode is automatically enabled when `process.env.CI` is detected: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      headless: !!process.env.CI // Auto-detect CI environment
    }
  }
})
```

### CLI Usage in CI

```bash
# Run browser tests in CI
vitest run --browser

# Force headless mode
vitest run --browser.headless

# Disable browser UI in CI
vitest run --browser.ui=false

# Enable trace capture
vitest run --browser.trace=on-first-retry

# Capture screenshots on failure
vitest run --browser.screenshotFailures
```

### Recommended CI Configuration

```typescript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      headless: !!process.env.CI,
      screenshotFailures: true,
      trace: 'on-first-retry',
      instances: [
        { browser: 'chromium' }
      ]
    }
  }
})
```

### GitHub Actions Example

```yaml
name: Browser Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run browser tests
        run: npm run test:browser

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: __screenshots__/
```

### Docker Integration

When using Docker, ensure browser binaries are installed: ([Vitest Playwright Integration][3])

```dockerfile
FROM node:20

# Install Playwright dependencies
RUN npx playwright install-deps

# Install project dependencies
COPY package*.json ./
RUN npm ci

# Install Playwright browsers
RUN npx playwright install chromium

COPY . .

CMD ["npm", "run", "test:browser"]
```

## Performance Optimization

### Parallelization

The Playwright provider supports parallel test execution: ([Vitest Browser Mode Guide][1])

```typescript
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright()
    },
    pool: 'threads',
    maxWorkers: 4,
    fileParallelism: true
  }
})
```

### Resource Management

Each browser instance consumes memory and CPU. ([Vitest Browser Mode Guide][1]) Optimize resource usage:

```typescript
export default defineConfig({
  test: {
    browser: {
      headless: true, // Reduces resource usage
      isolate: false // Share page context when safe
    },
    maxWorkers: 2, // Limit concurrent browsers
    testTimeout: 30000 // Prevent hanging tests
  }
})
```

### Speed Considerations

Browser tests are slower than Node tests due to browser startup overhead. ([Vitest Browser Mode Guide][1]) Optimization strategies:

1. **Use headless mode** - Faster than headed browsers
2. **Minimize browser launches** - Reuse contexts when possible
3. **Reduce test isolation** - Set `browser.isolate: false` if safe
4. **Optimize selectors** - Use efficient locator strategies
5. **Limit concurrent instances** - Balance speed vs. resources

### Connection Timeout

Increase timeout for slow environments: ([Vitest Browser Configuration][2])

```typescript
export default defineConfig({
  test: {
    browser: {
      connectTimeout: 120000 // 2 minutes for slow CI
    }
  }
})
```

## Migration Guide

### From Node Tests to Browser Tests

**Before (Node with jsdom):**

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'jsdom'
  }
})

// test file
import { test, expect } from 'vitest'

test('DOM test', () => {
  document.body.innerHTML = '<button>Click</button>'
  const button = document.querySelector('button')
  expect(button).toBeTruthy()
})
```

**After (Browser with Playwright):**

```typescript
// vitest.config.ts
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      instances: [{ browser: 'chromium' }]
    }
  }
})

// test file
import { test, expect } from 'vitest'
import { page } from '@vitest/browser/context'

test('DOM test', async () => {
  // Render actual component
  const button = page.getByRole('button', { name: 'Click' })
  await expect(button).toBeVisible()
})
```

### Configuration Migration Steps

1. **Install browser provider:**

```bash
npm install -D @vitest/browser-playwright
npm uninstall jsdom happy-dom
```

2. **Update configuration:**

```typescript
// Remove environment setting
- environment: 'jsdom'

// Add browser mode
+ browser: {
+   enabled: true,
+   provider: playwright(),
+   instances: [{ browser: 'chromium' }]
+ }
```

3. **Update imports:**

```typescript
// Add browser imports
import { page } from '@vitest/browser/context'
```

4. **Update assertions:**

```typescript
// Before
expect(element.textContent).toBe('Hello')

// After
await expect(element).toHaveText('Hello')
```

### Module Mocking Migration

Module mocking works differently in browser mode due to sealed namespace objects. ([Vitest Browser Mode Guide][1])

**Before (Node):**

```typescript
import { vi } from 'vitest'
import * as module from './module'

vi.spyOn(module, 'exportedFunction')
```

**After (Browser):**

```typescript
import { vi } from 'vitest'

vi.mock('./module', { spy: true })
import { exportedFunction } from './module'

// exportedFunction is now automatically spied on
```

## Best Practices

### Recommended Patterns

1. **Use Playwright provider for production** - Better performance and parallel execution support
2. **Enable headless in CI** - Automatically enabled via `process.env.CI` detection
3. **Use isolated mode** - Set `browser.isolate: true` for test independence
4. **Configure appropriate timeouts** - Increase `connectTimeout` for slow environments
5. **Capture screenshots on failures** - Enable `screenshotFailures` for debugging
6. **Use selective trace capture** - Set `trace: 'on-first-retry'` or `'retain-on-failure'`
7. **Prefer browser viewport config** - Use `test.browser.viewport` over context options
8. **Use semantic locators** - Prefer `getByRole` over CSS selectors
9. **Test in multiple browsers** - Validate cross-browser compatibility
10. **Optimize resource usage** - Limit `maxWorkers` based on available resources

### Anti-Patterns

1. **Don't rely on thread-blocking dialogs** - `alert`, `confirm`, `prompt` hang execution (Vitest provides default mocks)
2. **Avoid direct object spying** - Module namespace is sealed, use `vi.mock` with `spy: true`
3. **Don't specify viewport in context options** - Can cause headless mode issues, use `test.browser.viewport` instead
4. **Don't over-isolate tests** - Balance isolation with performance based on test independence
5. **Avoid excessive parallel execution** - Too many concurrent browsers can overwhelm system resources
6. **Don't skip error tracking** - Keep `trackUnhandledErrors: true` to catch issues
7. **Avoid synchronous DOM manipulation** - Use async Playwright APIs for reliability

### Test Organization Strategy

```typescript
// Good: Organize by component or feature
describe('LoginForm', () => {
  test('renders login fields', async () => {
    // Test implementation
  })

  test('validates email format', async () => {
    // Test implementation
  })

  test('submits form data', async () => {
    // Test implementation
  })
})

// Good: Use descriptive test names
test('displays error message when email is invalid', async () => {
  // Test implementation
})

// Bad: Vague test names
test('it works', async () => {
  // Test implementation
})
```

## Troubleshooting

### Browser Not Launching

**Symptoms:** Tests hang or fail with connection timeout

**Solutions:**

1. Verify Playwright provider is installed:

```bash
npm install -D @vitest/browser-playwright
```

2. Install browser binaries:

```bash
npx playwright install
```

3. Check Node.js version compatibility (requires Node ≥20.0.0)

4. Increase connection timeout:

```typescript
export default defineConfig({
  test: {
    browser: {
      connectTimeout: 120000
    }
  }
})
```

### Connection Timeout

**Symptoms:** Error: "Failed to connect to browser"

**Solutions:**

1. Check for port conflicts (default: 63315):

```typescript
export default defineConfig({
  test: {
    browser: {
      api: { port: 8080 }
    }
  }
})
```

2. Verify network connectivity and firewall rules

3. Ensure browser binaries are properly installed

### Module Mocking Not Working

**Symptoms:** `vi.spyOn` throws error about sealed namespace

**Solution:** Use `vi.mock` with `spy: true` option: ([Vitest Browser Mode Guide][1])

```typescript
// Correct approach for browser mode
vi.mock('./module.js', { spy: true })
import { exportedFunction } from './module.js'

// exportedFunction is automatically spied on
expect(exportedFunction).toHaveBeenCalled()
```

Alternative: Export helper functions instead of variables

```typescript
// Instead of exporting variable
export const value = 42

// Export getter function
export const getValue = () => 42
```

### Tests Hanging

**Symptoms:** Tests never complete or timeout

**Causes and solutions:**

1. **Thread-blocking dialogs** - Vitest provides default mocks for `alert`, `confirm`, `prompt` ([Vitest Browser Mode Guide][1])

2. **Missing await statements:**

```typescript
// Wrong
test('test', () => {
  page.getByRole('button').click() // Missing await
})

// Correct
test('test', async () => {
  await page.getByRole('button').click()
})
```

3. **Infinite loops or unresolved promises:**

```typescript
// Set appropriate timeout
test('test', async () => {
  // Test implementation
}, { timeout: 10000 })
```

### Screenshot Not Saved

**Symptoms:** Screenshots not appearing in configured directory

**Solutions:**

1. Verify directory path and permissions:

```typescript
export default defineConfig({
  test: {
    browser: {
      screenshotDirectory: './test-screenshots'
    }
  }
})
```

2. Ensure `screenshotFailures` is enabled:

```typescript
export default defineConfig({
  test: {
    browser: {
      screenshotFailures: true
    }
  }
})
```

3. Check that test actually failed (screenshots only captured on failure by default)

### Trace Not Working

**Symptoms:** Trace files not generated

**Solutions:**

1. Verify trace option is configured:

```typescript
export default defineConfig({
  test: {
    browser: {
      trace: 'on-first-retry'
    }
  }
})
```

2. Ensure test failed or retried (depending on trace setting)

3. Check file system permissions in trace directory

### Import Errors

**Symptoms:** Cannot find module or import errors

**Solution:** Ensure Vite config includes proper aliases and resolvers: ([Vitest Configuration][4])

```typescript
import path from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  test: {
    browser: {
      enabled: true,
      provider: playwright()
    }
  }
})
```

## Common Configuration Pitfalls

### Incorrect mergeConfig Usage in Inline Projects

**Problem:** Using `mergeConfig()` to wrap inline project definitions in the `projects` array prevents proper Vite plugin inheritance and causes browser startup failures.

**Symptoms:**
- Browser connection timeout (90+ seconds)
- "Failed to connect to the browser session" errors
- Path alias resolution failures (`@/` imports not working)
- Module import errors in browser context

**Incorrect Pattern:**

```typescript
import { defineConfig, mergeConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'
import viteConfig from './vite.config'

export default defineConfig({
  test: {
    projects: [
      // ❌ WRONG: mergeConfig in inline project
      mergeConfig(viteConfig, {
        test: {
          name: 'browser',
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [{ browser: 'chromium' }]
          }
        }
      })
    ]
  }
})
```

**Why This Fails:**
1. `mergeConfig` is designed for **separate config files**, not inline project objects
2. Vite plugins (e.g., React plugin) don't properly inherit in merged inline projects
3. Path resolution configuration (`resolve.alias`) gets lost
4. Browser context initialization silently fails due to missing build configuration

**Correct Pattern - Inline Projects:**

```typescript
import { defineConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'
import react from '@vitejs/plugin-react'
import path from 'node:path'

export default defineConfig({
  test: {
    projects: [
      // ✅ CORRECT: Plain object with explicit plugins and resolve
      {
        plugins: [react()],
        resolve: {
          alias: {
            '@': path.resolve(__dirname, './src')
          }
        },
        test: {
          name: 'browser',
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [{ browser: 'chromium' }]
          }
        }
      }
    ]
  }
})
```

**Alternative Pattern - Separate Config Files:**

```typescript
// vitest.workspace.ts
export default defineConfig({
  test: {
    projects: [
      './vitest.browser.config.ts',
      './vitest.node.config.ts'
    ]
  }
})

// vitest.browser.config.ts
import { defineProject, mergeConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineProject({
    test: {
      name: 'browser',
      browser: { /* config */ }
    }
  })
)
```

### Missing Environment Variables

**Problem:** Browser tests fail with validation errors when environment variables are undefined.

**Symptoms:**
- `ZodError` or validation failures on import
- "expected string, received undefined" errors
- Tests fail before reaching test code

**Solution:** Define environment variables in root config:

```typescript
export default defineConfig({
  // Environment variables for tests
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify('http://localhost:8000'),
    'import.meta.env.VITE_APP_NAME': JSON.stringify('Test App'),
  },
  test: {
    browser: { /* config */ }
  }
})
```

### MSW Browser Worker Not Enabled

**Problem:** API mocking fails in browser mode, causing tests to make real network requests or fail.

**Symptoms:**
- Form submission tests fail
- API integration tests hang or fail
- "Mock not found" or network errors
- Tests work in jsdom but fail in browser

**Solution:** Enable MSW browser worker in setup file:

```typescript
// tests/setup-browser.ts
import { beforeAll, afterEach, afterAll } from 'vitest'
import { worker } from './mocks/server-browser'

beforeAll(async () => {
  await worker.start({
    onUnhandledRequest: 'warn',
    quiet: false
  })
})

afterEach(() => {
  worker.resetHandlers()
})

afterAll(() => {
  worker.stop()
})
```

**Important:** Don't forget to generate the service worker file:

```bash
npx msw init public/ --save
```

### Using Node MSW Server in Browser Tests

**Problem:** Importing `server` from Node MSW setup instead of `worker` from browser setup causes import failures.

**Symptoms:**
- "Failed to fetch dynamically imported module" errors
- Integration tests fail to load
- MSW handlers don't intercept requests

**Solution:** Use browser worker in integration tests:

```typescript
// ❌ WRONG: Node server in browser test
import { server } from '../mocks/server'
server.use(/* override handler */)

// ✅ CORRECT: Browser worker in browser test
import { worker } from '../mocks/server-browser'
worker.use(/* override handler */)
```

### Path Alias Not Working

**Problem:** Path aliases like `@/` fail to resolve in browser tests.

**Symptoms:**
- "Failed to resolve import @/..." errors
- Module not found errors
- Tests fail during import phase

**Solution:** Explicitly add `resolve.alias` to each project:

```typescript
export default defineConfig({
  test: {
    projects: [
      {
        plugins: [react()],
        resolve: {
          alias: {
            '@': path.resolve(__dirname, './src')
          }
        },
        test: { /* config */ }
      }
    ]
  }
})
```

Note: For ES modules, you need to define `__dirname`:

```typescript
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
```

### Excessive Connection Timeout

**Problem:** Setting very high `connectTimeout` values (90+ seconds) masks configuration issues.

**Correct Approach:**
- Browser should start in < 5 seconds with proper configuration
- Use 30-60 second timeout as a reasonable maximum
- If timeout is reached, investigate configuration issues rather than increasing timeout

```typescript
export default defineConfig({
  test: {
    browser: {
      connectTimeout: 30000, // 30 seconds is reasonable
      // If this timeout is reached, fix the config instead of increasing
    }
  }
})
```

## Limitations and Tradeoffs

### Module Mocking Constraints

The module namespace object is sealed and cannot be reconfigured in browser mode, unlike Node.js tests. ([Vitest Browser Mode Guide][1]) This means direct spying on imported objects is not possible:

```typescript
// Does not work in browser mode
import * as module from './module'
vi.spyOn(module, 'exportedFunction') // Error: namespace is sealed
```

**Workaround:** Use `vi.mock` with `spy: true` option:

```typescript
vi.mock('./module.js', { spy: true })
import { exportedFunction } from './module.js'
```

### Thread-Blocking Dialogs

`alert`, `confirm`, and `prompt` dialogs hang test execution. ([Vitest Browser Mode Guide][1]) Vitest provides default mocks to prevent this, but the behavior differs from real user interaction.

### Test Isolation Level

Vitest opens a single page per test file, not per test. ([Vitest Browser Mode Guide][1]) Test isolation is at the file level unless `browser.isolate: true` is enabled. ([Vitest Browser Configuration][2])

```typescript
// Without isolate: true, all tests share page context
test('test 1', async () => { /* uses shared page */ })
test('test 2', async () => { /* uses same page */ })
```

Enable `browser.isolate: true` for per-test isolation at the cost of performance:

```typescript
export default defineConfig({
  test: {
    browser: {
      isolate: true // Each test gets fresh iframe
    }
  }
})
```

### ESM Feature Support

Tests only support features specified in the `esbuild.target` option, as Vitest uses Vite dev server. ([Vitest Browser Mode Guide][1]) Modern JavaScript features may not work in older browser targets.

### Performance Overhead

Browser tests are significantly slower than Node tests due to: ([Vitest Browser Mode Guide][1])

- Browser startup and initialization time
- Real DOM rendering and layout calculations
- Network request simulation
- Screenshot and trace capture overhead

### Provider Limitations

**Preview Provider:**
- Development/visualization only
- Simulates events rather than actual browser interactions
- Not suitable for production testing

**Playwright Provider:**
- Requires browser binary installation (~200-300MB per browser)
- Resource-intensive for parallel execution
- Platform-specific binaries

**Docker Playwright MCP:**
- Only supports headless Chromium
- Limited browser selection

### Browser Compatibility

Tests require modern browser features (ESM, dynamic import, BroadcastChannel): ([Vitest Browser Mode Guide][1])

- Chrome ≥87
- Firefox ≥78
- Safari ≥15.4
- Edge ≥88

Older browsers are not supported.

## References

[1]: https://vitest.dev/guide/browser/ "Vitest Browser Mode Guide"
[2]: https://vitest.dev/guide/browser/config "Vitest Browser Configuration"
[3]: https://vitest.dev/guide/browser/playwright "Vitest Playwright Integration"
[4]: https://vitest.dev/config/ "Vitest Configuration"
[5]: https://playwright.dev/ "Playwright Documentation"
