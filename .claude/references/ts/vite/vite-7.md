---
title: "Vite 7 Tool Reference"
description: "Vite 7 build tool features, Environment API, Rolldown integration, and migration guide"
type: "tool-reference"
tags: ["vite", "build-tool", "frontend", "bundler", "rollup", "rolldown", "hmr", "esm"]
category: "frontend"
subcategory: "build-tools"
version: "7.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Vite 7.0 Announcement"
    url: "https://vite.dev/blog/announcing-vite7"
  - name: "Vite 7 Migration Guide"
    url: "https://vite.dev/guide/migration"
  - name: "Vite Environment API"
    url: "https://vite.dev/guide/api-environment"
  - name: "Vite Guide"
    url: "https://vite.dev/guide"
related: ["../react/react-19.md"]
author: "unknown"
contributors: []
---

# Vite 7 Tool Reference

Vite 7.0 is a modern build tool that provides a faster and leaner development experience for modern web projects. ([Vite Guide][4]) Released on June 24, 2025, Vite 7 marks a significant milestone five years after the project's inception, with 31 million weekly downloads. ([Vite 7.0 Announcement][1])

## What Is Vite?

Vite (French for "quick", pronounced `/vit/`) combines two major components: ([Vite Guide][4])

1. **Development Server** - Features extremely fast Hot Module Replacement (HMR) built on native ES modules
2. **Production Build** - Bundles code using Rollup to generate highly optimized static assets

The platform is framework-agnostic, supporting Vue, React, Preact, Lit, Svelte, Solid, Qwik, and vanilla JavaScript projects. ([Vite Guide][4])

## Release Overview

### Timeline and Adoption

Vite 7.0 was released on June 24, 2025, representing five years of development since the project's inception. ([Vite 7.0 Announcement][1]) Weekly downloads increased from 17 million to 31 million over seven months, demonstrating rapid ecosystem growth. ([Vite 7.0 Announcement][1])

### Node.js Requirements

Vite 7 dropped support for Node.js 18 (which reached EOL in April 2025) and now requires Node.js 20.19+ or 22.12+. ([Vite 7.0 Announcement][1]) ([Vite 7 Migration Guide][2]) This enables ESM-only distribution while maintaining compatibility with CommonJS modules through `require(esm)` support. ([Vite 7.0 Announcement][1])

## Major Features and Changes

### Browser Target Updates

The default browser targeting shifted from `'modules'` to `'baseline-widely-available'`, aligning with established web platform features available across browsers for 30+ months. ([Vite 7.0 Announcement][1])

**Updated minimum browser versions:** ([Vite 7 Migration Guide][2])
- Chrome: 87 → 107
- Edge: 88 → 107
- Firefox: 78 → 104
- Safari: 14.0 → 16.0

Production builds target browsers from the past 2.5+ years by default, with legacy browser support available through the official `@vitejs/plugin-legacy`. ([Vite Guide][4])

### Environment API

The experimental Environment API from Vite 6 remains under active development. ([Vite 7.0 Announcement][1]) This API formalizes the concept of "environments"—distinct execution contexts where application code runs. ([Vite Environment API][3])

#### Core Concepts

Vite 6 introduced the ability to "configure their app during build and dev to map all of its environments," enabling support for browser, server, and edge runtimes in a single project. ([Vite Environment API][3]) Previously, Vite implicitly supported only `client` and optional `ssr` environments. ([Vite Environment API][3])

The API enables apps to run code across multiple runtimes concurrently during development, with each environment having independent configuration while sharing Vite's HTTP server, middleware, and plugin pipeline. ([Vite Environment API][3])

#### Configuration

**Simple Apps (SPA/MPA)**
Existing configurations require no changes. Top-level options automatically apply to the default `client` environment for backward compatibility. ([Vite Environment API][3])

**Multi-Environment Setup** ([Vite Environment API][3])
```javascript
// vite.config.js
export default {
  environments: {
    server: {},
    edge: {
      resolve: { noExternal: true }
    }
  }
}
```

Environments inherit parent-level options unless explicitly overridden. ([Vite Environment API][3]) The `client` environment should be configured via top-level options rather than `environments.client` to maintain clarity. ([Vite Environment API][3])

#### buildApp Hook

Vite 7 introduces a new `buildApp` hook enabling plugin coordination during environment building. ([Vite 7.0 Announcement][1]) This allows plugins to orchestrate complex build processes across multiple environments.

```javascript
// Plugin example with buildApp hook
export default function myPlugin() {
  return {
    name: 'my-plugin',
    buildApp: async (builder) => {
      // Coordinate builds across environments
      await builder.build('client');
      await builder.build('server');

      // Perform post-build coordination
      await generateManifest();
    }
  }
}
```

#### Ecosystem Adoption

The ecosystem continues testing Environment APIs with positive adoption examples like Cloudflare's updated Vite plugin supporting React Router v7. ([Vite 7.0 Announcement][1])

### Rolldown Integration

Users can test Rolldown, a Rust-based next-generation bundler, via the `rolldown-vite` package as a drop-in replacement. ([Vite 7.0 Announcement][1]) This should reduce build times for larger projects before Rolldown becomes the default bundler. ([Vite 7.0 Announcement][1])

#### Installation and Setup

```bash
npm install -D rolldown-vite
```

```javascript
// vite.config.js
import { defineConfig } from 'rolldown-vite';

export default defineConfig({
  // Your existing Vite config
});
```

The package provides a compatible API surface, allowing seamless testing without configuration changes.

## Breaking Changes and Deprecations

### Removed Features

**Sass Legacy API Support** ([Vite 7 Migration Guide][2])
Modern Sass API is now mandatory. Remove any `css.preprocessorOptions.sass.api` or `scss.api` configurations.

```javascript
// Remove this configuration
export default {
  css: {
    preprocessorOptions: {
      sass: { api: 'legacy' }, // No longer supported
      scss: { api: 'legacy' }  // No longer supported
    }
  }
}
```

**splitVendorChunkPlugin** ([Vite 7 Migration Guide][2])
Removed; use `build.rollupOptions.output.manualChunks` instead.

```javascript
// Old approach (removed)
import { splitVendorChunkPlugin } from 'vite';

export default {
  plugins: [splitVendorChunkPlugin()]
}

// New approach
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  }
}
```

### Deprecated Plugin Hooks

**transformIndexHtml** hook-level properties replaced: ([Vite 7 Migration Guide][2])
- `enforce` property → `order` property
- `transform` property → `handler` property

```javascript
// Old approach (deprecated)
export default {
  name: 'my-plugin',
  transformIndexHtml: {
    enforce: 'pre',
    transform(html, ctx) {
      return html.replace('<!--inject-->', '<script>...</script>');
    }
  }
}

// New approach
export default {
  name: 'my-plugin',
  transformIndexHtml: {
    order: 'pre',
    handler(html, ctx) {
      return html.replace('<!--inject-->', '<script>...</script>');
    }
  }
}
```

### Advanced Breaking Changes

Several rarely-used APIs were eliminated: ([Vite 7 Migration Guide][2])
- `legacy.proxySsrExternalModules` (non-functional since v6)
- Unused type properties from ModuleRunner, ViteDevServer, and ResolvePlugin options
- Deprecated HMR Broadcaster-related types
- CSS preprocessor peer dependency version ranges now specified

## Core Capabilities

### Framework Support

Vite is framework-agnostic and supports: ([Vite Guide][4])
- Vue
- React
- Preact
- Lit
- Svelte
- Solid
- Qwik
- Vanilla JavaScript

### Development Features

**Fast Hot Module Replacement**
Extremely fast HMR built on native ES modules. ([Vite Guide][4])

**Dependency Pre-bundling**
Optimizes module resolution for faster development. ([Vite Guide][4])

**Multi-page App Support**
Handles applications with multiple HTML entry points. ([Vite Guide][4])

**Environment Variables**
Built-in support for environment-based configuration. ([Vite Guide][4])

### Extensibility

**Plugin API**
Comprehensive Plugin API with full typing support. ([Vite Guide][4])

**JavaScript API**
Full programmatic access to Vite's functionality. ([Vite Guide][4])

## Migration Guide

### From Vite 6 to Vite 7

Users should first consult the Vite v6 migration guide, then apply these v7-specific changes. ([Vite 7 Migration Guide][2])

#### Step 1: Update Node.js

Ensure Node.js 20.19+ or 22.12+ is installed: ([Vite 7 Migration Guide][2])

```bash
node --version
# Should output v20.19.0 or higher, or v22.12.0 or higher
```

#### Step 2: Update Dependencies

```bash
npm install vite@7 --save-dev
```

#### Step 3: Remove Deprecated Configurations

1. **Remove Sass Legacy API configuration**

```javascript
// Remove these from vite.config.js
export default {
  css: {
    preprocessorOptions: {
      sass: { api: 'legacy' },
      scss: { api: 'legacy' }
    }
  }
}
```

2. **Replace splitVendorChunkPlugin**

```javascript
// Before
import { splitVendorChunkPlugin } from 'vite';
export default {
  plugins: [splitVendorChunkPlugin()]
}

// After
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        }
      }
    }
  }
}
```

3. **Update transformIndexHtml hooks**

```javascript
// Before
transformIndexHtml: {
  enforce: 'pre',
  transform(html) { return html; }
}

// After
transformIndexHtml: {
  order: 'pre',
  handler(html) { return html; }
}
```

#### Step 4: Update Browser Targets (Optional)

If you rely on specific browser support, review the new default targets and adjust if needed:

```javascript
// vite.config.js
export default {
  build: {
    target: 'es2020' // Override default if needed
  }
}
```

#### Step 5: Test Thoroughly

Run your development server and production builds to ensure compatibility:

```bash
npm run dev
npm run build
npm run preview
```

## Ecosystem Initiatives

### ViteConf 2025

ViteConf 2025 will occur in-person in Amsterdam (October 9-10), representing the first physical gathering after three online editions. ([Vite 7.0 Announcement][1])

### Vite DevTools

VoidZero and NuxtLabs are collaborating on Vite DevTools for enhanced debugging and analysis across Vite-based projects. ([Vite 7.0 Announcement][1])

## Getting Started

### Project Scaffolding

Create a new Vite project: ([Vite Guide][4])

```bash
npm create vite@latest
```

The command provides templates for multiple frameworks.

### Online Testing

Test Vite online through StackBlitz without local installation. ([Vite Guide][4])

### Basic Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});
```

## Best Practices

### Environment API Usage

1. **Keep client configuration at top level**: Maintain clarity by configuring the client environment via top-level options ([Vite Environment API][3])
2. **Use explicit environment configuration only when needed**: Avoid unnecessary complexity
3. **Leverage runtime providers' custom implementations**: Use specialized environments for edge and server runtimes
4. **Test multi-environment setups**: Ensure proper isolation between environments

### Build Optimization

1. **Use manual chunks for code splitting**: Replace deprecated `splitVendorChunkPlugin` with granular control
2. **Test Rolldown for large projects**: Evaluate build time improvements with the Rust-based bundler
3. **Configure browser targets appropriately**: Balance modern features with user browser support
4. **Enable source maps in production**: Aid debugging while accepting slight size increase

### Development Workflow

1. **Leverage HMR effectively**: Take advantage of fast module replacement for rapid iteration
2. **Pre-bundle dependencies**: Let Vite optimize third-party dependencies automatically
3. **Use environment variables**: Configure different behavior for dev/staging/prod
4. **Monitor plugin performance**: Ensure plugins don't significantly impact build times

### Migration Strategy

1. **Update Node.js first**: Ensure runtime compatibility before updating Vite
2. **Review breaking changes**: Check the migration guide for API changes
3. **Test incrementally**: Validate development and production builds separately
4. **Monitor bundle size**: Ensure new browser targets don't unexpectedly increase bundle size
5. **Update CI/CD pipelines**: Ensure build environments use compatible Node.js versions

## Configuration Reference

### Environment Options

Environment-specific options extend `EnvironmentOptions`, which includes: ([Vite Environment API][3])
- `resolve` - Module resolution configuration
- `define` - Global constant replacements
- `optimizeDeps` - Dependency optimization (dev only)

Some options apply only to development; others support both build and dev phases through `DevEnvironmentOptions` and `BuildEnvironmentOptions`. ([Vite Environment API][3])

### Backward Compatibility

Vite 6 maintains full backward compatibility with Vite 5. The deprecated `ssr` top-level property still functions identically to `environments.ssr`. ([Vite Environment API][3])

## Troubleshooting

### Node.js Version Errors

**Error**: "Vite requires Node.js version 20.19+ or 22.12+"

**Solution**: Update Node.js to a compatible version:
```bash
# Using nvm
nvm install 20.19
nvm use 20.19

# Or using n
n 20.19
```

### Sass API Errors

**Error**: "Sass legacy API is no longer supported"

**Solution**: Remove `api: 'legacy'` from Sass preprocessor options:
```javascript
// vite.config.js
export default {
  css: {
    preprocessorOptions: {
      sass: {
        // Remove: api: 'legacy'
      }
    }
  }
}
```

### Plugin Hook Warnings

**Warning**: "transformIndexHtml 'enforce' property is deprecated"

**Solution**: Rename `enforce` to `order` and `transform` to `handler`:
```javascript
transformIndexHtml: {
  order: 'pre',  // was: enforce
  handler(html) { return html; }  // was: transform
}
```

### Build Target Issues

**Issue**: Build fails in older browsers

**Solution**: Configure custom browser targets:
```javascript
// vite.config.js
export default {
  build: {
    target: ['es2020', 'chrome87', 'safari14']
  }
}
```

## Performance Considerations

### Build Times

Vite 7 with Rolldown should reduce build times for larger projects. ([Vite 7.0 Announcement][1]) Test the `rolldown-vite` package to evaluate improvements for your specific project.

### Development Server

Development assumes modern browser features, enabling extremely fast HMR. ([Vite Guide][4]) This keeps the development cycle tight even for large applications.

### Production Bundles

Rollup-based production builds generate highly optimized static assets. ([Vite Guide][4]) The updated browser targets reduce polyfill overhead while maintaining broad compatibility.

## Future Roadmap

### Rolldown as Default

Rolldown is currently available as an opt-in package but is expected to become the default bundler in a future release, bringing significant performance improvements to all users.

### Environment API Stabilization

The Environment API remains experimental but is seeing positive ecosystem adoption. Expect stabilization and enhanced documentation in upcoming releases.

### DevTools Integration

The collaborative Vite DevTools project will provide enhanced debugging and analysis capabilities across the entire Vite ecosystem.

## References

[1]: https://vite.dev/blog/announcing-vite7 "Vite 7.0 Announcement"
[2]: https://vite.dev/guide/migration "Vite 7 Migration Guide"
[3]: https://vite.dev/guide/api-environment "Vite Environment API"
[4]: https://vite.dev/guide "Vite Guide"
