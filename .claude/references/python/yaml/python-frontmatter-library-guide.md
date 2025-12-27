---
title: "Python-Frontmatter Library Guide"
description: "Complete guide to python-frontmatter for parsing YAML/TOML/JSON metadata blocks"
type: "tool-reference"
tags: ["python", "frontmatter", "yaml", "markdown", "metadata", "jekyll"]
category: "python"
subcategory: "yaml"
version: "1.1.0"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "python-frontmatter Documentation"
    url: "https://python-frontmatter.readthedocs.io/"
  - name: "python-frontmatter GitHub"
    url: "https://github.com/eyeseast/python-frontmatter"
related: ["pyyaml-library-guide.md"]
author: "unknown"
contributors: []
---

# Python-Frontmatter Library Guide

Python-frontmatter is a library for parsing and managing files containing Jekyll-style frontmatter — structured metadata blocks at the beginning of text documents. It enables adding arbitrary, structured metadata to any text document regardless of type. ([python-frontmatter Docs][1])

## Installation

Install via pip:

```bash
pip install python-frontmatter
```

Latest version: **1.1.0** (January 2024) with type checking support. ([python-frontmatter GitHub][2])

## Core Concepts

Frontmatter consists of a metadata block (typically YAML) followed by content:

```markdown
---
title: "Document Title"
date: 2025-11-02
tags: ["python", "tutorial"]
---

# Document Content

This is the main content of the document.
```

The library parses this into a `Post` object with two main components:
- `.metadata` — dictionary of structured metadata
- `.content` — string containing the document body

([python-frontmatter Docs][1])

## Loading Frontmatter

### From Files

Load from file paths:

```python
import frontmatter

# Load from path
post = frontmatter.load('document.md')

print(post['title'])        # Access metadata
print(post.content)         # Access content
print(post.metadata)        # Full metadata dict
```

Load from file objects:

```python
import frontmatter

with open('document.md', 'r') as f:
    post = frontmatter.load(f)
```

([python-frontmatter Docs][1])

### From Strings

Parse frontmatter directly from strings:

```python
import frontmatter

text = """---
title: "Example"
author: "Alice"
---

# Content here
"""

post = frontmatter.loads(text)
print(post['title'])   # "Example"
print(post['author'])  # "Alice"
print(post.content)    # "# Content here\n"
```

([python-frontmatter Docs][1])

### Parse Without Post Object

Get metadata and content separately without creating a Post object:

```python
import frontmatter

text = """---
key: value
---
Content body
"""

metadata, content = frontmatter.parse(text)
print(metadata)  # {'key': 'value'}
print(content)   # 'Content body\n'
```

Useful when you only need the data, not the Post object interface. ([python-frontmatter Docs][1])

## Accessing Data

### Dictionary-Style Access

Post objects act as dictionary proxies for metadata:

```python
import frontmatter

post = frontmatter.loads("""---
title: "My Post"
tags: ["python", "tutorial"]
published: true
---

Content here.
""")

# Dictionary access
print(post['title'])           # "My Post"
print(post['tags'])            # ["python", "tutorial"]
print(post.get('author', 'Unknown'))  # "Unknown" (default)

# Check if key exists
if 'published' in post:
    print("Post is published")

# Iterate over metadata
for key, value in post.metadata.items():
    print(f"{key}: {value}")
```

### Attribute Access

Access common attributes directly:

```python
post.content      # Document body (string)
post.metadata     # Full metadata dictionary
```

([python-frontmatter Docs][1])

## Creating and Modifying Posts

### Create New Posts

Build Post objects programmatically:

```python
import frontmatter

# Create empty post
post = frontmatter.Post("")

# Set metadata
post['title'] = "New Document"
post['date'] = "2025-11-02"
post['tags'] = ["python", "example"]

# Set content
post.content = "This is the document content."

# Convert to string
text = frontmatter.dumps(post)
print(text)
# Output:
# ---
# date: '2025-11-02'
# tags:
# - python
# - example
# title: New Document
# ---
#
# This is the document content.
```

### Create with Initial Data

Pass content and metadata to constructor:

```python
import frontmatter

post = frontmatter.Post(
    "# Content",
    title="Document Title",
    author="Alice",
    tags=["python"]
)

print(post['title'])   # "Document Title"
print(post.content)    # "# Content"
```

([python-frontmatter Docs][1])

### Modify Existing Posts

Update metadata and content:

```python
import frontmatter

# Load existing post
post = frontmatter.load('article.md')

# Modify metadata
post['title'] = "Updated Title"
post['updated_at'] = "2025-11-02"

# Add new metadata
post['version'] = 2

# Modify content
post.content = post.content + "\n\n## New Section"

# Write back to file
with open('article.md', 'w') as f:
    frontmatter.dump(post, f)
```

([python-frontmatter Docs][1])

## Writing Frontmatter

### Dump to String

Convert Post to formatted string:

```python
import frontmatter

post = frontmatter.Post("Content", title="Example", version=1)
text = frontmatter.dumps(post)
print(text)
# Output:
# ---
# title: Example
# version: 1
# ---
#
# Content
```

([python-frontmatter Docs][1])

### Dump to File

Write directly to file objects:

```python
import frontmatter

post = frontmatter.Post("Content", title="Document")

with open('output.md', 'w') as f:
    frontmatter.dump(post, f)
```

([python-frontmatter Docs][1])

## Supported Formats

Python-frontmatter supports multiple metadata formats through handlers:

### YAML (Default)

The default and most common format:

```markdown
---
title: "YAML Format"
tags: ["a", "b", "c"]
---

Content
```

### TOML

Using `+++` delimiters:

```markdown
+++
title = "TOML Format"
tags = ["a", "b", "c"]
+++

Content
```

### JSON

Using `;;;` delimiters or explicit JSON blocks:

```markdown
;;;
{
  "title": "JSON Format",
  "tags": ["a", "b", "c"]
}
;;;

Content
```

The library automatically detects the format based on delimiters. ([python-frontmatter Docs][1])

## Encoding Handling

Handle UTF-8 BOM (byte order mark) correctly:

```python
import frontmatter

# Read files with UTF-8 BOM
with open('document.md', 'r', encoding='utf-8-sig') as f:
    post = frontmatter.load(f)
```

The `utf-8-sig` encoding automatically strips the BOM if present. ([python-frontmatter GitHub][2])

## Custom Handlers

Define custom parsing and serialization behavior:

```python
import frontmatter
import yaml

# Create custom handler with specific YAML options
handler = frontmatter.YAMLHandler()

# Load with custom handler
post = frontmatter.loads(text, handler=handler)

# Dump with custom handler
output = frontmatter.dumps(post, handler=handler)
```

Handlers control how metadata is serialized and deserialized, enabling custom formatting or validation. ([python-frontmatter Docs][1])

## Common Patterns

### Parse Markdown Files with Metadata

Process a directory of markdown files:

```python
import frontmatter
from pathlib import Path

def process_markdown_files(directory: Path):
    """Process all markdown files in directory."""
    for md_file in directory.glob('*.md'):
        post = frontmatter.load(md_file)

        # Access metadata
        title = post.get('title', md_file.stem)
        tags = post.get('tags', [])
        date = post.get('date')

        # Process content
        content = post.content

        print(f"Processing: {title}")
        print(f"Tags: {', '.join(tags)}")
        print(f"Content length: {len(content)} chars")
```

### Build Static Site Metadata Index

Create an index of all posts:

```python
import frontmatter
from pathlib import Path
from datetime import datetime

def build_post_index(content_dir: Path) -> list[dict]:
    """Build index of all posts with metadata."""
    posts = []

    for md_file in content_dir.rglob('*.md'):
        post = frontmatter.load(md_file)

        posts.append({
            'path': str(md_file.relative_to(content_dir)),
            'title': post.get('title', 'Untitled'),
            'date': post.get('date'),
            'tags': post.get('tags', []),
            'excerpt': post.content[:200],
        })

    # Sort by date
    posts.sort(key=lambda p: p['date'] or datetime.min, reverse=True)
    return posts
```

### Validate Metadata Schema

Combine with Pydantic for validation:

```python
import frontmatter
from pydantic import BaseModel, ValidationError
from pathlib import Path

class PostMetadata(BaseModel):
    title: str
    date: str
    tags: list[str]
    author: str

def load_validated_post(file_path: Path):
    """Load post and validate metadata."""
    post = frontmatter.load(file_path)

    try:
        # Validate metadata
        metadata = PostMetadata(**post.metadata)
        return post, metadata
    except ValidationError as e:
        raise ValueError(f"Invalid metadata in {file_path}: {e}")
```

### Extract Metadata Without Loading Full Content

Parse only metadata for performance:

```python
import frontmatter
from pathlib import Path

def extract_metadata(file_path: Path) -> dict:
    """Extract only metadata without processing content."""
    with open(file_path, 'r') as f:
        metadata, _ = frontmatter.parse(f.read())
    return metadata
```

### Convert Between Formats

Migrate from one format to another:

```python
import frontmatter
from pathlib import Path

def convert_yaml_to_toml(input_dir: Path, output_dir: Path):
    """Convert YAML frontmatter files to TOML format."""
    for md_file in input_dir.glob('*.md'):
        # Load with YAML
        post = frontmatter.load(md_file)

        # Write with TOML handler
        toml_handler = frontmatter.TOMLHandler()
        output_path = output_dir / md_file.name

        with open(output_path, 'w') as f:
            frontmatter.dump(post, f, handler=toml_handler)
```

### Update Metadata Across Multiple Files

Bulk update operation:

```python
import frontmatter
from pathlib import Path

def add_metadata_field(directory: Path, field: str, value):
    """Add a metadata field to all markdown files."""
    for md_file in directory.glob('*.md'):
        post = frontmatter.load(md_file)

        # Add or update field
        post[field] = value

        # Write back
        with open(md_file, 'w') as f:
            frontmatter.dump(post, f)

        print(f"Updated: {md_file}")

# Usage
add_metadata_field(Path('content/posts'), 'version', '2.0')
```

## Integration with Search Systems

Build search index from frontmatter:

```python
import frontmatter
from pathlib import Path
from typing import TypedDict

class SearchDocument(TypedDict):
    path: str
    title: str
    content: str
    tags: list[str]
    metadata: dict

def build_search_index(content_dir: Path) -> list[SearchDocument]:
    """Build searchable index from markdown files."""
    documents = []

    for md_file in content_dir.rglob('*.md'):
        try:
            post = frontmatter.load(md_file)

            documents.append({
                'path': str(md_file.relative_to(content_dir)),
                'title': post.get('title', md_file.stem),
                'content': post.content,
                'tags': post.get('tags', []),
                'metadata': post.metadata,
            })
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            continue

    return documents
```

This pattern is used by the Workbench Search API to index reference documentation. ([Project Context])

## Error Handling

Handle parsing errors gracefully:

```python
import frontmatter
import yaml

def safe_load_post(file_path: Path):
    """Load post with error handling."""
    try:
        post = frontmatter.load(file_path)
        return post
    except yaml.YAMLError as e:
        print(f"YAML parsing error in {file_path}: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Unexpected error loading {file_path}: {e}")
        return None
```

Common errors:
- **YAML syntax errors** — malformed YAML in frontmatter
- **Missing delimiters** — no closing `---` marker
- **Encoding issues** — non-UTF-8 files (use `encoding='utf-8-sig'`)

## Best Practices

1. **Use consistent delimiters** — stick to `---` for YAML (most common)
2. **Validate metadata** — use Pydantic or similar for schema enforcement
3. **Handle missing metadata** — use `.get()` with defaults
4. **Use UTF-8 encoding** — specify `encoding='utf-8-sig'` for BOM handling
5. **Parse only when needed** — use `frontmatter.parse()` if you don't need Post object
6. **Keep metadata structured** — use consistent keys across documents
7. **Version your metadata** — include version field for schema migrations
8. **Test round-trip** — ensure `dump(load(file))` preserves content

## Performance Considerations

### Lazy Loading

Don't load content if you only need metadata:

```python
import frontmatter

# Fast: parse only
metadata, _ = frontmatter.parse(file_content)

# Slower: create Post object
post = frontmatter.loads(file_content)
```

### Caching

Cache parsed posts for repeated access:

```python
from functools import lru_cache
from pathlib import Path

@lru_cache(maxsize=128)
def load_post_cached(file_path: str):
    """Load post with LRU cache."""
    return frontmatter.load(file_path)
```

### Batch Processing

Process multiple files efficiently:

```python
import frontmatter
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def load_posts_parallel(file_paths: list[Path]) -> list:
    """Load multiple posts in parallel."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(frontmatter.load, file_paths))
```

## Troubleshooting

### Issue: Empty Metadata

If `post.metadata` is empty when frontmatter exists:

```python
import frontmatter

# Check for BOM
with open('file.md', 'r', encoding='utf-8-sig') as f:
    post = frontmatter.load(f)

# Check delimiters (must be exactly ---)
# Wrong: ---- or -- --
# Correct: ---
```

### Issue: Content Includes Frontmatter

If content includes the YAML block:

```python
# Ensure delimiters are on separate lines
# Wrong:
# --- title: "Test" ---
# Content

# Correct:
# ---
# title: "Test"
# ---
# Content
```

### Issue: Metadata Not Updating

If changes don't persist:

```python
import frontmatter

post = frontmatter.load('file.md')
post['title'] = "New Title"

# Must explicitly write back
with open('file.md', 'w') as f:
    frontmatter.dump(post, f)  # ← Required!
```

## Version Compatibility

- **Python 3.7+** — Required for modern features
- **Type Checking** — v1.1.0+ includes type hints
- **Dependencies** — PyYAML required for YAML support

## Project Usage

This library is used in the Workbench Search API Phase 1 to extract metadata from markdown reference files:

```python
import frontmatter
from pathlib import Path

def extract_file_metadata(file_path: Path):
    """Extract metadata from markdown file."""
    try:
        post = frontmatter.loads(file_path.read_text(encoding='utf-8'))
        return post.metadata if post.metadata else None
    except Exception:
        return None
```

([Project Context])

## References

[1]: https://python-frontmatter.readthedocs.io/ "Python-Frontmatter Documentation"
[2]: https://github.com/eyeseast/python-frontmatter "Python-Frontmatter GitHub Repository"
