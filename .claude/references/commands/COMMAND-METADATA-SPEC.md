---
author: unknown
category: meta
contributors: []
description: Standard metadata specification for Claude Code command files
last_updated: '2025-11-03'
related:
- METADATA-SPEC.md
- ../specs/SPEC-METADATA-SPEC.md
sources: []
status: stable
subcategory: commands
tags:
- metadata
- standards
- commands
- documentation
- claude-code
title: Command Metadata Specification
type: meta
version: '1.0'
---

# Command Metadata Specification

All Claude Code command files (.claude/commands/*.md) should include a YAML frontmatter block with metadata to enable discovery, search, and proper tool usage validation.

## Purpose

Command metadata enables:
- **Discovery:** Find commands by purpose, tools used, or domain
- **Tool validation:** Declare which tools a command is allowed to use
- **Usage guidance:** Provide examples and argument hints
- **Search:** Build searchable command library for agents and users

## Metadata Block

```yaml
---
title: "Command Title"
description: "Brief description of what the command does"
type: "command"
tags: ["tag1", "tag2"]
category: "category-name"
subcategory: "subcategory-name"
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "stable"
allowed_tools: ["Tool1", "Tool2"]
requires_args: true
argument_hint: "[arg1] [optional-arg2]"
usage_examples:
  - "/command-name argument"
  - "/command-name arg1 arg2"
---
```

## Field Definitions

### Base Fields (Inherited from BaseMetadata)

#### title
**Required:** Yes
**Type:** String
**Description:** Short, descriptive title for the command
**Example:** `"Create Reference Documentation"`

#### description
**Required:** Yes
**Type:** String
**Description:** Brief one-line description of what the command does
**Example:** `"Research a topic and create comprehensive reference documentation with proper metadata"`

#### type
**Required:** Yes
**Type:** String (literal)
**Description:** Type of document - always "command" for command files
**Allowed Values:** `"command"`
**Example:** `"command"`

#### tags
**Required:** Yes
**Type:** Array of strings
**Description:** Keywords for search and categorization (3-10 tags recommended)
**Purpose:** Enable search by domain, purpose, or technology
**Example:** `["documentation", "research", "metadata", "references"]`
**Use:** `[]` if no tags applicable (not recommended)

#### category
**Required:** Yes
**Type:** String
**Description:** Primary category for organization
**Examples:** `"documentation"`, `"development"`, `"testing"`, `"deployment"`, `"analysis"`
**Use:** `"general"` if no specific category

#### subcategory
**Required:** Yes
**Type:** String
**Description:** Secondary categorization within category
**Examples:** `"creation"`, `"migration"`, `"planning"`, `"setup"`
**Use:** `"none"` if no subcategory

#### version
**Required:** Yes
**Type:** String
**Description:** Version of the command
**Examples:** `"1.0"`, `"1.1"`, `"2.0"`
**Use:** `"1.0"` for initial version, increment for significant changes

#### last_updated
**Required:** Yes
**Type:** String (ISO date format YYYY-MM-DD)
**Description:** Date of last significant update
**Example:** `"2025-11-03"`

#### status
**Required:** Yes
**Type:** String (from allowed values)
**Description:** Current status of the command
**Allowed Values:**
- `draft` - Command is being developed, not ready for use
- `stable` - Command is tested and ready for use
- `deprecated` - Command is no longer recommended, will be removed
- `archived` - Command is kept for reference but not active

**Example:** `"stable"`

### Command-Specific Fields

#### allowed_tools
**Required:** Yes
**Type:** Array of strings (tool names)
**Description:** List of Claude Code tools this command is allowed to use
**Purpose:** Declares tool usage for validation and documentation
**Common Tools:**
- `"Bash"` - Execute shell commands
- `"Read"` - Read files
- `"Write"` - Write new files
- `"Edit"` - Edit existing files
- `"Glob"` - File pattern matching
- `"Grep"` - Content search
- `"WebFetch"` - Fetch web content
- `"WebSearch"` - Search the web
- `"Task"` - Launch specialized agents
- `"AskUserQuestion"` - Prompt user for input
- `"TodoWrite"` - Manage task lists

**Example:** `["Bash", "Read", "WebFetch", "Write", "Glob", "Grep"]`
**Use:** `[]` if command uses no tools (rare)

#### requires_args
**Required:** Yes
**Type:** Boolean
**Description:** Whether the command requires arguments from the user
**Example:** `true` (command requires arguments), `false` (no arguments needed)

#### argument_hint
**Required:** No (required if requires_args is true)
**Type:** String
**Description:** Hint showing what arguments the command expects
**Format:** Use `[required]` and `[optional]` notation
**Example:** `"[topic-name] [optional-urls]"`
**Use:** Omit field if requires_args is false

#### usage_examples
**Required:** Yes
**Type:** Array of strings
**Description:** Example invocations of the command
**Purpose:** Show users how to use the command with real examples
**Format:** Include full command with `/command-name` and arguments
**Example:**
```yaml
usage_examples:
  - "/create-reference OpenTelemetry Collector"
  - "/create-reference Kubernetes operators https://kubernetes.io/docs/concepts/"
```
**Use:** Provide 1-3 representative examples

## Complete Examples

### Research/Creation Command

```yaml
---
title: "Create Reference Documentation"
description: "Research a topic and create comprehensive reference documentation with proper metadata"
type: "command"
tags: ["documentation", "research", "metadata", "references", "web"]
category: "documentation"
subcategory: "creation"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Bash", "Read", "WebFetch", "Write", "Glob", "Grep", "Task"]
requires_args: true
argument_hint: "[topic-name] [optional-urls]"
usage_examples:
  - "/create-reference OpenTelemetry Collector configuration"
  - "/create-reference Kubernetes operators https://kubernetes.io/docs/concepts/"
  - "/create-reference TanStack Router concepts"
---

# Create Reference Documentation

[Command content follows...]
```

### Planning Command

```yaml
---
title: "Feature Planning"
description: "Create a detailed implementation plan for a new feature using the standard spec format"
type: "command"
tags: ["planning", "feature", "specs", "implementation"]
category: "development"
subcategory: "planning"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Read", "Write", "Glob", "Grep", "Task", "AskUserQuestion"]
requires_args: true
argument_hint: "[feature-description]"
usage_examples:
  - "/feature Add user authentication with JWT"
  - "/feature Implement caching layer for API responses"
---

# Feature Planning

[Command content follows...]
```

### Initialization Command

```yaml
---
title: "Prime Context"
description: "Load context for a new agent session by analyzing codebase structure and documentation"
type: "command"
tags: ["initialization", "context", "codebase", "documentation", "onboarding"]
category: "development"
subcategory: "setup"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Bash", "Read", "Glob", "Grep", "Task"]
requires_args: false
usage_examples:
  - "/prime"
---

# Prime Context

[Command content follows...]
```

### Analysis Command

```yaml
---
title: "Split Specification"
description: "Split a large spec into incrementally verifiable phases"
type: "command"
tags: ["planning", "specs", "phases", "incremental", "analysis"]
category: "development"
subcategory: "planning"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Read", "Edit", "AskUserQuestion"]
requires_args: true
argument_hint: "[spec-file-path]"
usage_examples:
  - "/split-spec specs/large-feature.md"
  - "/split-spec specs/complex-migration.md"
---

# Split Specification

[Command content follows...]
```

## Validation Rules

A valid command metadata block must:
1. Include all required base fields
2. Have `type: "command"`
3. Use allowed values for `status`
4. Use ISO date format (YYYY-MM-DD) for `last_updated`
5. Have at least one tag (empty array allowed but not recommended)
6. Have at least one tool in `allowed_tools` (or empty array if no tools used)
7. Include `argument_hint` if `requires_args` is `true`
8. Include at least one usage example

## Usage

### Finding Commands

```bash
# Find all stable commands
rg "type: \"command\"" .claude/commands/ | xargs rg "status: \"stable\""

# Find commands that use WebFetch
rg "allowed_tools:.*WebFetch" .claude/commands/

# Find documentation-related commands
rg "category: \"documentation\"" .claude/commands/

# Find commands that require arguments
rg "requires_args: true" .claude/commands/
```

### Programmatic Access

```python
import yaml
from pathlib import Path

def load_command_metadata(file_path):
    """Extract metadata from command file."""
    with open(file_path) as f:
        content = f.read()
        if content.startswith('---'):
            yaml_content = content.split('---')[1]
            return yaml.safe_load(yaml_content)
    return None

# Find commands by tool
def find_commands_by_tool(tool_name):
    """Find all commands that use a specific tool."""
    results = []
    for cmd_file in Path('.claude/commands').glob('*.md'):
        metadata = load_command_metadata(cmd_file)
        if metadata and tool_name in metadata.get('allowed_tools', []):
            results.append({
                'file': str(cmd_file),
                'title': metadata['title'],
                'description': metadata['description']
            })
    return results

# Find commands by category
def find_commands_by_category(category):
    """Find all commands in a category."""
    results = []
    for cmd_file in Path('.claude/commands').glob('*.md'):
        metadata = load_command_metadata(cmd_file)
        if metadata and metadata.get('category') == category:
            results.append({
                'file': str(cmd_file),
                'title': metadata['title'],
                'usage_examples': metadata.get('usage_examples', [])
            })
    return results
```

## Migration Guide

### Migrating from Current Format

Current commands have minimal frontmatter:
```yaml
---
allowed-tools: [Tool1, Tool2]
description: Short description
---
```

New format extends this with full metadata:
```yaml
---
title: "Command Title"
description: "Short description"
type: "command"
tags: ["tag1", "tag2"]
category: "category"
subcategory: "subcategory"
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "stable"
allowed_tools: ["Tool1", "Tool2"]
requires_args: true
argument_hint: "[arg]"
usage_examples:
  - "/command example"
---
```

### Migration Steps

1. **Keep existing fields:**
   - `allowed-tools` → `allowed_tools` (note: dash to underscore)
   - `description` → keep as-is

2. **Add required base fields:**
   - `title` - extract from command purpose
   - `type: "command"` - always this value
   - `tags` - list relevant keywords
   - `category` - main category (documentation, development, testing, etc.)
   - `subcategory` - subcategory (creation, planning, setup, etc.)
   - `version: "1.0"` - start at 1.0
   - `last_updated` - today's date or last commit date
   - `status: "stable"` - most commands are stable

3. **Add command-specific fields:**
   - `requires_args` - does command need arguments?
   - `argument_hint` - if requires_args, describe arguments
   - `usage_examples` - provide 1-3 example invocations

### Example Migration

**Before:**
```yaml
---
allowed-tools: [Bash, Read, WebFetch, Write, Glob, Grep]
description: Research a topic and create or extend reference documentation with proper metadata
---

# Create Reference Documentation
[command content]
```

**After:**
```yaml
---
title: "Create Reference Documentation"
description: "Research a topic and create comprehensive reference documentation with proper metadata"
type: "command"
tags: ["documentation", "research", "metadata", "references", "web"]
category: "documentation"
subcategory: "creation"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed_tools: ["Bash", "Read", "WebFetch", "Write", "Glob", "Grep", "Task"]
requires_args: true
argument_hint: "[topic-name] [optional-urls]"
usage_examples:
  - "/create-reference OpenTelemetry Collector"
  - "/create-reference Kubernetes operators https://kubernetes.io/docs/"
---

# Create Reference Documentation
[command content]
```

## Best Practices

### Tool Declaration
- Be explicit about all tools used in the command
- Include conditional tools (tools that might be used based on logic)
- Order tools by importance or frequency of use
- Remove deprecated tool names

### Usage Examples
- Provide realistic, actionable examples
- Show variety: simple and complex invocations
- Use real-world topics/arguments users would encounter
- Include edge cases if relevant

### Tag Selection
- Include domain tags: `"documentation"`, `"testing"`, `"deployment"`
- Include action tags: `"creation"`, `"planning"`, `"analysis"`, `"migration"`
- Include technology tags if specific: `"git"`, `"docker"`, `"python"`
- Be generous - more tags = better discoverability

### Argument Hints
- Use square brackets: `[required]` `[optional]`
- Be specific: `[file-path]` not `[path]`
- Show format if relevant: `[YYYY-MM-DD]` or `[key=value]`
- Keep concise: focus on essential parameters

### Status Management
- `draft` - actively developing, not ready
- `stable` - tested and production-ready (most commands)
- `deprecated` - superseded by another command
- `archived` - kept for reference only

## Command Discovery

Users and agents can discover commands by:

1. **By purpose:** Search tags or description
   - "Find commands for documentation creation"
   - Tags: `"documentation"`, `"creation"`

2. **By tool:** Find commands using specific tools
   - "Find commands that use WebFetch"
   - Filter by `allowed_tools`

3. **By category:** Browse command categories
   - `"documentation"`, `"development"`, `"testing"`, `"deployment"`

4. **By examples:** See how to use commands
   - Browse `usage_examples` for patterns

This metadata enables intelligent command discovery and helps users/agents find the right tool for their task.