---
title: "Playwright MCP Server"
description: "Model Context Protocol server for browser automation with Playwright"
type: "integration-guide"
tags: ["playwright", "mcp", "browser-automation", "accessibility", "model-context-protocol", "llm", "testing"]
category: "ts"
subcategory: "mcp"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Playwright MCP GitHub Repository"
    url: "https://github.com/microsoft/playwright-mcp"
  - name: "Playwright MCP NPM Package"
    url: "https://www.npmjs.com/package/@playwright/mcp"
related: ["playwright-framework-guide.md", "../../claude/mcp-integration.md"]
author: "unknown"
contributors: []
---

# Playwright MCP Server

The Playwright MCP server is a Model Context Protocol implementation that enables LLMs to automate browser interactions. Rather than relying on screenshots or vision models, it provides structured accessibility snapshots for text-based interaction with web pages. ([Playwright MCP GitHub][1])

## Overview

### What Is It?

The Playwright MCP server bridges the Model Context Protocol with Playwright's browser automation capabilities, allowing AI assistants to interact with web pages through structured data rather than visual analysis. ([Playwright MCP GitHub][1])

### Key Features

**Text-Based Operations**: Uses accessibility trees instead of pixel analysis, making it faster and more efficient for LLM processing. ([Playwright MCP GitHub][1])

**No Vision Models Required**: Operates entirely on structured data, eliminating the need for screenshot analysis or visual perception. ([Playwright MCP GitHub][1])

**Deterministic Interactions**: Reduces ambiguity compared to screenshot-dependent approaches by using semantic element references. ([Playwright MCP GitHub][1])

**Multi-Browser Support**: Works with Chromium, Firefox, and WebKit, providing cross-browser testing capabilities. ([Playwright MCP GitHub][1])

**Flexible Deployment**: Runs locally, in Docker, or as a standalone HTTP service for various deployment scenarios. ([Playwright MCP GitHub][1])

## Installation

### Prerequisites

Install required package managers:

```bash
brew install node    # Node.js runtime
```

### MCP Client Integration

The server integrates with multiple MCP clients:

#### Claude Code

```bash
claude mcp add --transport stdio playwright \
  -- npx @playwright/mcp@latest
```

#### VS Code/Insiders

One-click installation via MCP protocol.

#### Cursor

Browser-based installation button or manual config.

#### Claude Desktop

Standard MCP setup via configuration file:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

([Playwright MCP GitHub][1])

#### Other Clients

Goose, Windsurf, and LM Studio each have native integration support. ([Playwright MCP GitHub][1])

### Docker Deployment

Pre-built image available at `mcr.microsoft.com/playwright/mcp`. The Docker implementation only supports headless chromium at the moment, but enables portable deployment across environments. ([Playwright MCP GitHub][1])

```bash
docker run -p 8931:8931 mcr.microsoft.com/playwright/mcp
```

## Configuration

### CLI Arguments

The server supports extensive CLI arguments for customization:

#### Browser Control

- `--browser` - Browser engine selection (chromium, firefox, webkit)
- `--headless` - Run browser without UI
- `--device` - Emulate specific device profiles
- `--executable-path` - Custom browser binary path

#### Network Configuration

- `--allowed-origins` - Whitelist specific domains
- `--blocked-origins` - Blacklist specific domains
- `--proxy-server` - Proxy server configuration

#### Storage & State

- `--user-data-dir` - Persistent browser profile directory
- `--storage-state` - Session state file for maintaining login
- `--isolated` - Fresh context for each session

#### Performance & Timeouts

- `--timeout-action` - Action timeout duration
- `--timeout-navigation` - Navigation timeout duration
- `--viewport-size` - Browser viewport dimensions

#### Output & Debugging

- `--output-dir` - Directory for artifacts
- `--save-trace` - Enable trace recording
- `--save-video` - Enable video recording

([Playwright MCP GitHub][1])

### Configuration File

Configuration can also be specified via JSON file with `--config` parameter:

```json
{
  "browser": "chromium",
  "headless": true,
  "viewport": {
    "width": 1280,
    "height": 720
  },
  "timeout": {
    "action": 30000,
    "navigation": 60000
  },
  "output": {
    "dir": "./artifacts",
    "trace": true,
    "video": false
  }
}
```

Then run with:

```bash
npx @playwright/mcp@latest --config playwright-mcp.json
```

## User Profile Modes

The server supports three profile modes for different use cases:

### 1. Persistent Mode

Maintains logged-in sessions across uses, storing cookies, local storage, and authentication state:

```bash
npx @playwright/mcp@latest --user-data-dir ./profile
```

**Use case**: Testing authenticated workflows without repeated login.

### 2. Isolated Mode

Fresh context for each session; useful for testing:

```bash
npx @playwright/mcp@latest --isolated
```

**Use case**: Clean-state testing, avoiding session pollution.

### 3. Browser Extension Mode

Connects to existing browser tabs with active sessions:

```bash
npx @playwright/mcp@latest --connect-to-browser
```

**Use case**: Debugging live sessions, working with existing auth.

([Playwright MCP GitHub][1])

## Core Tools Available

### Automation Tools

#### browser_click

Single/double clicks with modifiers:

```typescript
// Example capability
click(element, { button: 'left' | 'right', modifiers: ['Control', 'Shift'] })
```

#### browser_drag

Drag-and-drop operations between elements.

#### browser_fill

Form field population with multiple fields:

```typescript
// Example capability
fill([
  { field: 'username', value: 'user@example.com' },
  { field: 'password', value: 'secret123' }
])
```

#### browser_goto

Navigate to URLs:

```typescript
// Example capability
goto('https://example.com')
```

#### browser_scroll

Page scrolling with directional control.

([Playwright MCP GitHub][1])

### Information Retrieval Tools

#### browser_snapshot

Accessibility tree capture providing structured DOM representation:

```typescript
// Returns accessibility tree JSON
{
  "role": "WebArea",
  "name": "Page Title",
  "children": [
    { "role": "button", "name": "Submit", "ref": "elem-123" }
  ]
}
```

This is the core feature enabling text-based LLM interaction.

#### browser_console_messages

Error/warning logs from browser console.

#### browser_evaluate

JavaScript execution in browser context:

```typescript
// Example capability
evaluate('() => document.title')
```

#### browser_find_elements

Element discovery using selectors or text content.

([Playwright MCP GitHub][1])

### Advanced Tools

Capability-dependent features include:

- **PDF generation** - Export pages to PDF format
- **Vision-based coordinate interactions** - Fallback to coordinate clicking
- **Tab management** - Multiple tab orchestration

([Playwright MCP GitHub][1])

## Deployment Scenarios

### Local Development

Standard NPX installation suitable for individual developer environments:

```bash
npx @playwright/mcp@latest
```

**Best for**: Development, testing, debugging.

### Headless/Server Environments

Use `--port` flag for HTTP transport when display is unavailable:

```bash
npx @playwright/mcp@latest --port 8931
```

**Best for**: CI/CD pipelines, cloud servers, containerized environments. ([Playwright MCP GitHub][1])

### Docker Containerized

Enables portable deployment across environments:

```bash
docker run -p 8931:8931 mcr.microsoft.com/playwright/mcp --headless
```

**Best for**: Production deployments, reproducible environments.

### Programmatic Embedding

Can be embedded directly using Node.js APIs with custom transports:

```typescript
import { PlaywrightMCP } from '@playwright/mcp';

const server = new PlaywrightMCP({
  transport: customTransport,
  browser: 'chromium',
  headless: true
});

await server.start();
```

**Best for**: Custom integrations, specialized workflows.

([Playwright MCP GitHub][1])

## Output & Artifacts

With `--output-dir`, the server can generate:

### Session Recordings

Complete session recordings for playback and analysis.

### Performance Traces

Playwright traces showing:
- Action timeline
- Network requests
- Console logs
- Screenshots at each step

### Video Captures

Specify dimensions like `800x600`:

```bash
npx @playwright/mcp@latest --save-video --viewport-size 800x600
```

### Storage State Snapshots

Exportable authentication and session state:

```bash
npx @playwright/mcp@latest --storage-state ./auth.json
```

This enables reusing login sessions across runs.

([Playwright MCP GitHub][1])

## Security Considerations

### Origin Control

**Allowlisting**:
```bash
npx @playwright/mcp@latest --allowed-origins "https://example.com,https://trusted.com"
```

**Blocklisting**:
```bash
npx @playwright/mcp@latest --blocked-origins "https://malicious.com"
```

### Additional Security Features

- **HTTPS error tolerance configuration** - Control SSL error handling
- **Service worker blocking** - Prevent service worker interference
- **Sandbox control** - Browser process isolation
- **Session-scoped permissions** - Granular permission management

([Playwright MCP GitHub][1])

### Best Practices

**Validate URLs**: Always validate and sanitize URLs before navigation.

**Limit origins**: Use allowlists to restrict accessible domains.

**Review permissions**: Grant minimum necessary permissions for automation tasks.

**Audit logs**: Monitor console messages and network activity for suspicious behavior.

## Accessibility-First Architecture

### Why Accessibility Trees?

The server emphasizes accessibility-first automation suitable for agentic AI workflows without requiring visual perception capabilities. ([Playwright MCP GitHub][1])

**Benefits**:
- **Faster processing** - Text is more compact than images
- **Deterministic** - Semantic references are more reliable than pixel coordinates
- **Screen reader parity** - Interactions match how assistive technology works
- **Resilient** - Less brittle than visual selectors

### Accessibility Snapshot Structure

```json
{
  "role": "button",
  "name": "Submit Form",
  "ref": "elem-abc123",
  "focused": false,
  "disabled": false,
  "expanded": null,
  "level": null,
  "children": []
}
```

**Key fields**:
- `role` - ARIA role (button, link, textbox, etc.)
- `name` - Accessible name (visible text or aria-label)
- `ref` - Unique reference for interaction
- `focused`, `disabled`, `expanded` - Element state
- `children` - Nested accessibility tree

This structure enables LLMs to understand page semantics without visual analysis.

## Example Workflows

### Form Filling & Submission

```typescript
// AI workflow example (conceptual)
1. Navigate: browser_goto('https://example.com/form')
2. Snapshot: browser_snapshot() -> get accessibility tree
3. Fill: browser_fill([
     { name: 'Email', value: 'user@example.com' },
     { name: 'Password', value: 'secret' }
   ])
4. Click: browser_click({ element: 'Submit', ref: 'elem-123' })
```

### Web Scraping

```typescript
// AI workflow example (conceptual)
1. Navigate: browser_goto('https://news.example.com')
2. Snapshot: browser_snapshot() -> get article structure
3. Evaluate: browser_evaluate('() => Array.from(document.querySelectorAll("article")).map(a => a.textContent)')
4. Extract: Parse and structure content
```

### Authentication Testing

```typescript
// AI workflow example (conceptual)
1. Navigate: browser_goto('https://app.example.com/login')
2. Fill: browser_fill([{ name: 'username', value: 'test@example.com' }])
3. Fill: browser_fill([{ name: 'password', value: 'test123' }])
4. Click: browser_click({ element: 'Login' })
5. Wait: Verify redirect to dashboard
6. Save state: --storage-state ./authenticated.json
```

### Multi-Tab Orchestration

```typescript
// AI workflow example (conceptual)
1. Open tabs: Create multiple browser contexts
2. Navigate each: Different URLs per tab
3. Coordinate: Share data between tabs
4. Aggregate: Collect results from all tabs
```

## Integration with Claude Code

### Setup

```bash
claude mcp add --transport stdio playwright \
  -- npx @playwright/mcp@latest
```

### Usage Patterns

**Natural language queries**: "Navigate to example.com and fill out the contact form with my details."

**Resource references**: `@playwright:snapshot://current-page`

**Tool invocation**: Claude automatically selects appropriate Playwright tools based on your request.

### Example Session

```
User: Open google.com and search for "playwright testing"

Claude uses:
1. browser_goto('https://google.com')
2. browser_snapshot() -> find search box
3. browser_fill([{ name: 'Search', value: 'playwright testing' }])
4. browser_click({ element: 'Google Search' })
5. browser_snapshot() -> capture results
```

## Troubleshooting

### Browser Not Launching

**Check Node.js version**: Ensure Node.js 20.x, 22.x, or 24.x is installed.

**Install browsers**: Run `npx playwright install` to download browser binaries.

**Check permissions**: Ensure execute permissions on browser binaries.

### Headless Mode Issues

**Display errors**: Use `--headless` flag when running without display server.

**Screenshot failures**: Headless mode requires explicit viewport size:
```bash
npx @playwright/mcp@latest --headless --viewport-size 1280x720
```

### Connection Timeout

**Increase timeouts**:
```bash
npx @playwright/mcp@latest --timeout-navigation 60000
```

**Check network**: Verify network connectivity and proxy settings.

### Storage State Not Persisting

**Verify path**: Ensure `--storage-state` path is writable.

**Check format**: Storage state must be valid JSON.

**Session expiration**: Some sites invalidate sessions quickly; re-authenticate as needed.

### MCP Client Connection

**Verify installation**:
```bash
claude mcp list
```

**Debug mode**:
```bash
claude --mcp-debug
```

**Check transport**: Ensure stdio transport is configured correctly.

## Best Practices

### Performance Optimization

**Headless mode**: Use `--headless` for faster execution without UI overhead.

**Selective tracing**: Enable `--save-trace` only when debugging, not in production.

**Viewport size**: Use smaller viewports for faster rendering:
```bash
npx @playwright/mcp@latest --viewport-size 800x600
```

**Browser selection**: Chromium is typically fastest for automation.

### Reliability

**Wait for actionability**: Playwright auto-waits; trust the built-in waiting mechanisms.

**Use accessibility references**: Prefer `ref` from snapshots over brittle selectors.

**Handle navigation**: Allow sufficient navigation timeout for slow pages.

**State management**: Use `--storage-state` to avoid repeated authentication.

### Maintainability

**Configuration files**: Use `--config` for complex setups instead of long CLI arguments.

**Origin allowlists**: Explicitly define allowed domains for security and clarity.

**Artifact organization**: Use `--output-dir` to centralize traces, videos, and screenshots.

**Documentation**: Document custom configuration for team sharing.

## Limitations

### Current Constraints

**Docker browser support**: The Docker implementation only supports headless chromium at the moment. ([Playwright MCP GitHub][1])

**Vision features**: Vision-based coordinate interactions are capability-dependent and not always available.

**Plugin support**: Browser extensions may not work in all modes.

### Workarounds

**Multi-browser Docker**: Run separate containers for Firefox and WebKit if needed.

**Extension testing**: Use `--user-data-dir` with local browser profile containing extensions.

**Coordinate clicking**: Falls back to vision-based clicking when accessibility tree is insufficient.

## Repository Details

- **License**: Apache 2.0
- **Repository**: microsoft/playwright-mcp on GitHub
- **NPM Package**: `@playwright/mcp@latest`
- **Maintainer**: Microsoft (22.7k+ stars, active development)

([Playwright MCP GitHub][1])

## References

[1]: https://github.com/microsoft/playwright-mcp "Playwright MCP GitHub Repository"
