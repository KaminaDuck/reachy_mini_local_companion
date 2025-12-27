---
title: "PyYAML Library Guide"
description: "Complete guide to PyYAML for parsing and emitting YAML in Python"
type: "tool-reference"
tags: ["python", "yaml", "parsing", "serialization", "pyyaml", "configuration"]
category: "python"
subcategory: "yaml"
version: "6.0"
last_updated: "2025-11-02"
status: "stable"
sources:
  - name: "PyYAML Documentation"
    url: "https://pyyaml.org/wiki/PyYAMLDocumentation"
related: ["python-frontmatter-library-guide.md"]
author: "unknown"
contributors: []
---

# PyYAML Library Guide

PyYAML is the canonical YAML parser and emitter for Python, enabling serialization and deserialization of YAML documents. The library provides both pure Python implementations and optional C-based bindings (LibYAML) for performance. ([PyYAML Docs][1])

## Installation

Basic installation via pip:

```bash
pip install pyyaml
```

For significantly faster C bindings with LibYAML:

```bash
python setup.py --with-libyaml install
```

The library automatically uses C implementations when available. ([PyYAML Docs][1])

## Critical Security Warning

**Never use `yaml.load()` with untrusted data.** The function can execute arbitrary Python code and is as dangerous as `pickle.load()`. Always use `yaml.safe_load()` for external input. ([PyYAML Security][1])

## Loading YAML

### Safe Loading (Recommended)

For untrusted sources, use `safe_load()` which restricts parsing to standard YAML tags only:

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# From string
data = yaml.safe_load("""
database:
  host: localhost
  port: 5432
""")
```

This prevents code execution vulnerabilities. ([PyYAML Security][1])

### Standard Loading (Trusted Sources Only)

For trusted internal data requiring custom Python objects:

```python
import yaml

# Explicitly specify loader for clarity
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open('internal_config.yaml', 'r') as f:
    data = yaml.load(f, Loader=Loader)
```

Always specify the `Loader` parameter explicitly. ([PyYAML Docs][1])

### Loading Multiple Documents

YAML files can contain multiple documents separated by `---`:

```python
import yaml

documents = """---
document: first
---
document: second
---
document: third
"""

for doc in yaml.safe_load_all(documents):
    print(doc)
# Output:
# {'document': 'first'}
# {'document': 'second'}
# {'document': 'third'}
```

Use `safe_load_all()` for multiple document streams. ([PyYAML Docs][1])

## Dumping Python Objects to YAML

### Basic Dumping

Convert Python objects to YAML strings:

```python
import yaml

data = {
    'name': 'Application',
    'version': '1.0',
    'features': ['auth', 'api', 'ui']
}

yaml_string = yaml.dump(data)
print(yaml_string)
# Output:
# features:
# - auth
# - api
# - ui
# name: Application
# version: '1.0'
```

For performance with large datasets, use CDumper:

```python
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

output = yaml.dump(data, Dumper=Dumper)
```

([PyYAML Docs][1])

### Controlling Output Format

PyYAML provides several formatting options:

```python
import yaml

data = {'name': 'test', 'items': list(range(10))}

# Block style (more readable, default for nested)
yaml.dump(data, default_flow_style=False)

# Flow style (more compact)
yaml.dump(data, default_flow_style=True)
# Output: {items: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name: test}

# Custom width and indentation
yaml.dump(data, width=50, indent=4)

# Canonical YAML format
yaml.dump(data, canonical=True)

# Explicit string quoting
yaml.dump(data, default_style='"')
```

By default, PyYAML uses block style for nested collections and may use flow style for flat dictionaries. ([PyYAML Docs][1])

### Writing to Files

Dump directly to file objects:

```python
import yaml

data = {'config': 'values'}

with open('output.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
```

## Error Handling

Handle YAML parsing errors with detailed position information:

```python
import yaml

try:
    config = yaml.safe_load(file_content)
except yaml.YAMLError as exc:
    if hasattr(exc, 'problem_mark'):
        mark = exc.problem_mark
        print(f"Error at line {mark.line + 1}, column {mark.column + 1}")
    print(f"Error: {exc}")
```

The `problem_mark` attribute provides line and column numbers for debugging. ([PyYAML Docs][1])

## Custom Tags and Objects

### Using YAMLObject

Define custom classes that serialize/deserialize automatically:

```python
import yaml

class Monster(yaml.YAMLObject):
    yaml_tag = '!Monster'
    yaml_loader = yaml.SafeLoader  # Make safe for safe_load()

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp!r})"

# Serialize
monster = Monster('Cave Spider', hp=12, ac=14, attacks=['bite'])
yaml_str = yaml.dump(monster)
print(yaml_str)
# Output:
# !Monster
# ac: 14
# attacks: [bite]
# hp: 12
# name: Cave Spider

# Deserialize
loaded = yaml.safe_load(yaml_str)
print(loaded)  # Monster(name='Cave Spider', hp=12)
```

Set `yaml_loader = yaml.SafeLoader` to make custom classes usable with `safe_load()`. ([PyYAML Docs][1])

### Manual Constructor and Representer Registration

For more control, register constructors and representers explicitly:

```python
import yaml

class Dice:
    def __init__(self, count, sides):
        self.count = count
        self.sides = sides

# Define how to represent Dice as YAML
def dice_representer(dumper, data):
    return dumper.represent_scalar('!dice', f'{data.count}d{data.sides}')

# Define how to construct Dice from YAML
def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    count, sides = value.split('d')
    return Dice(int(count), int(sides))

# Register with both safe and unsafe loaders/dumpers
yaml.add_representer(Dice, dice_representer)
yaml.add_constructor('!dice', dice_constructor, yaml.SafeLoader)

# Usage
damage = Dice(2, 6)
yaml_str = yaml.dump(damage)  # !dice '2d6'
loaded = yaml.safe_load(yaml_str)  # Dice(2, 6)
```

Always register custom constructors with `SafeLoader` to enable `safe_load()`. ([PyYAML Docs][1])

### Implicit Tag Resolution

Automatically recognize patterns without explicit tags:

```python
import yaml
import re

# Auto-detect dice notation pattern
pattern = re.compile(r'^\d+d\d+$')
yaml.add_implicit_resolver('!dice', pattern, Loader=yaml.SafeLoader)

# Now "2d6" is automatically recognized as Dice
data = yaml.safe_load("damage: 2d6")
print(type(data['damage']))  # <class 'Dice'>
```

Implicit resolvers eliminate the need for explicit `!dice` tags in YAML files. ([PyYAML Docs][1])

## Python 2 vs. Python 3 Differences

### Python 3 (Current)

- `str` → `!!str` (Unicode strings)
- `bytes` → `!!binary` (binary data)
- `yaml.dump()` returns `str` object
- Full Unicode support

### Python 2 (Legacy)

- `str` → `!!str`, `!!python/str`, or `!binary`
- `unicode` → `!!python/unicode` or `!!str`
- `yaml.dump()` returns UTF-8 encoded `str`

Legacy tags like `!!python/str` and `!!python/unicode` are still supported for backward compatibility. ([PyYAML Docs][1])

## Common Patterns

### Configuration Files

Load configuration with safe defaults:

```python
import yaml
from pathlib import Path

def load_config(config_path: Path) -> dict:
    """Load YAML configuration file safely."""
    try:
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        return config or {}  # Handle empty files
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {config_path}: {e}")
    except FileNotFoundError:
        return {}  # Return empty config if file missing
```

### Structured Data Export

Export Python objects with readable formatting:

```python
import yaml
from typing import Any

def export_data(data: Any, output_path: Path) -> None:
    """Export data to YAML with readable formatting."""
    with output_path.open('w') as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,  # Block style
            indent=2,                   # 2-space indent
            sort_keys=False,            # Preserve order
            allow_unicode=True          # Support Unicode
        )
```

### Validation and Schemas

Combine with Pydantic for validated configuration:

```python
import yaml
from pydantic import BaseModel, ValidationError

class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str

def load_validated_config(config_path: Path) -> DatabaseConfig:
    """Load and validate YAML configuration."""
    with config_path.open('r') as f:
        data = yaml.safe_load(f)

    try:
        return DatabaseConfig(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid config: {e}")
```

## Performance Considerations

### C Bindings (LibYAML)

For performance-critical applications, use C implementations:

```python
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    print("Warning: Using pure Python YAML (slower)")

# Use imported Loader/Dumper
data = yaml.load(stream, Loader=Loader)
output = yaml.dump(data, Dumper=Dumper)
```

C bindings provide significant speedup (10-100x) for large documents. ([PyYAML Docs][1])

### Lazy Loading

For very large YAML files, load documents lazily:

```python
import yaml

with open('large_dataset.yaml', 'r') as f:
    for document in yaml.safe_load_all(f):
        process(document)
        # Each document processed independently
        # Memory usage stays constant
```

## Best Practices

1. **Always use `safe_load()` for external input** — prevents code execution
2. **Specify Loader explicitly** — makes security choices visible
3. **Register custom types with SafeLoader** — enables safe deserialization
4. **Handle empty files** — `safe_load()` returns `None` for empty input
5. **Use block style for readability** — `default_flow_style=False`
6. **Catch `YAMLError` broadly** — covers all parsing/dumping errors
7. **Validate after loading** — use Pydantic or similar for schema enforcement
8. **Use C bindings in production** — significant performance improvement

## Troubleshooting

### Common Issues

**Issue**: `yaml.constructor.ConstructorError: could not determine a constructor for the tag '!CustomType'`

**Solution**: Register constructor for the custom tag or use `safe_load()` which ignores custom tags.

**Issue**: `YAMLError: mapping values are not allowed here`

**Solution**: Check for missing quotes around strings containing colons:
```yaml
# Wrong
title: Error: Something failed

# Correct
title: "Error: Something failed"
```

**Issue**: Dates being parsed as `datetime` objects unexpectedly

**Solution**: Quote ISO date strings if you want them as strings:
```yaml
# Parsed as datetime.date object
date: 2025-11-02

# Kept as string
date: "2025-11-02"
```

## Version Information

This guide covers PyYAML 6.0, the latest stable version. Python 3 support began at release 3.08. The library maintains strong backward compatibility while adding type hints and modern Python features. ([PyYAML Docs][1])

## References

[1]: https://pyyaml.org/wiki/PyYAMLDocumentation "PyYAML Documentation"
