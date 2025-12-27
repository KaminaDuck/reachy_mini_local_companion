---
author: unknown
category: meta
contributors: []
description: Standard metadata specification for all reference documents
last_updated: '2025-01-15'
related:
- README.md
- REFERENCE-TEMPLATE.md
sources: []
status: stable
subcategory: none
tags:
- metadata
- standards
- documentation
title: Reference Metadata Specification
type: meta
version: '1.0'
---

# Reference Metadata Specification

All reference documents must include a YAML frontmatter block with all specified metadata fields.

## Metadata Block

```yaml
---
title: "Short Title"
description: "Brief one-line description"
type: "reference-type"
tags: ["tag1", "tag2", "tag3"]
category: "category-name"
subcategory: "subcategory-name"
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "stable"
sources:
  - name: "Source Name"
    url: "https://example.com"
related: ["path/to/related.md"]
author: "Author Name"
contributors: ["Name1", "Name2"]
---
```

## Field Definitions

### title
**Required:** Yes
**Type:** String
**Description:** Short, descriptive title for the reference
**Example:** `"GPT-OSS 120B Model Reference"`

### description
**Required:** Yes
**Type:** String
**Description:** Brief one-line description of what this reference covers
**Example:** `"Open-weight 120B MoE reasoning LLM deployment reference"`

### type
**Required:** Yes
**Type:** String (from allowed values)
**Description:** Category of reference document
**Allowed Values:**
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
- `meta` - Meta documentation (this file, templates, guides)

**Example:** `"model-spec"`

### tags
**Required:** Yes
**Type:** Array of strings
**Description:** Keywords for search and categorization (3-10 tags recommended)
**Example:** `["llm", "moe", "vllm", "inference", "gpu"]`
**Use:** `[]` if no tags applicable

### category
**Required:** Yes
**Type:** String
**Description:** Primary category for organization
**Examples:** `"ai-models"`, `"deployment"`, `"standards"`, `"frontend"`, `"observability"`
**Use:** `"general"` if no specific category

### subcategory
**Required:** Yes
**Type:** String
**Description:** Secondary categorization within category
**Examples:** `"inference"`, `"docker"`, `"sbom"`, `"routing"`
**Use:** `"none"` if no subcategory

### version
**Required:** Yes
**Type:** String
**Description:** Version of the reference document or subject matter
**Examples:** `"1.0"`, `"1.7"`, `"4.0.0"`
**Use:** `"1.0"` for initial version, increment as content evolves

### last_updated
**Required:** Yes
**Type:** String (ISO date format YYYY-MM-DD)
**Description:** Date of last significant update
**Example:** `"2025-01-15"`

### status
**Required:** Yes
**Type:** String (from allowed values)
**Description:** Current state of the reference
**Allowed Values:**
- `draft` - Work in progress, incomplete
- `review` - Ready for review
- `stable` - Tested and ready for use
- `deprecated` - No longer recommended
- `archived` - Historical reference only

**Example:** `"stable"`

### sources
**Required:** Yes
**Type:** Array of objects with `name` and `url` keys
**Description:** Attribution for where information came from
**Example:**
```yaml
sources:
  - name: "OpenAI Documentation"
    url: "https://openai.com/gpt-oss"
  - name: "vLLM Blog"
    url: "https://blog.vllm.ai/2025/08/05/gpt-oss.html"
```
**Use:** `[]` if no external sources

### related
**Required:** Yes
**Type:** Array of strings (relative paths)
**Description:** Related reference documents
**Example:** `["models/gpt_oss_20b.md", "deployment/vllm-setup.md"]`
**Use:** `[]` if no related references

### author
**Required:** Yes
**Type:** String
**Description:** Primary author or team
**Example:** `"AI Engineering Team"`
**Use:** `"unknown"` if not tracked

### contributors
**Required:** Yes
**Type:** Array of strings
**Description:** Additional contributors
**Example:** `["Alice Smith", "Bob Jones"]`
**Use:** `[]` if no contributors

## Complete Examples

### Model Specification

```yaml
---
title: "GPT-OSS 120B Reference"
description: "Open-weight 120B MoE reasoning LLM deployment reference"
type: "model-spec"
tags: ["llm", "moe", "vllm", "inference", "gpu", "openai"]
category: "ai-models"
subcategory: "inference"
version: "1.0"
last_updated: "2025-01-15"
status: "stable"
sources:
  - name: "OpenAI Docs"
    url: "https://openai.com/gpt-oss"
  - name: "vLLM Documentation"
    url: "https://blog.vllm.ai"
related: ["models/gpt_oss_20b.md"]
author: "AI Team"
contributors: []
---
```

### Standard Specification

```yaml
---
title: "CycloneDX 1.7"
description: "CycloneDX 1.7 SBOM standard specification and migration guide"
type: "standard-spec"
tags: ["sbom", "security", "supply-chain", "compliance", "cyclonedx"]
category: "standards"
subcategory: "sbom"
version: "1.7"
last_updated: "2025-10-21"
status: "stable"
sources:
  - name: "CycloneDX.org"
    url: "https://cyclonedx.org"
related: []
author: "Security Team"
contributors: ["Jane Doe"]
---
```

### Deployment Guide

```yaml
---
title: "Phoenix Docker Compose Deployment"
description: "Production-ready Phoenix deployment with Docker Compose"
type: "deployment-guide"
tags: ["docker", "postgres", "observability", "phoenix", "deployment"]
category: "deployment"
subcategory: "docker"
version: "1.0"
last_updated: "2025-01-15"
status: "stable"
sources:
  - name: "Phoenix Documentation"
    url: "https://arize.com/docs/phoenix"
related: ["arize/span-kinds-reference.md", "arize/tracing-links.md"]
author: "DevOps Team"
contributors: []
---
```

### Concept Guide

```yaml
---
title: "TanStack Router Concepts"
description: "Core routing concepts and patterns in TanStack Router"
type: "concept-guide"
tags: ["routing", "react", "tanstack", "frontend", "spa"]
category: "frontend"
subcategory: "routing"
version: "1.0"
last_updated: "2025-01-15"
status: "stable"
sources:
  - name: "TanStack Router Docs"
    url: "https://tanstack.com/router"
related: []
author: "Frontend Team"
contributors: []
---
```

## Validation

A valid reference document must:
1. Include all required fields
2. Use allowed values for `type` and `status`
3. Use ISO date format (YYYY-MM-DD) for `last_updated`
4. Have at least one tag (or empty array)
5. Include proper source attribution with name and url

## Usage

### Finding References

```bash
# Find all stable model specs
grep -l "type: \"model-spec\"" .claude/references/**/*.md | xargs grep -l "status: \"stable\""

# Find all deployment guides
grep -r "type: \"deployment-guide\"" .claude/references/

# Find references updated in 2025
grep -r "last_updated: \"2025-" .claude/references/
```

### Programmatic Access

```python
import yaml
from pathlib import Path

def load_reference_metadata(file_path):
    with open(file_path) as f:
        content = f.read()
        if content.startswith('---'):
            yaml_content = content.split('---')[1]
            return yaml.safe_load(yaml_content)
    return None

# Find all references by type
refs_by_type = {}
for md_file in Path('.claude/references').rglob('*.md'):
    metadata = load_reference_metadata(md_file)
    if metadata:
        ref_type = metadata['type']
        refs_by_type.setdefault(ref_type, []).append({
            'file': str(md_file),
            'metadata': metadata
        })
```