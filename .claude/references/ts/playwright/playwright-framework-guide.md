---
title: "Playwright Testing Framework"
description: "Comprehensive guide to Playwright end-to-end testing framework"
type: "framework-guide"
tags: ["playwright", "testing", "e2e", "typescript", "automation", "browsers", "chromium", "webkit", "firefox"]
category: "ts"
subcategory: "testing"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Playwright Documentation"
    url: "https://playwright.dev/docs/intro"
  - name: "Playwright API Reference"
    url: "https://playwright.dev/docs/api/class-playwright"
  - name: "Playwright Test Configuration"
    url: "https://playwright.dev/docs/test-configuration"
  - name: "Playwright Locators"
    url: "https://playwright.dev/docs/locators"
  - name: "Playwright Assertions"
    url: "https://playwright.dev/docs/test-assertions"
  - name: "Playwright Trace Viewer"
    url: "https://playwright.dev/docs/trace-viewer"
related: ["../vite/vitest-browser-playwright.md"]
author: "unknown"
contributors: []
---

# Playwright Testing Framework

Playwright Test is an end-to-end testing framework for modern web applications, integrating a test runner, assertions, isolation capabilities, and parallelization features with comprehensive tooling support. ([Playwright Docs][1])

## Overview

### Key Features

Playwright supports Chromium, WebKit, and Firefox on Windows, Linux, and macOS, locally or in CI, headless or headed, with native mobile emulation for Chrome (Android) and Mobile Safari. ([Playwright Docs][1])

The framework includes:
- Multiple browser engine support (Chromium, WebKit, Firefox)
- Cross-platform compatibility (Windows, Linux, macOS)
- Native mobile emulation capabilities
- Headless and headed execution modes
- CI/CD integration support
- Auto-waiting and retry capabilities
- Parallelization and test isolation

### System Requirements

- **Node.js:** Latest versions 20.x, 22.x, or 24.x
- **Windows:** Version 11+ or Server 2019+
- **macOS:** Version 14 (Ventura) or later
- **Linux:** Debian 12/13 or Ubuntu 22.04/24.04 (both x86-64 and arm64)

([Playwright Docs][1])

## Installation

### Package Manager Approach

The quickest setup uses npm, yarn, or pnpm with initialization commands:

```bash
npm init playwright@latest
```

This scaffolds a new project or integrates into existing ones, creating:
- Configuration file (`playwright.config.ts`)
- Package dependencies
- Example tests
- Sample test directory for pattern exploration

([Playwright Docs][1])

### VS Code Extension

Alternative setup through the integrated VS Code extension for test creation and execution.

## Core Concepts

### Playwright Module

Playwright is a module that enables browser automation. The Playwright module provides a method to launch a browser instance, allowing developers to control Chromium, Firefox, and WebKit browsers programmatically. ([Playwright API][2])

#### Main Properties

The Playwright object exposes several key properties:

- **Browser Engines**: `chromium`, `firefox`, and `webkit` are BrowserType objects used to launch or connect to respective browsers
- **devices**: Dictionary of pre-configured device profiles for mobile testing scenarios
- **errors**: Specialized error classes like TimeoutError for exception handling
- **request**: APIRequest interface for Web API testing
- **selectors**: Tools for installing custom selector engines

([Playwright API][2])

### Test Structure

Playwright tests follow a simple pattern: they **perform actions** and **assert the state** against expectations. ([Playwright Tests][5])

Tests use the `test` function with an async callback receiving fixtures like `page`:

```typescript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

### Test Isolation & Fixtures

Each test receives its own isolated `page` fixture within a separate Browser Context. This ensures every test gets a fresh environment, even when multiple tests run in a single browser. ([Playwright Tests][5])

## Locators

### What Are Locators?

Locators represent a way to find element(s) on the page at any moment, serving as the core of Playwright's auto-waiting and retry capabilities. Every time a locator is used, it retrieves the current DOM element, ensuring tests remain resilient to page changes. ([Playwright Locators][4])

### Recommended Locator Strategies

Playwright prioritizes user-facing locators in this order:

1. **Role-based**: `page.getByRole()` - reflects how users perceive elements
2. **Text content**: `page.getByText()` - matches visible text
3. **Labels**: `page.getByLabel()` - locates form controls
4. **Placeholders**: `page.getByPlaceholder()` - finds inputs by hint text
5. **Alt text**: `page.getByAltText()` - locates images
6. **Titles**: `page.getByTitle()` - uses title attributes
7. **Test IDs**: `page.getByTestId()` - relies on `data-testid` attributes

([Playwright Locators][4])

#### Best Practices

Role locators should be prioritized because they align most closely with how assistive technology interprets pages. For interactive elements, use role locators; for non-interactive ones like divs and spans, text locators work better. ([Playwright Locators][4])

CSS and XPath selectors are discouraged—they break easily when DOM structure changes. Test IDs offer resilience but aren't user-facing, making them suitable as a secondary strategy.

### Advanced Locator Features

**Filtering**: Narrow results using `filter()` with text, child elements, or visibility criteria.

```typescript
await page
  .getByRole('listitem')
  .filter({ hasText: 'Product 2' })
  .click();
```

**Chaining**: Combine methods like `locator.and()` and `locator.or()` for complex selections.

**Strictness**: Locators throw errors when multiple elements match a single-element operation, forcing explicit disambiguation through `first()`, `last()`, or `nth()`. ([Playwright Locators][4])

## Actions

### Common Actions

Playwright provides a comprehensive set of actions for interacting with web elements:

**Navigation:**
- `page.goto()` - navigate to a URL (waits for page load state)

**Interactions:**
- `click()` - activate elements
- `fill()` - input text into forms
- `check()`/`uncheck()` - toggle checkboxes
- `selectOption()` - choose dropdown values
- `hover()` and `focus()` - element positioning

Playwright automatically waits for actionability, eliminating manual wait statements. ([Playwright Tests][5])

## Assertions

### Core Concept

Playwright provides the `expect()` function for test assertions. The framework distinguishes between two assertion types: auto-retrying assertions for web-specific conditions and non-retrying assertions for general value checks. ([Playwright Assertions][6])

### Auto-Retrying Assertions

These async matchers repeatedly check conditions until they pass or timeout. Playwright will be re-testing the element until the condition is met or until the timeout is reached. The default timeout is 5 seconds. ([Playwright Assertions][6])

Key examples include:

**Visibility checks:**
- `toBeVisible()`, `toBeHidden()`, `toBeInViewport()`

**State checks:**
- `toBeChecked()`, `toBeDisabled()`, `toBeEnabled()`, `toBeEditable()`

**Content checks:**
- `toHaveText()`, `toContainText()`, `toHaveValue()`

**Attribute checks:**
- `toHaveAttribute()`, `toHaveClass()`, `toHaveCSS()`

### Non-Retrying Assertions

These synchronous matchers don't auto-retry and include generic checks like `toEqual()`, `toBeTruthy()`, `toContain()`, and `toMatch()`. These are useful for testing synchronous values but can cause flaky tests with asynchronous content. ([Playwright Assertions][6])

### Advanced Assertion Features

**Soft Assertions**: Use `expect.soft()` to continue tests even when assertions fail, allowing multiple validation points.

**Custom Configuration**: `expect.configure()` creates pre-configured instances with custom timeouts or soft assertion defaults.

**Polling Logic**: `expect.poll()` and `expect.toPass()` enable retry logic for complex scenarios requiring repeated checks. ([Playwright Assertions][6])

## Configuration

### Configuration File Structure

Playwright uses a configuration file (typically `playwright.config.ts`) to define test behavior. The file exports a configuration object created with `defineConfig()`. Importantly, test runner options are **top-level**, do not put them into the `use` section. ([Playwright Config][3])

### Essential Configuration Options

**Test Discovery:**
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: /.*\.spec\.ts/,
  testIgnore: /.*\.skip\.ts/,
});
```

- `testDir`: Directory containing test files
- `testMatch`: Glob patterns matching test files (defaults to `.*(test|spec).(js|ts|mjs)`)
- `testIgnore`: Patterns to exclude from test discovery

([Playwright Config][3])

**Execution Control:**
```typescript
export default defineConfig({
  fullyParallel: true,
  workers: '50%',
  timeout: 30000,
  retries: 2,
});
```

- `fullyParallel`: Run all tests concurrently
- `workers`: Maximum concurrent worker processes (supports percentage notation)
- `timeout`: Per-test timeout (30 seconds default)
- `retries`: Retry attempts on failure

([Playwright Config][3])

**CI/CD Considerations:**
```typescript
export default defineConfig({
  forbidOnly: !!process.env.CI,
});
```

- `forbidOnly`: Fail build if `test.only` remains in code (defaults to checking environment variables for CI detection)

([Playwright Config][3])

**Output & Reporting:**
```typescript
export default defineConfig({
  outputDir: 'test-results',
  reporter: 'html',
});
```

- `outputDir`: Location for screenshots, videos, and traces
- `reporter`: Test reporting format

([Playwright Config][3])

### Project Configuration

The `projects` array enables testing across multiple browsers:

```typescript
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

([Playwright Config][3])

### Web Server Integration

Launch a development server automatically:

```typescript
export default defineConfig({
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

([Playwright Config][3])

## Test Organization

### Hooks

Hooks enable test organization:

- `test.describe()` - group related tests
- `test.beforeEach()`/`test.afterEach()` - run before/after each test
- `test.beforeAll()`/`test.afterAll()` - run once per worker

```typescript
test.describe('feature tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/feature');
  });

  test('test case 1', async ({ page }) => {
    // test code
  });

  test('test case 2', async ({ page }) => {
    // test code
  });
});
```

([Playwright Tests][5])

## Debugging & Tooling

### Trace Viewer

Playwright Trace Viewer is a graphical debugging tool that helps developers investigate test failures by examining recorded traces after script execution. The tool is particularly valuable for debugging CI failures. ([Playwright Trace][7])

#### Recording Traces

**Local Development:**
```bash
npx playwright test --trace on
```

**Continuous Integration:**
Configure traces for failed test retries in `playwright.config.ts`:

```typescript
export default defineConfig({
  retries: 1,
  use: {
    trace: 'on-first-retry',
  },
});
```

Available options include `'on-first-retry'`, `'on-all-retries'`, `'retain-on-failure'`, and `'off'`. ([Playwright Trace][7])

#### Opening Traces

Users can access recorded traces through:
- **CLI:** `npx playwright show-trace path/to/trace.zip`
- **Web:** [trace.playwright.dev](https://trace.playwright.dev) (supports drag-and-drop upload)
- **Remote traces:** `npx playwright show-trace https://example.com/trace.zip`

The browser-based viewer processes traces locally without transmitting data externally. ([Playwright Trace][7])

#### Trace Viewer Features

The trace viewer provides multiple debugging tabs:

- **Actions:** Displays locators and timing for each action with before/after DOM snapshots
- **Screenshots:** Film strip visualization showing state changes during test execution
- **Snapshots:** DOM captures at three points—before action, during input, and after action
- **Source:** Highlights the relevant code line for selected actions
- **Network & Console:** Filters request and log data by selected action timeframes
- **Errors:** Shows failure messages with timeline markers indicating error locations
- **Metadata & Attachments:** Test environment details and visual regression comparisons

([Playwright Trace][7])

### UI Mode

Interactive testing with watch functionality and time-travel debugging.

### HTML Test Reports

Dashboard interface with filtering and error inspection. HTML report is opened automatically if some of the tests failed unless configured otherwise. ([Playwright Reporters][8])

## Test Reporters

### Built-in Reporters

Playwright Test provides several pre-configured reporters accessible via the `--reporter` command line option or configuration file:

**List Reporter** (default locally)
List reporter is default (except on CI where the `dot` reporter is default). It displays one line per test with pass/fail status. ([Playwright Reporters][8])

**Line Reporter**
More condensed output than list mode, showing only the most recent completed test while maintaining progress visibility.

**Dot Reporter** (default on CI)
Dot reporter is very concise - it only produces a single character per successful test run. Uses symbols (·, F, ×, ±, T, °) to indicate test status. ([Playwright Reporters][8])

**HTML Reporter**
Generates a self-contained folder with interactive web-based results.

**JSON & JUnit Reporters**
Produce structured output formats suitable for integration with other tools and CI/CD systems.

**Blob Reporter**
Facilitates merging reports from sharded test runs, storing complete test details.

**GitHub Actions Reporter**
Automatically generates annotations within GitHub Actions workflows.

([Playwright Reporters][8])

### Custom Reporters

Developers can implement custom reporters by creating a class implementing the Reporter interface with methods like `onBegin()`, `onTestEnd()`, and `onEnd()`. These are registered via configuration or command-line arguments. Multiple reporters can run simultaneously. ([Playwright Reporters][8])

## Best Practices

### Locator Selection
1. Prefer role-based locators for interactive elements
2. Use text locators for non-interactive content
3. Avoid CSS and XPath selectors due to fragility
4. Use test IDs as a fallback strategy

### Test Design
1. Leverage auto-waiting instead of manual waits
2. Use test isolation for independent test execution
3. Enable parallelization for faster test runs
4. Configure retries for flaky test mitigation

### Debugging
1. Use trace viewer for CI failure investigation
2. Enable traces on first retry in CI environments
3. Leverage UI mode for local development debugging
4. Use soft assertions for comprehensive validation

### Configuration
1. Keep test runner options at top-level, not in `use` section
2. Configure `forbidOnly` for CI environments
3. Use project-specific configurations for multi-browser testing
4. Integrate web server launching for development workflows

## References

[1]: https://playwright.dev/docs/intro "Playwright Introduction"
[2]: https://playwright.dev/docs/api/class-playwright "Playwright API Reference"
[3]: https://playwright.dev/docs/test-configuration "Playwright Test Configuration"
[4]: https://playwright.dev/docs/locators "Playwright Locators"
[5]: https://playwright.dev/docs/writing-tests "Playwright Writing Tests"
[6]: https://playwright.dev/docs/test-assertions "Playwright Test Assertions"
[7]: https://playwright.dev/docs/trace-viewer "Playwright Trace Viewer"
[8]: https://playwright.dev/docs/test-reporters "Playwright Test Reporters"
