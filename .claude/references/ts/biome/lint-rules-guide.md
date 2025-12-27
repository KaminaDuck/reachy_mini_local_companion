---
title: "Biome Lint Rules Guide"
description: "Comprehensive guide to Biome's 364 lint rules and configuration"
type: "config-reference"
tags: ["biome", "linter", "lint-rules", "code-quality", "static-analysis", "eslint", "typescript"]
category: "ts"
subcategory: "dev-tools"
version: "2.3"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Biome Linter Documentation"
    url: "https://biomejs.dev/linter/"
  - name: "Biome Rules Sources"
    url: "https://biomejs.dev/linter/rules-sources/"
  - name: "Biome Linter Configuration"
    url: "https://biomejs.dev/reference/configuration/#linter"
  - name: "Biome Suppressions"
    url: "https://biomejs.dev/linter/#ignoring-code"
related: ["biome-v2-tool-reference.md"]
author: "unknown"
contributors: []
---

# Biome Lint Rules Guide

Biome's linter performs static code analysis across multiple languages, offering 364 rules to identify errors and enforce modern coding practices. It distinguishes itself by separating formatting concerns—the formatter handles those—and focusing purely on code quality issues. ([Biome Linter][1])

## Core Concepts

### Rule Naming Convention

Rules follow a consistent naming pattern: `use*` rules enforce practices, while `no*` rules prohibit them. Biome typically converts kebab-case ESLint rule names to camelCase (e.g., "no-console" becomes `noConsole`). ([Biome Linter][1], [Rules Sources][2])

### Fix Types

Rules may emit two types of fixes:

- **Safe fixes**: Guaranteed semantic preservation; applicable on save
- **Unsafe fixes**: May alter program behavior; require manual review

([Biome Linter][1])

## Rule Categories

Biome organizes linter rules into eight groups, each focusing on specific code quality aspects. ([Linter Config][3])

### Accessibility (`a11y`)

Prevents accessibility problems in web applications. These rules ensure your code follows WCAG guidelines and best practices for inclusive design.

**Common rules**:
- Rules adapted from eslint-plugin-jsx-a11y
- Focus on ARIA attributes, semantic HTML, keyboard navigation

### Complexity

Inspects complex code that could be simplified. These rules identify overly complex logic that may be harder to maintain and test.

**Focus areas**:
- Cyclomatic complexity
- Nested structures
- Code that can be refactored for clarity

### Correctness

Detects guaranteed incorrect or useless code. These rules catch bugs and logic errors that would cause runtime issues.

**Example rules**:
- `noUnusedVariables` - Identifies variables that are declared but never used
- `noUndeclaredVariables` - Catches references to undefined variables
- Type-related errors in TypeScript code

### Nursery

Unstable rules under development. These rules are opt-in on stable versions and may change behavior or graduate to other categories.

**Characteristics**:
- Experimental status
- May have false positives
- Subject to breaking changes
- Provide early access to new rules

([Linter Config][3])

### Performance

Identifies ways to write faster and more efficient code. These rules suggest optimizations that improve runtime performance.

**Focus areas**:
- Unnecessary operations
- Inefficient patterns
- Performance anti-patterns

### Security

Detects potential security flaws in code. These rules help prevent common vulnerabilities and insecure coding practices.

**Common patterns**:
- Dangerous function usage
- Security-sensitive configurations
- Potential injection vulnerabilities

### Style

Enforces consistent, idiomatic code writing. These rules promote readability and maintainability through consistent patterns.

**Example patterns**:
- Naming conventions
- Code organization
- Consistent syntax usage

([Linter Config][3])

### Suspicious

Finds likely incorrect or useless code. These rules catch code that technically works but is probably not what you intended.

**Example rules**:
- `useStrictMode` - Enforces `"use strict"` directive in script files
- Code that appears to be incomplete or mistaken
- Patterns that suggest developer error

([Linter Config][3])

## Rule Sources

Biome's 364 rules come from multiple established linting ecosystems. ([Rules Sources][2])

### Biome Exclusive Rules

Approximately 33 proprietary rules unique to Biome:

- `noAccumulatingSpread` - Prevents performance issues with spread operators
- `noConstEnum` - Discourages TypeScript const enums
- `noDelete` - Prevents use of the `delete` operator
- `noEnum` - Discourages TypeScript enums
- `useStrictMode` - Enforces strict mode in scripts
- `useSortedClasses` - Enforces sorted utility class names

([Rules Sources][2])

### Adapted from External Sources

**JavaScript/TypeScript Core**:
- ESLint core rules (`noUndeclaredVariables`, `noDebugger`)
- TypeScript-ESLint (`useExplicitType`, type-aware rules)

**React Ecosystem**:
- jsx-a11y (accessibility rules)
- react-hooks (hooks rules)
- react-refresh (fast refresh compatibility)
- Next.js ESLint plugin (`useGoogleFontDisplay`, `noImgElement`)

**Code Quality Tools**:
- eslint-plugin-unicorn
- eslint-plugin-sonarjs
- eslint-plugin-import

**Specialized Domains**:
- Stylelint (CSS validation)
- GraphQL-ESLint (schema rules)
- Clippy (Rust linter concepts adapted for JavaScript)

([Rules Sources][2])

## Configuration

### Basic Configuration

Enable/disable linting in `biome.json`:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

([Linter Config][3])

### Severity Levels

Configure rule severity using these values:

- `"on"`: Emits diagnostics with the rule's default severity
- `"off"`: Suppresses all diagnostics for the group
- `"info"`: Informational diagnostic (doesn't fail builds)
- `"warn"`: Warning diagnostic (doesn't fail builds by default)
- `"error"`: Error diagnostic (fails builds)

([Linter Config][3])

**Example - Configure entire group**:

```json
{
  "linter": {
    "rules": {
      "a11y": "info",
      "correctness": "error"
    }
  }
}
```

### Disabling Specific Rules

Disable individual rules or groups:

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noDebugger": "off"
      },
      "style": "off"
    }
  }
}
```

([Biome Linter][1])

### Rule Options

Many rules accept configuration options. Use the object syntax with `level` and `options` properties:

```json
{
  "linter": {
    "rules": {
      "style": {
        "useNamingConvention": {
          "level": "error",
          "options": {
            "strictCase": false
          }
        }
      },
      "correctness": {
        "noUnusedVariables": {
          "level": "error",
          "options": {
            "ignoreRestSiblings": true
          }
        }
      }
    }
  }
}
```

The `options` object contents vary by rule. Consult individual rule documentation for available options. ([Biome Linter][1])

### Recommended Rules

Enable all recommended rules across groups:

```json
{
  "linter": {
    "rules": {
      "recommended": true
    }
  }
}
```

Or enable recommended rules for specific groups:

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "recommended": true
      }
    }
  }
}
```

([Linter Config][3])

### File Includes/Excludes

Control which files to lint:

```json
{
  "linter": {
    "enabled": true,
    "includes": ["src/**/*.ts", "src/**/*.tsx"]
  }
}
```

**Important notes**:
- `linter.includes` is applied after `files.includes`
- Files inside `node_modules/` are always ignored
- Negated patterns require an initial `**` to match correctly
- Supports `!` (exclude) and `!!` (force-ignore) patterns

([Linter Config][3])

## Suppression

Biome provides multiple mechanisms to suppress lint violations when needed. ([Suppressions][4])

### Inline Suppression

Suppress violations at the specific code location:

```javascript
// biome-ignore lint/suspicious/noDebugger: debugging production issue
debugger;

// biome-ignore lint/correctness/noUnusedVariables: used in type checking
const _typeCheck: string = "test";
```

### File-Level Suppression

Suppress rules across an entire file:

```javascript
// biome-ignore-all lint/suspicious/noDebugger
// This file has multiple debugger statements for development
```

### Range Suppression

Suppress violations in a specific code block:

```javascript
// biome-ignore-start lint/correctness/noUnusedVariables
const temp1 = data;
const temp2 = data;
const temp3 = data;
// biome-ignore-end
```

The end comment is optional. ([Suppressions][4])

### Editor Code Actions

LSP-compatible editors provide code actions for suppressions:

1. **Inline Suppressions**: `source.suppressRule.inline.biome`
2. **Top-Level Suppressions**: `source.suppressRule.topLevel.biome`

These can be configured in editor settings to show/hide suppression options. ([Suppressions][4])

### Migration Workflow

When migrating from ESLint, suppress all violations initially:

```bash
biome lint --write --unsafe --suppress="suppressed due to migration"
```

This allows incremental fixing of issues over time. ([Suppressions][4])

## Rule Examples

### noUnusedVariables

Identifies and reports variables that are declared but never used. ([Rules Sources][2])

**Category**: `lint/correctness/noUnusedVariables`
**Status**: Recommended
**Severity**: Warning
**Fix**: Unsafe (prepends underscore)

**Invalid**:
```javascript
let a = 4;
a++;  // 'a' is modified but never read
```

**Valid**:
```javascript
let _a = 4;  // Underscore prefix signals intentional non-use
_a++;

function foo(b) {
  console.log(b);  // 'b' is used
}
```

**Configuration**:
```json
{
  "linter": {
    "rules": {
      "correctness": {
        "noUnusedVariables": {
          "level": "error",
          "options": {
            "ignoreRestSiblings": true
          }
        }
      }
    }
  }
}
```

**Options**:
- `ignoreRestSiblings` (default: `true`): Ignores variables captured by object spread patterns

### useStrictMode

Enforces the use of the `"use strict"` directive in script files. ([Rules Sources][2])

**Category**: `lint/suspicious/useStrictMode`
**Status**: Available since v1.8.0
**Severity**: Warning
**Fix**: Safe (inserts `"use strict";`)

**What it does**: Checks that JavaScript script files (CommonJS `.cjs` files and `.js` files configured as CommonJS in `package.json`) include the `"use strict"` directive at the beginning. Strict mode enables safer execution and optimizations.

**Invalid**:
```javascript
var a = 1;
```

**Valid**:
```javascript
"use strict";
var a = 1;
```

**Does not apply to**: ES modules (always in strict mode by default)

**Configuration**:
```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "useStrictMode": "error"
      }
    }
  }
}
```

## Performance Considerations

Scanner functionality—required for project-domain rules like `noUnresolvedImports`—adds processing overhead. For approximately 2,000 files:

- Without Scanner: ~800ms
- With Scanner: ~2 seconds

The file scanner only activates when project-domain rules are enabled, maintaining performance for basic linting. ([Biome Linter][1])

## Editor Integration

### LSP Support

LSP-compatible editors receive:
- Real-time diagnostics
- Code actions for fixes and suppressions
- Apply safe fixes on save

### Fix on Save

Configure safe fixes to apply automatically when saving files using the `source.fixAll.biome` code action:

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.biome": "explicit"
  }
}
```

([Biome Linter][1])

## CLI Usage

### Lint with Fixes

Apply safe fixes automatically:

```bash
biome lint --write ./src
```

Apply unsafe fixes (requires confirmation or `--unsafe` flag):

```bash
biome lint --write --unsafe ./src
```

### Error vs Warning Behavior

By default:
- **Errors**: Halt CLI execution (non-zero exit code)
- **Warnings**: Don't halt execution (zero exit code)

Force warnings to fail builds:

```bash
biome lint --error-on-warnings ./src
```

([Biome Linter][1])

### Controlling Fix Behavior

Override default fix behavior:

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "noUnusedVariables": {
          "fix": "none"
        }
      }
    }
  }
}
```

Fix options: `"none"`, `"safe"`, `"unsafe"` ([Biome Linter][1])

## Best Practices

### Rule Selection Strategy

1. **Start with recommended rules**: Enable `"recommended": true` as baseline
2. **Add project-specific rules**: Enable additional rules based on project needs
3. **Adjust severity levels**: Convert critical rules from warnings to errors
4. **Document suppressions**: Always include reasons when suppressing rules

### Incremental Adoption

For existing codebases:

1. Enable linter with suppressions for all existing violations
2. Fix violations incrementally by category
3. Enable stricter rules for new code via `overrides`
4. Gradually reduce suppressions over time

### Performance Optimization

1. **Limit file scanning**: Use `linter.includes` to target specific directories
2. **Disable unnecessary rules**: Turn off rules not relevant to your stack
3. **Use nursery rules selectively**: Only enable nursery rules you need
4. **Monitor scanner impact**: Be aware of performance cost for project-domain rules

### Team Configuration

1. **Commit biome.json**: Share configuration across team
2. **Document custom rules**: Explain why specific rules are enabled/disabled
3. **Set up CI checks**: Fail builds on linting errors
4. **Configure editor integration**: Ensure consistent developer experience

## Migration from ESLint

### Rule Mapping

Biome provides equivalents for many ESLint rules. Check the [rules sources documentation](https://biomejs.dev/linter/rules-sources/) for specific mappings.

**Common mappings**:
- `no-console` → `noConsole`
- `no-debugger` → `noDebugger`
- `no-unused-vars` → `noUnusedVariables`
- `@typescript-eslint/no-explicit-any` → `noExplicitAny`

([Rules Sources][2])

### Migration Process

1. **Install Biome**: Add to project dependencies
2. **Initial suppression**: Run `biome lint --write --unsafe --suppress="migration"`
3. **Review configuration**: Map ESLint config to Biome equivalents
4. **Test changes**: Verify linting behavior matches expectations
5. **Incremental fixes**: Remove suppressions and fix issues over time

### Missing Rules

Some ESLint rules may not have Biome equivalents. For these cases:

- Check if a similar rule exists with different name
- Consider if the rule is still needed (formatting vs linting)
- Keep ESLint for specific rules if necessary (dual tooling)
- Request new rules via Biome's contribution process

## Troubleshooting

### Rules Not Running

**Check**:
1. Linter is enabled: `"linter.enabled": true`
2. Rule group is not disabled: `"correctness": "on"`
3. File is included in linting scope
4. File is not in `node_modules/`

### Fixes Not Applying

**Verify**:
1. Using `--write` flag for CLI
2. Fix is marked as safe (unsafe fixes require `--unsafe`)
3. Rule has fix capability (not all rules provide fixes)
4. Rule fix is not disabled via `"fix": "none"`

### Performance Issues

**Optimize by**:
1. Limiting `linter.includes` to relevant directories
2. Disabling project-domain rules if not needed
3. Increasing `files.maxSize` if large files are timing out
4. Using `!!pattern` to force-ignore generated directories

## References

[1]: https://biomejs.dev/linter/ "Biome Linter Documentation"
[2]: https://biomejs.dev/linter/rules-sources/ "Biome Rules Sources"
[3]: https://biomejs.dev/reference/configuration/#linter "Biome Linter Configuration"
[4]: https://biomejs.dev/linter/#ignoring-code "Biome Suppressions"
