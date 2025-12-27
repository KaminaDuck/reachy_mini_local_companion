---
author: unknown
category: python
contributors: []
description: Index of YAML parsing and frontmatter handling libraries for Python
last_updated: '2025-11-02'
related:
- README.md
sources: []
status: stable
subcategory: yaml
tags:
- python
- yaml
- frontmatter
- parsing
- index
title: Python YAML Libraries Index
type: meta
version: '1.0'
---

# Python YAML Libraries

Reference documentation for YAML parsing, serialization, and frontmatter handling in Python.

## Available References

### Core YAML Parsing

**[PyYAML Library Guide](pyyaml-library-guide.md)**
Complete guide to PyYAML, the canonical YAML parser and emitter for Python. Covers safe loading, custom tags, serialization, and security best practices.

**Topics:**
- Safe vs. unsafe loading (`safe_load()` vs `load()`)
- Dumping Python objects to YAML
- Custom tags and object serialization
- Error handling and troubleshooting
- Performance with C bindings (LibYAML)

### Frontmatter Parsing

**[Python-Frontmatter Library Guide](python-frontmatter-library-guide.md)**
Complete guide to python-frontmatter for parsing Jekyll-style metadata blocks in text files. Essential for static site generators and document management systems.

**Topics:**
- Loading and parsing frontmatter from files and strings
- Creating and modifying Post objects
- Supported formats (YAML, TOML, JSON)
- Integration with search systems
- Common patterns for static sites

## Quick Comparison

| Feature | PyYAML | python-frontmatter |
|---------|--------|-------------------|
| **Purpose** | Parse/emit YAML | Parse frontmatter + content |
| **Input** | Pure YAML files | Text files with metadata blocks |
| **Output** | Python objects | Post object (metadata + content) |
| **Use Case** | Config files, data serialization | Markdown files, static sites |
| **Formats** | YAML only | YAML, TOML, JSON |

## Common Use Cases

### Configuration Files
Use **PyYAML** directly:
```python
import yaml
config = yaml.safe_load(open('config.yaml'))
```

### Markdown Files with Metadata
Use **python-frontmatter**:
```python
import frontmatter
post = frontmatter.load('article.md')
print(post['title'])  # metadata
print(post.content)   # content
```

### Workbench Search API
The project uses **python-frontmatter** to extract metadata from reference documentation:
```python
import frontmatter
post = frontmatter.loads(file_content)
metadata = post.metadata  # FileMetadata Pydantic model
```

## Installation

```bash
# PyYAML (required for both)
pip install pyyaml

# python-frontmatter (requires PyYAML)
pip install python-frontmatter
```

## Security Notes

- **Always use `yaml.safe_load()`** for untrusted data
- **Never use `yaml.load()`** without specifying `Loader=SafeLoader`
- **python-frontmatter uses PyYAML** — inherits same security considerations
- **Validate metadata** after parsing (use Pydantic or similar)

## Related References

- [Pydantic Library Guide](../pydantic/pydantic-library-guide.md) — For metadata validation
- [Python Index](../README.md) — Main Python references index

## External Resources

- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [python-frontmatter Docs](https://python-frontmatter.readthedocs.io/)
- [YAML Specification](https://yaml.org/spec/1.2.2/)