---
title: "Create Reference Documentation"
description: "Research a topic and create comprehensive reference documentation with proper metadata"
type: "command"
tags: ["documentation", "research", "metadata", "references", "web", "creation"]
category: "documentation"
subcategory: "creation"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed-tools: Bash, Read, WebFetch, Write, Glob, Grep, Task
requires_args: true
argument_hint: "[topic-name] [optional-urls]"
usage_examples:
  - "/create-reference OpenTelemetry Collector configuration"
  - "/create-reference Kubernetes operators https://kubernetes.io/docs/concepts/"
  - "/create-reference TanStack Router concepts"
---

# Create Reference Documentation

This command helps you research a topic and create comprehensive reference documentation following the project's metadata specification.

## Context Loading

First, understand the existing reference structure and standards:

### Review Templates and Specifications
- Read `.claude/references/METADATA-SPEC.md` to understand required metadata fields
- Read `.claude/references/REFERENCE-TEMPLATE.md` for reference document structure
- Read `.claude/references/README-TEMPLATE.md` for index/README structure

### Check Existing References
- Run `git ls-files .claude/references/` to see existing reference files
- If updating an existing topic, read the current reference file(s)

## Research Phase

### Arguments
$ARGUMENTS should contain:
- Topic name or subject to research (required)
- Optional: Specific documentation URLs to fetch
- Optional: Local file paths to review
- Optional: Category/subcategory hints

### Research Steps

1. **Web Research** (for new topics or updates):
   - Use WebFetch to gather information from official documentation
   - Fetch multiple sources (official docs, GitHub repos, specifications)
   - Extract key concepts, configuration options, examples, and best practices
   - **Use inline reference links heavily** - format: `([Source Name][N])`
   - Collect all URLs for the references section at the bottom

2. **Local Context** (if extending existing references):
   - Read related reference files in `.claude/references/`
   - Check for cross-references and related topics
   - Identify gaps or areas needing expansion

3. **Source Verification**:
   - Prefer official documentation over third-party sources
   - Note version numbers and publication dates
   - Verify claims across multiple sources when possible

## Document Creation

### Metadata Requirements

Every reference document MUST include complete YAML frontmatter with all 13 fields:

```yaml
---
title: "Descriptive Title"
description: "One-line description (50-100 chars)"
type: "appropriate-type"  # See allowed values below
tags: ["tag1", "tag2", "tag3", ...]  # 3-10 relevant tags
category: "primary-category"
subcategory: "secondary-category"  # or "none"
version: "1.0"  # document or subject version
last_updated: "YYYY-MM-DD"  # ISO format
status: "draft|review|stable|deprecated|archived"
sources:
  - name: "Source Name"
    url: "https://example.com/docs"
  # Add more sources as needed
related: ["path/to/related.md"]  # or []
author: "unknown"  # or actual author
contributors: []  # or ["Name1", "Name2"]
---
```

### Allowed Type Values
- `model-spec` - LLM/ML model specifications
- `api-reference` - API documentation and endpoints
- `config-reference` - Configuration options and settings
- `deployment-guide` - Deployment patterns and setups
- `standard-spec` - Standards and specifications
- `concept-guide` - Conceptual explanations
- `pattern-reference` - Design patterns and practices
- `tool-reference` - Tool usage and configuration
- `framework-guide` - Framework-specific guidance
- `integration-guide` - Integration instructions
- `meta` - Meta documentation (indexes, templates, guides)

### Allowed Status Values
- `draft` - Work in progress, incomplete
- `review` - Ready for review
- `stable` - Tested and ready for use
- `deprecated` - No longer recommended
- `archived` - Historical reference only

### Content Structure

Organize content to fit the material, not force material into a fixed structure. Generally:

1. **Overview/Summary** - Brief introduction to the topic
2. **Core Concepts** - Main ideas, architecture, components
3. **Configuration/Setup** - How to configure or deploy
4. **Usage Examples** - Practical examples with code snippets
5. **Best Practices** - Recommendations and patterns
6. **Troubleshooting** - Common issues and solutions (if applicable)
7. **References** - Inline citations collected at bottom

### Inline Reference Style

**IMPORTANT**: Use inline references heavily throughout the document to enable human review and verification:

- Format: `Key information from the docs. ([Source Name][1])`
- Place citation immediately after the claim or information
- Number references sequentially: `[1]`, `[2]`, `[3]`, etc.
- Define all references at the end of the document:

```markdown
[1]: https://example.com/docs "Page Title"
[2]: https://github.com/org/repo "Repository Name"
```

**Example**:
```markdown
Phoenix exposes three ports by default: 6006 for HTTP, 4317 for gRPC, and 9090 for Prometheus metrics. ([Phoenix Docker Docs][1])

The default admin credentials are `admin@localhost` with password `admin`. ([Phoenix Auth Guide][2])

[1]: https://hub.docker.com/r/arizephoenix/phoenix "Phoenix Docker Hub"
[2]: https://arize.com/docs/phoenix/authentication "Phoenix Authentication"
```

## File Placement

Determine the appropriate location:
- New category: `.claude/references/category-name/topic.md`
- Existing category: `.claude/references/existing-category/topic.md`
- Create a category README if starting a new category

## Quality Checklist

Before finalizing, verify:

- [ ] All 13 metadata fields present and valid
- [ ] `type` matches one of the allowed values
- [ ] `status` matches one of the allowed values
- [ ] `last_updated` in ISO format (YYYY-MM-DD)
- [ ] Tags are relevant and specific (3-10 tags)
- [ ] Sources include both `name` and `url`
- [ ] Inline references used throughout content
- [ ] All inline reference numbers defined at bottom
- [ ] Related references updated (bidirectional linking)
- [ ] Content is accurate and verified against sources
- [ ] Examples are clear and practical
- [ ] No sensitive information included

## Report

After completing research and document creation, provide:

### 1. Summary
- Topic overview and what the reference covers
- Document type and category
- Key sections included

### 2. Sources Used
- List all sources fetched and reviewed
- Note official vs. community sources
- Highlight any version-specific information

### 3. File(s) Created/Updated
- File paths and line counts
- Related files that were cross-referenced
- Any index files that need updating

### 4. Metadata Details
- Type, category, subcategory chosen
- Tags selected and rationale
- Version and status assigned

### 5. Review Notes
- Any areas needing further research
- Conflicting information found
- Suggestions for related references to create

## Examples

### Creating a new reference:
```
/create-reference OpenTelemetry Collector configuration
```

### Updating with specific sources:
```
/create-reference Kubernetes operators https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
```

### Extending existing reference:
```
/create-reference .claude/references/arize/tracing-links.md - add LangChain integration details
``` 
