---
author: unknown
category: meta
contributors: []
description: Standard metadata specification for specification documents (specs)
last_updated: '2025-11-03'
related:
- METADATA-SPEC.md
- ../commands/COMMAND-METADATA-SPEC.md
sources: []
status: stable
subcategory: specifications
tags:
- metadata
- standards
- specs
- documentation
title: Spec Metadata Specification
type: meta
version: '1.0'
---

# Spec Metadata Specification

All specification documents (feature specs, defect specs, chore specs) should include a YAML frontmatter block with metadata to enable search, discovery, and "agentic memory" - allowing agents to learn from past patterns and solutions.

## Purpose

Spec metadata serves as **agentic memory** - a searchable knowledge base of past problems, solutions, and patterns. Agents can search specs to:
- Find similar features or defects that were solved before
- Discover common patterns and anti-patterns
- Learn from implementation approaches
- Identify dependencies and related work

## Metadata Block

```yaml
---
title: "Feature: Workbench Search API"
description: "Brief one-line description of the spec"
type: "feature-spec"
tags: ["tag1", "tag2", "tag3"]
category: "category-name"
subcategory: "subcategory-name"
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "draft"
dependencies: ["path/to/related-spec.md"]
phases: 5
---
```

## Field Definitions

### Base Fields (Inherited from BaseMetadata)

#### title
**Required:** Yes
**Type:** String
**Description:** Short, descriptive title for the spec
**Format:** Should start with spec type prefix: "Feature:", "Defect:", "Chore:"
**Example:** `"Feature: Workbench Search API"`

#### description
**Required:** Yes
**Type:** String
**Description:** Brief one-line description of what this spec covers
**Example:** `"Implement full-text search for workbench files with BM25 ranking"`

#### type
**Required:** Yes
**Type:** String (from allowed values)
**Description:** Type of specification document
**Allowed Values:**
- `feature-spec` - New feature specifications
- `defect-spec` - Bug fix specifications
- `chore-spec` - Maintenance/refactoring specifications
- `spike-spec` - Research/investigation specifications

**Example:** `"feature-spec"`

#### tags
**Required:** Yes
**Type:** Array of strings
**Description:** Keywords for search and categorization (3-10 tags recommended)
**Purpose:** Primary mechanism for search/discovery - be generous with relevant tags
**Example:** `["search", "api", "backend", "frontend", "bm25", "indexing"]`
**Use:** `[]` if no tags applicable (not recommended)

#### category
**Required:** Yes
**Type:** String
**Description:** Primary category for organization
**Examples:** `"workbench"`, `"search"`, `"metadata"`, `"ui"`, `"api"`, `"deployment"`
**Use:** `"general"` if no specific category

#### subcategory
**Required:** Yes
**Type:** String
**Description:** Secondary categorization within category
**Examples:** `"search"`, `"files"`, `"display"`, `"parsing"`
**Use:** `"none"` if no subcategory

#### version
**Required:** Yes
**Type:** String
**Description:** Version of the spec document
**Examples:** `"1.0"`, `"1.1"`, `"2.0"`
**Use:** `"1.0"` for initial version, increment for major changes

#### last_updated
**Required:** Yes
**Type:** String (ISO date format YYYY-MM-DD)
**Description:** Date of last significant update
**Example:** `"2025-11-03"`

#### status
**Required:** Yes
**Type:** String (from allowed values)
**Description:** Current implementation status of the spec
**Allowed Values:**
- `draft` - Spec is being written, not ready for implementation
- `ready` - Spec is complete and ready for implementation
- `in-progress` - Implementation has started but not finished
- `completed` - Implementation is complete and validated
- `archived` - Spec is no longer relevant or was superseded

**Example:** `"completed"`

### Spec-Specific Fields

#### dependencies
**Required:** Yes
**Type:** Array of strings (relative paths to other specs)
**Description:** Other specs that must be completed before or are related to this spec
**Purpose:** Tracks relationships between specs for context and ordering
**Example:** `["workbench-files-api.md", "../references/search/bm25-ranking.md"]`
**Use:** `[]` if no dependencies

#### phases
**Required:** Yes
**Type:** Integer
**Description:** Number of implementation phases in the spec
**Purpose:** Indicates complexity and helps with planning
**Example:** `5` (if spec has 5 phases)
**Use:** `1` if spec is single-phase or not broken into phases

## Complete Examples

### Feature Specification

```yaml
---
title: "Feature: Workbench Search API"
description: "Implement full-text search for workbench files with BM25 ranking"
type: "feature-spec"
tags: ["search", "api", "backend", "frontend", "bm25", "indexing", "workbench"]
category: "workbench"
subcategory: "search"
version: "1.0"
last_updated: "2025-11-03"
status: "completed"
dependencies: ["workbench-files-api.md"]
phases: 5
---

# Feature: Workbench Search API

[Spec content follows...]
```

### Defect Specification

```yaml
---
title: "Defect: Schema Validation Null Size"
description: "Fix null size field failing JSON schema validation in workbench"
type: "defect-spec"
tags: ["bug", "validation", "schema", "workbench", "json-schema"]
category: "workbench"
subcategory: "validation"
version: "1.0"
last_updated: "2025-10-28"
status: "completed"
dependencies: []
phases: 2
---

# Defect: Schema Validation Null Size

[Spec content follows...]
```

### Chore Specification

```yaml
---
title: "Chore: Migrate to Biome from ESLint/Prettier"
description: "Replace ESLint and Prettier with Biome for unified linting and formatting"
type: "chore-spec"
tags: ["tooling", "linting", "formatting", "biome", "eslint", "prettier", "migration"]
category: "tooling"
subcategory: "linting"
version: "1.0"
last_updated: "2025-10-15"
status: "completed"
dependencies: []
phases: 3
---

# Chore: Migrate to Biome

[Spec content follows...]
```

### Spike Specification

```yaml
---
title: "Spike: Evaluate Vector Search for Semantic Code Search"
description: "Research and prototype vector embeddings for semantic code search"
type: "spike-spec"
tags: ["research", "vector-search", "embeddings", "semantic-search", "prototype"]
category: "search"
subcategory: "research"
version: "1.0"
last_updated: "2025-11-01"
status: "in-progress"
dependencies: ["workbench-search-api.md"]
phases: 1
---

# Spike: Vector Search for Semantic Code Search

[Spec content follows...]
```

## Validation Rules

A valid spec metadata block must:
1. Include all required base fields
2. Use allowed values for `type` and `status`
3. Use ISO date format (YYYY-MM-DD) for `last_updated`
4. Have at least one tag (empty array allowed but not recommended)
5. Have `phases` as positive integer (minimum 1)
6. Title should start with type prefix (Feature:, Defect:, Chore:, Spike:)

## Usage

### Finding Specs by Pattern

```bash
# Find all completed feature specs
rg "type: \"feature-spec\"" specs/ | xargs rg "status: \"completed\""

# Find specs about search
rg "tags:.*search" specs/

# Find specs with dependencies
rg "dependencies: \[.+\]" specs/

# Find in-progress specs
rg "status: \"in-progress\"" specs/
```

### Programmatic Access

```python
import yaml
from pathlib import Path

def load_spec_metadata(file_path):
    """Extract metadata from spec file."""
    with open(file_path) as f:
        content = f.read()
        if content.startswith('---'):
            yaml_content = content.split('---')[1]
            return yaml.safe_load(yaml_content)
    return None

# Find all specs by status
specs_by_status = {}
for spec_file in Path('specs').glob('*.md'):
    metadata = load_spec_metadata(spec_file)
    if metadata and metadata.get('type', '').endswith('-spec'):
        status = metadata['status']
        specs_by_status.setdefault(status, []).append({
            'file': str(spec_file),
            'title': metadata['title'],
            'tags': metadata['tags']
        })

# Find specs by tag
def find_specs_by_tag(tag):
    """Find all specs with a specific tag."""
    results = []
    for spec_file in Path('specs').glob('*.md'):
        metadata = load_spec_metadata(spec_file)
        if metadata and tag in metadata.get('tags', []):
            results.append({
                'file': str(spec_file),
                'title': metadata['title'],
                'description': metadata['description']
            })
    return results

# Find specs with dependencies
def find_spec_dependencies(spec_file):
    """Get all dependencies for a spec."""
    metadata = load_spec_metadata(spec_file)
    return metadata.get('dependencies', []) if metadata else []
```

## Migration Guide

### Migrating Existing Specs

Existing specs without metadata will continue to work. To add metadata:

1. **Extract information from spec content:**
   - Title from main heading
   - Description from Feature Description section
   - Tags from technologies/concepts mentioned
   - Status from whether spec is implemented

2. **Add frontmatter block at top of file:**
   ```yaml
   ---
   title: "Feature: [extract from heading]"
   description: "[extract from Feature Description]"
   type: "feature-spec"  # or defect-spec, chore-spec
   tags: [list relevant keywords]
   category: "[main category]"
   subcategory: "[subcategory]"
   version: "1.0"
   last_updated: "YYYY-MM-DD"
   status: "completed"  # or draft, ready, in-progress
   dependencies: []
   phases: [count phases in spec]
   ---
   ```

3. **Validate metadata:**
   - Ensure all required fields present
   - Use allowed values for type and status
   - Use ISO date format
   - Add generous tags for discoverability

### Example Migration

**Before:**
```markdown
# Feature: Workbench Search API

## Feature Description
Implement full-text search for workbench files...

[rest of spec]
```

**After:**
```markdown
---
title: "Feature: Workbench Search API"
description: "Implement full-text search for workbench files with BM25 ranking"
type: "feature-spec"
tags: ["search", "api", "backend", "bm25", "workbench"]
category: "workbench"
subcategory: "search"
version: "1.0"
last_updated: "2025-11-03"
status: "completed"
dependencies: []
phases: 5
---

# Feature: Workbench Search API

## Feature Description
Implement full-text search for workbench files...

[rest of spec]
```

## Best Practices

### Tag Selection
- Include technology tags: `"python"`, `"typescript"`, `"react"`, `"fastapi"`
- Include domain tags: `"search"`, `"metadata"`, `"ui"`, `"api"`, `"parsing"`
- Include pattern tags: `"validation"`, `"indexing"`, `"caching"`, `"testing"`
- Be generous - more tags = better discoverability for agents

### Dependencies
- Link to specs that provide prerequisite functionality
- Link to related references for context
- Use relative paths from specs directory
- Update dependencies when specs change

### Status Tracking
- Start with `"draft"` when writing spec
- Move to `"ready"` when spec is complete and reviewed
- Move to `"in-progress"` when implementation starts
- Move to `"completed"` when implementation is done and validated
- Move to `"archived"` if spec is superseded or no longer relevant

### Agentic Memory Usage
When searching for patterns/solutions:
1. Search by tags: `"Find all specs with tag 'search'"`
2. Search by category: `"Find all workbench specs"`
3. Search by status: `"Find completed specs about validation"`
4. Search by dependencies: `"Find specs that depend on workbench-files-api"`

This enables agents to learn from past work and avoid reinventing solutions.