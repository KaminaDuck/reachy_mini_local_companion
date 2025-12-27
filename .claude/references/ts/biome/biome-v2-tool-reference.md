---
title: "Biome v2 Tool Reference"
description: "Comprehensive guide to Biome v2 web toolchain with type-aware linting"
type: "tool-reference"
tags: ["biome", "linter", "formatter", "typescript", "javascript", "toolchain", "rust", "performance"]
category: "ts"
subcategory: "dev-tools"
version: "2.3"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Biome v2 Release"
    url: "https://biomejs.dev/blog/biome-v2/"
  - name: "Biome v2.3 Release"
    url: "https://biomejs.dev/blog/biome-v2-3/"
  - name: "Biome Documentation"
    url: "https://biomejs.dev/"
  - name: "Biome Configuration Reference"
    url: "https://biomejs.dev/reference/configuration/"
related: ["lint-rules-guide.md"]
author: "unknown"
contributors: []
---

# Biome v2 Tool Reference

Biome is a comprehensive web development toolchain that combines formatting, linting, and code quality features into a single, fast application built with Rust. ([Biome Docs][1]) Version 2, codenamed "Biotype," introduces type-aware linting without requiring the TypeScript compiler, positioning itself as a next-generation alternative to ESLint, Prettier, and other traditional tools. ([Biome v2 Release][2])

## Core Capabilities

Biome provides three primary functions in a unified toolchain:

**Formatting**: Code formatter supporting JavaScript, TypeScript, JSX, TSX, JSON, HTML, CSS, and GraphQL with 97% compatibility with Prettier while running approximately 35x faster on large codebases (tested on 171,127 lines across 2,104 files). ([Biome Docs][1])

**Linting**: Includes 364 rules sourced from ESLint, TypeScript ESLint, and other tools, with detailed and contextualized diagnostics. ([Biome Docs][1])

**Type-Aware Analysis**: Version 2 introduces type inference without requiring the TypeScript compiler, with early testing showing the `noFloatingPromises` rule detects floating promises in approximately 75% of cases comparable to `typescript-eslint` with significantly lower performance overhead. ([Biome v2 Release][2])

## Installation

Install via npm with exact version pinning:

```bash
npm install --save-dev --save-exact @biomejs/biome
```

For migration from v1 to v2:

```bash
npm install --save-dev --save-exact @biomejs/biome
npx @biomejs/biome migrate --write
```

The `migrate` command automatically handles configuration breaking changes. ([Biome v2 Release][2])

## Basic Usage

**Format files**:
```bash
npx @biomejs/biome format --write ./src
```

**Lint files**:
```bash
npx @biomejs/biome lint --write ./src
```

**Combined check** (formatting and linting simultaneously):
```bash
npx @biomejs/biome check --write ./src
```

([Biome Docs][1])

## Supported Languages

- JavaScript & TypeScript (including JSX/TSX variants)
- JSON (with optional comments and trailing commas)
- HTML (experimental formatter in v2+)
- CSS (with Tailwind v4 support in v2.3+)
- GraphQL
- Vue, Svelte, and Astro (experimental in v2.3+)

([Biome Docs][1], [Biome v2.3 Release][3])

## Version 2 Major Features

### Multi-File Analysis & Type Inference

Biome v2 includes a new file scanner that indexes project files similarly to IDE LSP services, enabling type inference queries that require cross-file information. ([Biome v2 Release][2])

**Performance-conscious design**:
- Full scans only activate when "project domain" rules are enabled
- Opt-in functionality prevents v1-to-v2 slowdowns
- Users control scanned files via `files.includes` configuration (excluding `node_modules` by default)

([Biome v2 Release][2])

### Monorepo Support

Nested configuration files are now supported throughout projects:

```json
{
  "root": false,
  "extends": "//"
}
```

The convenient `"extends": "//"` syntax eliminates complex relative paths like `"extends": ["../../biome.json"]`. Individual nested configs don't inherit root settings by default; use the `extends` field for explicit inheritance. ([Biome v2 Release][2])

### Plugin System

Linter plugins in the initial iteration match code patterns and report diagnostics:

```
`$fn($args)` where {
    $fn <: `Object.assign`,
    register_diagnostic(
        span = $fn,
        message = "Prefer object spread"
    )
}
```

Distribution methods are still under discussion. ([Biome v2 Release][2])

### Import Organizer Revamp

Enhanced import organization resolves v1.x limitations:

- **Blank-line handling**: Reorganizes imports across separators intelligently
- **Import merging**: Combines multiple imports from identical modules
- **Custom ordering**: Configurable grouping (Node, internal, external packages)
- **Export support**: Now organizes `export` statements
- **Enhanced features**: Comment separation, import attribute sorting

([Biome v2 Release][2])

### Assists Framework

New generalized system for code actions without diagnostics:

- **Import Organizer**: Moved from special case to assist action
- **`useSortedKeys`**: Sorts object literal keys
- **`useSortedAttributes`**: Organizes JSX attributes

([Biome v2 Release][2])

### Suppression Improvements

Added comment-based suppression options:

```javascript
// biome-ignore-all: Suppresses rules/formatter across entire files
function example() {
  // biome-ignore-start
  // Code in this block is ignored
  // biome-ignore-end
}
```

The end comment is optional. ([Biome v2 Release][2])

### HTML Formatter (Experimental)

Experimental formatter covering `.html` files (Vue/Svelte support added in v2.3):

- Parses 46/124 of Prettier's test suite successfully
- Implements `attributePosition`, `bracketSameLine`, `whitespaceSensitivity` options
- Disabled by default; enable via configuration:

```json
{
  "html": {
    "formatter": {
      "enabled": true
    }
  }
}
```

Embedded language formatting (JavaScript, CSS) not yet supported in v2.0. ([Biome v2 Release][2])

## Version 2.3 Features

### Framework Support

Experimental support for Vue, Svelte, and Astro files, allowing formatting and linting of JavaScript/TypeScript within `<script>` tags and CSS within `<style>` tags. Must be explicitly enabled:

```json
{
  "html": {
    "experimentalFullSupportEnabled": true
  }
}
```

([Biome v2.3 Release][3])

### Tailwind CSS v4

Native support for Tailwind directives as an opt-in feature:

```json
{
  "css": {
    "parser": {
      "tailwindDirectives": true
    }
  }
}
```

([Biome v2.3 Release][3])

### Improved Ignore Syntax

Refined ignore pattern system with two levels of exclusion:

- Single exclamation (`!pattern`): Excludes from linting/formatting but allows type indexing
- Double exclamation (`!!pattern`): Completely removes paths from all Biome operations

The deprecated `files.experimentalScannerIgnores` option should be migrated away from. ([Biome v2.3 Release][3])

### Additional v2.3 Improvements

- New `indentScriptAndStyle` option controls indentation in script and style blocks
- `lineEnding` format option now supports `"auto"` for OS-appropriate line endings
- Enhanced `init` command auto-detects `.gitignore` files and `dist/` directories
- `--skip` and `--only` flags now accept lint domains
- New reporters: checkstyle and RDJSON formats

([Biome v2.3 Release][3])

## Configuration

### Configuration File

Biome uses `biome.json` or `biome.jsonc` for configuration. ([Biome Configuration][4])

**Basic configuration example**:

```json
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### Root-Level Settings

**`$schema`**: Points to JSON schema for validation. ([Biome Configuration][4])

**`extends`**: Paths to other config files, resolving from least to most relevant. Supports `"//"` for monorepo setups in v2+. ([Biome Configuration][4])

**`root`**: Boolean flag (default: `true`) indicating root configuration. Nested configs require `"root": false`. ([Biome Configuration][4])

### File Processing

**`files.includes`**: Glob patterns determining which files to process. Supports negated patterns (`!pattern`) and force-ignore patterns (`!!pattern`). ([Biome Configuration][4])

**`files.ignoreUnknown`**: When `true`, suppresses diagnostics for unsupported file types (default: `false`). ([Biome Configuration][4])

**`files.maxSize`**: Maximum file size in bytes; default is 1MB (1048576). ([Biome Configuration][4])

### VCS Integration

```json
{
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true,
    "root": ".",
    "defaultBranch": "main"
  }
}
```

([Biome Configuration][4])

### Formatter Options

**Common options**:
- `enabled`: Toggle formatter (default: `true`)
- `indentStyle`: `"tab"` or `"space"` (default: `"tab"`)
- `indentWidth`: Spaces per indent (default: `2`)
- `lineEnding`: `"lf"`, `"crlf"`, `"cr"`, or `"auto"` (v2.3+, default: `"lf"`)
- `lineWidth`: Characters per line (default: `80`)
- `bracketSpacing`: Add spaces around brackets (default: `true`)

([Biome Configuration][4])

**JavaScript/TypeScript specific**:

```json
{
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded",
      "arrowParentheses": "asNeeded",
      "trailingCommas": "all",
      "operatorLinebreak": "after"
    }
  }
}
```

([Biome Configuration][4])

**HTML specific**:

```json
{
  "html": {
    "formatter": {
      "enabled": true,
      "attributePosition": "auto",
      "whitespaceSensitivity": "css",
      "selfCloseVoidElements": "never",
      "indentScriptAndStyle": true
    }
  }
}
```

([Biome Configuration][4])

### Linter Configuration

**Rule groups**: accessibility, complexity, correctness, nursery, performance, security, style, suspicious. Each accepts severity levels: `"on"`, `"off"`, `"info"`, `"warn"`, `"error"`. ([Biome Configuration][4])

**Example**:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error"
      },
      "suspicious": {
        "noFloatingPromises": "warn"
      }
    }
  }
}
```

### Overrides

Apply configuration changes to specific file patterns:

```json
{
  "overrides": [
    {
      "includes": ["generated/**"],
      "formatter": {
        "lineWidth": 160
      }
    },
    {
      "includes": ["**/*.test.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    }
  ]
}
```

Patterns are evaluated in order; first match applies. ([Biome Configuration][4])

## Glob Pattern Syntax

- `*`: Matches characters except `/`
- `**`: Recursive directory matching (must be entire path component)
- `[...]`: Character ranges (e.g., `[0-9]`)
- `[!...]`: Negation of character class
- `!pattern`: Negated glob (excludes matches)
- `!!pattern`: Force-ignore pattern (prevents scanner indexing)

Example: `"**/*.js"` matches all JavaScript files recursively. ([Biome Configuration][4])

## CLI Commands

**Format**:
```bash
biome format --write ./src
```

**Lint**:
```bash
biome lint --write ./src
```

**Check** (format + lint):
```bash
biome check --write ./src
```

**Migrate configuration**:
```bash
biome migrate --write
```

**Initialize project**:
```bash
biome init
```

The `init` command in v2.3+ auto-detects `.gitignore` files and `dist/` directories. ([Biome v2.3 Release][3])

**CLI flags** (v2.3+):
- `--skip <domain>`: Skip specific lint domains
- `--only <domain>`: Only run specific lint domains
- `--format-with-errors`: Continue formatting despite errors
- `--css-parse-tailwind-directives`: Enable Tailwind directive parsing
- `--json-parse-allow-comments`: Allow comments in JSON

([Biome v2.3 Release][3])

## Performance Characteristics

- Approximately 35x faster than Prettier on large codebases
- Built with Rust using rust-analyzer architecture
- Multi-file analysis is opt-in to prevent performance degradation
- File scanner only performs full scans when project-domain rules are enabled

([Biome Docs][1], [Biome v2 Release][2])

## Editor Integration

Biome provides editor plugins for:
- Visual Studio Code
- Other editors via LSP

A web-based playground is also available for testing. ([Biome Docs][1])

## Migration from Other Tools

### From Prettier

Biome achieves 97% compatibility with Prettier. Key differences should be verified during migration. ([Biome Docs][1])

### From ESLint

Biome includes 364 rules sourced from ESLint and TypeScript ESLint. Review the rule mapping documentation for specific equivalents. ([Biome Docs][1])

### From v1 to v2

Run the automated migration command:

```bash
npx @biomejs/biome migrate --write
```

This handles configuration breaking changes automatically. Manual updates may be needed for complex scenarios. ([Biome v2 Release][2])

## Roadmap

2025 priorities include:

- Stabilize HTML formatter
- Expand HTML support to Vue, Svelte, Astro
- Implement Markdown parser and support
- Enhance type inference coverage
- Develop additional rules

([Biome v2 Release][2])

## Contributing

Contribution opportunities:

- **Translations**: 125+ language support dashboard available
- **Parsers**: HTML, Markdown, YAML, and JavaScript/TypeScript enhancements
- **Lint rules**: Implement ESLint, plugin, and framework-specific rules
- **Editor integration**: VS Code, Zed, and JetBrains improvements
- **Financial support**: Open Collective, GitHub Sponsors, enterprise programs

([Biome v2 Release][2])

## References

[1]: https://biomejs.dev/ "Biome Documentation"
[2]: https://biomejs.dev/blog/biome-v2/ "Biome v2 Release"
[3]: https://biomejs.dev/blog/biome-v2-3/ "Biome v2.3 Release"
[4]: https://biomejs.dev/reference/configuration/ "Biome Configuration Reference"
