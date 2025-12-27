---
title: "Biome Reference Index"
description: "Reference documentation for Biome web toolchain"
type: "meta"
tags: ["index", "biome", "toolchain", "reference"]
category: "ts"
subcategory: "dev-tools"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources: []
related: ["biome-v2-tool-reference.md", "lint-rules-guide.md"]
author: "unknown"
contributors: []
---

# Biome Reference Index

Comprehensive reference documentation for Biome, a fast web development toolchain that combines formatting, linting, and type-aware analysis.

## Documentation Files

### [Biome v2 Tool Reference](biome-v2-tool-reference.md)
Complete guide to Biome v2 and v2.3, covering:
- Core capabilities (formatting, linting, type-aware analysis)
- Installation and migration from v1
- Supported languages (JavaScript, TypeScript, JSON, HTML, CSS, GraphQL, Vue, Svelte, Astro)
- Major v2 features (multi-file analysis, monorepo support, plugin system, import organizer)
- Framework support (experimental Vue/Svelte/Astro)
- Configuration reference (file processing, VCS integration, formatter/linter options)
- CLI commands and usage
- Performance characteristics and editor integration

### [Lint Rules Guide](lint-rules-guide.md)
Comprehensive guide to Biome's 364 lint rules, covering:
- Rule categories (accessibility, complexity, correctness, nursery, performance, security, style, suspicious)
- Rule naming conventions and organization
- Configuration syntax and severity levels
- Rule options and customization
- Suppression techniques (inline, file-level, range-based)
- Rule sources (ESLint, TypeScript ESLint, React, Unicorn, etc.)
- Detailed rule examples (noUnusedVariables, useStrictMode)
- Migration from ESLint
- Performance considerations
- Best practices and troubleshooting

## External Resources

- [Official Biome Documentation](https://biomejs.dev/)
- [Biome v2 Release Announcement](https://biomejs.dev/blog/biome-v2/)
- [Biome v2.3 Release Announcement](https://biomejs.dev/blog/biome-v2-3/)
- [Configuration Reference](https://biomejs.dev/reference/configuration/)
- [GitHub Repository](https://github.com/biomejs/biome)
- [Web Playground](https://biomejs.dev/playground/)

## Quick Start

```bash
# Install
npm install --save-dev --save-exact @biomejs/biome

# Initialize configuration
npx @biomejs/biome init

# Format and lint
npx @biomejs/biome check --write ./src
```

## Key Features

- **Fast**: 35x faster than Prettier on large codebases
- **Type-aware**: Linting with type inference without TypeScript compiler
- **Unified**: Single tool for formatting, linting, and code quality
- **97% Prettier Compatible**: Easy migration from existing workflows
- **364 Lint Rules**: Sourced from ESLint, TypeScript ESLint, and others
- **Multi-language**: JavaScript, TypeScript, JSON, HTML, CSS, GraphQL, and more
