---
title: "Update Spec Metadata"
description: "Deeply analyze spec files and generate high-quality metadata through comprehensive spec comprehension and codebase analysis"
type: "command"
tags: ["metadata", "specs", "analysis", "memory", "documentation", "knowledge-base"]
category: "documentation"
subcategory: "maintenance"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion"]
requires_args: true
argument_hint: "[spec-file-path-or-directory]"
usage_examples:
  - "/update-spec-metadata specs/metadata-card-ui.md"
  - "/update-spec-metadata specs/"
  - "/update-spec-metadata specs/workbench-search-api/"
---

# Update Spec Metadata

Analyze specification files through deep comprehension and codebase analysis to generate high-quality metadata that serves as **agentic memory** - enabling future agents to learn from past patterns, solutions, and implementations.

## Core Principle

This is NOT an autopilot data extraction task. This is about **understanding** each spec deeply and creating metadata that captures:
- What problem was solved and why it mattered
- How it was implemented (patterns, approaches, architecture)
- What it depended on and what it enabled
- Technical details AND conceptual patterns

Future agents should be able to search this metadata and learn: "Show me how similar problems were solved before."

## Instructions

### 1. Determine Scope

Parse `$ARGUMENTS` to determine processing mode:
- **Single file**: If argument is a `.md` file path
- **Batch directory**: If argument is a directory
- **Default**: If empty, use `specs/` directory

### 2. For Each Spec - Deep Comprehension Phase

**Read the entire spec carefully.** Understand:

#### A. Problem & Context
- What problem or need did this spec address?
- What was the motivation or business value?
- What constraints or requirements existed?

#### B. Solution & Approach
- How was the problem solved?
- What architectural patterns or design decisions were made?
- What technologies or libraries were chosen and why?

#### C. Implementation Scope
- What was actually built?
- What files/modules/components were created or modified?
- How does it fit into the larger system?

#### D. Dependencies & Relationships
- What other specs or systems did this depend on?
- What prerequisites were needed?
- What did this enable for future work?

**Think about**: What would a future agent want to know when searching for similar patterns?

### 3. Codebase Analysis Phase

**Understand the actual implementation** (not just check if files exist):

#### A. Find Implementation Files
Search the codebase for files related to this spec:
- Parse "Relevant Files" sections from spec
- Search for component/module names mentioned in spec
- Look for test files related to implementation
- Check both backend (`app/py/`) and frontend (`app/ts/`) codebases

#### B. Analyze Implementation Patterns
For key implementation files, understand:
- **Architecture**: How was this organized? (e.g., service layer, component hierarchy)
- **Patterns used**: What design patterns or approaches? (e.g., hooks, context, state machines)
- **Integration points**: How does it connect to other systems?

Use `Read` tool to examine key files when needed to understand patterns.

#### C. Analyze Dependencies & Relationships
- What specs or modules does this build upon?
- Search for imports, references, or explicit dependencies in code
- Look for related spec files mentioned in content
- Check git history if needed: `git log --oneline --all -- <file-paths>`

#### D. Determine Implementation Status
Based on comprehensive analysis:
- **completed**: All described functionality implemented, tests exist, validated
- **in-progress**: Partially implemented, some files missing
- **ready**: Spec is complete but not yet implemented
- **draft**: Spec is incomplete
- **archived**: Superseded or no longer relevant

Consider:
- Do the referenced files exist?
- Are there corresponding test files?
- Is this in the `archive/` directory?
- Does git history show recent completion?

Get last update date:
```bash
git log -1 --format="%cd" --date=short -- <spec-file>
```

### 4. Metadata Generation Phase

Now synthesize your understanding into high-quality metadata:

#### A. Title
- Extract from main heading or generate from filename
- Ensure proper prefix: "Feature:", "Defect:", "Chore:", "Spike:"
- Make it clear and descriptive

**Example**: "Feature: Metadata Card UI for Workbench File Viewer"

#### B. Description (Agent-Written)
**Write a clear, informative 1-2 sentence description** that captures:
- The essence of what this spec accomplished
- The value or impact it provided
- Enough detail for future searches

**Don't** just extract the first paragraph. **Do** comprehend and synthesize.

**Good example**: "Implement full-text search for workbench files using BM25 ranking algorithm with FastAPI backend and React frontend integration"

**Bad example**: "This spec describes the search feature" (too vague)

#### C. Type
Determine from content and naming:
- **feature-spec**: New functionality or capability
- **defect-spec**: Bug fix or issue resolution
- **chore-spec**: Refactoring, tooling, maintenance
- **spike-spec**: Research or proof-of-concept

Hints: filename prefix ("defect-", "chore-"), content analysis

#### D. Tags (Semantic Analysis)
Generate 5-10 tags combining:

**Technical keywords** (search for mentions):
- Technologies: "react", "fastapi", "typescript", "python", "docker"
- Libraries: "material-ui", "tanstack-router", "pydantic"
- Tools: "pytest", "vitest", "playwright"

**Domain concepts** (from understanding):
- "search", "metadata", "validation", "parsing", "rendering"
- "workbench", "api", "ui", "backend", "frontend"

**Patterns and approaches** (from analysis):
- "indexing", "caching", "state-management", "testing"
- "integration", "migration", "optimization"

**Conceptual patterns** (think about):
- What category of problem is this? (e.g., "data-transformation", "user-interaction")
- What patterns were used? (e.g., "bm25-ranking", "component-library")

Be generous with tags - more = better discoverability.

#### E. Category & Subcategory
Determine from file path and domain:
- Path `specs/workbench-search-api/` → category: "workbench", subcategory: "search"
- Path `specs/metadata-card-ui.md` → category: "workbench", subcategory: "display"

Use semantic understanding to choose appropriate categories.

#### F. Dependencies
List relative paths to other specs this depends on or relates to:
- Specs mentioned in "Dependencies:" sections
- Specs mentioned in "Prerequisites:" sections
- Related specs found during analysis

**Example**: `["workbench-files-api/00-index.md", "../references/METADATA-SPEC.md"]`

#### G. Phases
Count implementation phases:
- Count numbered phase files in directory: `01-*.md`, `02-*.md`, etc.
- OR parse "Phase" sections from spec content
- Use `1` if single-phase or not phased

#### H. Version & Status
- **version**: Use "1.0" for initial metadata, increment for major spec revisions
- **status**: From your analysis in step 3D
- **last_updated**: From git log

### 5. Quality Check & User Confirmation

Before updating, confirm ambiguous decisions with user:

**Present your analysis**:
```
Analyzed: specs/metadata-card-ui.md

Understanding:
- Problem: Raw YAML display was not user-friendly for metadata viewing
- Solution: Built Material-UI card component with formatted display
- Implementation: React component with 3 phases (foundation, features, polish)
- Pattern: Presentational component with props-based configuration

Generated Metadata:
- Type: feature-spec
- Status: completed (8/8 implementation files exist, tests present)
- Title: "Feature: Metadata Card UI for Workbench File Viewer"
- Description: "Replace raw YAML rendering with polished Material-UI card component for displaying file metadata in workbench"
- Tags: [ui, metadata, react, material-ui, frontend, workbench, display, component]
- Category: workbench, Subcategory: display
- Dependencies: 2 found
- Phases: 3
```

**Ask user to confirm**:
- Does the description accurately capture the spec's essence?
- Are type and status correct?
- Any tags to add/remove?

### 6. Update Metadata Intelligently

#### If NO existing metadata:
Add complete frontmatter block following SPEC-METADATA-SPEC.md format:

```yaml
---
title: "Feature: Spec Title"
description: "Clear, informative description of what this accomplished"
type: "feature-spec"
tags: ["tag1", "tag2", "tag3", "tag4", "tag5"]
category: "category-name"
subcategory: "subcategory-name"
version: "1.0"
last_updated: "2025-11-03"
status: "completed"
dependencies: ["path/to/related-spec.md"]
phases: 3
---
```

#### If existing metadata EXISTS:
**Be thoughtful about changes**:
- **Preserve** well-formed existing values (especially user-curated descriptions)
- **Update** if clearly outdated or incorrect:
  - `last_updated` if git shows newer date
  - `tags` - merge: add missing relevant tags, keep existing good ones
  - `dependencies` if new relationships discovered
  - `phases` if count changed
- **Add** missing required fields
- **Don't change** without good reason

Use judgment: only update when you have genuine improvements.

### 7. Validate & Report

Run the validation script to check metadata quality:

```bash
./scripts/validate-spec-metadata.py
```

The script validates against SPEC-METADATA-SPEC.md:
- All required fields present
- Correct format (ISO date YYYY-MM-DD for last_updated)
- Allowed values for type and status
- Dependencies are valid relative paths
- Phases is positive integer (≥1)
- Title prefix matches spec type
- Tag count and quality

**If validation passes** (exit code 0):
- ✅ Metadata is valid and complete

**If validation fails** (exit code 1):
- Review errors and warnings
- Fix any validation issues
- Re-run validation script
- Only proceed when all checks pass

Report results:
```
✓ Updated: specs/metadata-card-ui.md
  Status: completed (comprehensive implementation verified)
  Description: Replace raw YAML rendering with polished Material-UI card component
  Tags: 23 generated (ui, metadata, react, material-ui, frontend, workbench, display, component, ...)
  Dependencies: 1 identified
  Phases: 3 detected
  Pattern: Presentational React component with props-based configuration

✓ Validation: PASSED (all required fields present, valid values)
```

## Batch Processing

When processing multiple specs:
1. Analyze each spec thoroughly (don't rush)
2. Consider relationships between specs as you process them
3. Prompt for confirmation on each spec before updating
4. Report summary at end

## Key Principles

1. **Understand deeply** - Read and comprehend the entire spec, don't just extract data
2. **Write thoughtfully** - Descriptions should be clear and informative for future searches
3. **Analyze comprehensively** - Understand implementation patterns, not just file existence
4. **Think semantically** - Tags should capture both technical details and conceptual patterns
5. **Build memory** - Metadata should help future agents learn from past work
6. **Be conservative** - Don't change good existing metadata without reason

## Arguments

`$ARGUMENTS` accepts:
- Single file: `specs/metadata-card-ui.md`
- Directory: `specs/` or `specs/workbench-search-api/`
- Empty: defaults to `specs/` directory
