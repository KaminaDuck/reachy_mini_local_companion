---
title: "Pydantic: Data Validation Library"
description: "Python data validation using type hints with Rust-powered performance"
type: "framework-guide"
tags: ["pydantic", "python", "validation", "type-hints", "data-modeling", "serialization", "json-schema", "rust"]
category: "python"
subcategory: "data-validation"
version: "2.12"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Pydantic Documentation"
    url: "https://docs.pydantic.dev/latest/"
  - name: "Pydantic Models"
    url: "https://docs.pydantic.dev/latest/concepts/models/"
  - name: "Pydantic Fields"
    url: "https://docs.pydantic.dev/latest/concepts/fields/"
  - name: "Pydantic Validators"
    url: "https://docs.pydantic.dev/latest/concepts/validators/"
  - name: "Pydantic Serialization"
    url: "https://docs.pydantic.dev/latest/concepts/serialization/"
  - name: "Pydantic JSON Schema"
    url: "https://docs.pydantic.dev/latest/concepts/json_schema/"
  - name: "Why Pydantic"
    url: "https://docs.pydantic.dev/latest/why/"
  - name: "Pydantic Performance"
    url: "https://docs.pydantic.dev/latest/concepts/performance/"
related: ["../fastapi/fastapi-framework-guide.md"]
author: "unknown"
contributors: []
---

# Pydantic: Data Validation Library

Pydantic is a data validation library for Python that leverages type hints to control schema validation and serialization. As the documentation states, it is "the most widely used data validation library for Python." ([Pydantic Documentation][1])

## Overview

Pydantic validates data through Python type annotations, reducing code complexity while improving IDE integration and static analysis compatibility. ([Pydantic Documentation][1]) The core validation engine is implemented in Rust, making Pydantic among the fastest data validation libraries available for Python developers. ([Pydantic Documentation][1])

### Key Features

**Type-Driven Validation**: Schema validation is controlled through Python type annotations, reducing code complexity while improving IDE integration and static analysis compatibility. ([Pydantic Documentation][1])

**Performance**: The core validation engine is implemented in Rust via `pydantic-core`, making Pydantic among the fastest data validation libraries available. ([Pydantic Documentation][1], [Why Pydantic][7])

**Flexible Validation Modes**: The library supports both strict mode (no data conversion) and lax mode (intelligent type coercion when appropriate). ([Pydantic Documentation][1])

**JSON Schema Support**: Pydantic models can generate JSON Schema output, enabling seamless integration with other tools and systems. ([Pydantic Documentation][1])

**Broad Compatibility**: Beyond custom classes, Pydantic validates standard library types including dataclasses and TypedDicts. ([Pydantic Documentation][1])

**Extensibility**: Custom validators and serializers allow developers to modify data processing in sophisticated ways. ([Pydantic Documentation][1])

### Primary Use Cases

- Web API request validation
- Configuration file parsing
- Database model definition
- Data transformation and serialization
- Cross-system data exchange

([Pydantic Documentation][1])

### Adoption

The ecosystem reflects Pydantic's utility: approximately 8,000 PyPI packages depend on it, including FastAPI, LangChain, and Django Ninja. ([Pydantic Documentation][1]) The documentation notes that Pydantic has "466,400 repositories on GitHub and 8,119 packages on PyPI" depending on it, with adoption spanning organizations like NASA, Netflix, Microsoft, and OpenAI. ([Why Pydantic][7])

## Installation

### Basic Installation

```bash
pip install pydantic
```

### Using uv

```bash
# Add to project
uv add pydantic

# With email validation
uv add "pydantic[email]"
```

### Optional Dependencies

```bash
# Email validation
pip install "pydantic[email]"

# Dotenv support
pip install "pydantic-settings"
```

## Core Concepts

The fundamental workflow involves creating a class inheriting from `BaseModel`, defining fields with type annotations, and instantiating it with data. Pydantic automatically validates and coerces values according to their declared types, raising `ValidationError` exceptions with detailed diagnostics when validation fails. ([Pydantic Documentation][1])

### Models

Pydantic models are classes inheriting from `BaseModel` with annotated attributes as fields. As the documentation states: "Models are simply classes which inherit from `BaseModel` and define fields as annotated attributes." ([Pydantic Models][2])

### Basic Model Definition

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
```

([Pydantic Models][2])

### Field Types & Validation

Pydantic supports extensive type annotations and automatically coerces compatible data types. For instance, the string `'123'` converts to integer `123`. The framework guarantees "the fields of the resultant model instance will conform to the field types defined on the model." ([Pydantic Models][2])

### Creating Model Instances

```python
user = User(id='123', name='John')
print(user)
# id=123 name='John'

print(user.id)
# 123

print(type(user.id))
# <class 'int'>
```

## Models

### Model Methods

The following methods are available on all Pydantic models ([Pydantic Models][2]):

| Method | Purpose |
|--------|---------|
| `model_validate()` | Validates dictionaries or objects against the model |
| `model_dump()` | Returns a dictionary representation |
| `model_dump_json()` | Returns JSON string representation |
| `model_copy()` | Creates a model copy with optional updates |
| `model_construct()` | Creates models without validation |

### Data Handling

**Coercion**: Pydantic converts input data to match field types, sometimes losing information intentionally. ([Pydantic Models][2])

**Extra Data**: By default, extra fields are ignored. Use `ConfigDict(extra='allow')` to store them or `extra='forbid'` to reject them. ([Pydantic Models][2])

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: int
    name: str
```

**Immutability**: Set `frozen=True` in model config to prevent attribute modifications. ([Pydantic Models][2])

```python
class FrozenUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    name: str
```

### Error Handling

Validation failures raise `ValidationError` containing details about all errors found, helping identify exactly what went wrong. ([Pydantic Models][2])

```python
from pydantic import ValidationError

try:
    User(id='not an int')
except ValidationError as e:
    print(e)
```

## Fields

Pydantic supports two approaches for defining fields ([Pydantic Fields][3]):

### Direct Assignment

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(frozen=True)
```

### Annotated Pattern

```python
from typing import Annotated
from pydantic import BaseModel, Field

class User(BaseModel):
    name: Annotated[str, Field(strict=True)]
```

The annotated pattern offers advantages: it clarifies that fields remain required despite value assignment, allows multiple metadata elements, and enables reusable type definitions. ([Pydantic Fields][3])

### Field Configuration

**Default Values**: Fields can have defaults via assignment or the `default` parameter. For dynamic defaults, use `default_factory` with a callable ([Pydantic Fields][3]):

```python
from uuid import uuid4

class Model(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

**Aliases**: Three alias options exist ([Pydantic Fields][3]):
- `alias`: For both validation and serialization
- `validation_alias`: Validation only
- `serialization_alias`: Serialization only

```python
class User(BaseModel):
    name: str = Field(alias='userName')
```

**Constraints**: "The Field() function can also be used to add constraints to specific types" like `gt=0` for integers or `max_length=3` for strings. ([Pydantic Fields][3])

```python
class User(BaseModel):
    age: int = Field(gt=0, lt=150)
    name: str = Field(min_length=1, max_length=100)
```

### Advanced Features

**Strict Mode**: `Field(strict=True)` enforces strict validation, rejecting type coercion. ([Pydantic Fields][3])

```python
class StrictModel(BaseModel):
    count: int = Field(strict=True)
    # Will reject count='123', requires actual int
```

**Immutability**: `Field(frozen=True)` prevents reassignment after model creation, emulating frozen dataclass behavior. ([Pydantic Fields][3])

**Deprecation**: Mark fields with `deprecated='message'` to emit runtime warnings and update JSON schemas. ([Pydantic Fields][3])

```python
class OldModel(BaseModel):
    old_field: str = Field(deprecated='Use new_field instead')
    new_field: str
```

**Computed Fields**: The `@computed_field` decorator includes property or cached_property attributes in serialization and JSON schema generation. ([Pydantic Fields][3])

```python
from pydantic import computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
```

### Field Inspection

Access field metadata via `Model.model_fields['field_name']`, returning a `FieldInfo` instance with annotation, alias, and metadata details. ([Pydantic Fields][3])

```python
print(User.model_fields['name'])
```

## Validators

Pydantic supports four field validator types ([Pydantic Validators][4]):

### Field Validators

**After Validators**: "run after Pydantic's internal validation" and are generally safer to implement since they work with already-validated data. ([Pydantic Validators][4])

```python
from pydantic import field_validator

class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v.title()
```

**Before Validators**: Execute prior to Pydantic's parsing, offering flexibility but requiring handling of raw input that could be any object type. ([Pydantic Validators][4])

```python
from pydantic import field_validator

class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def parse_age(cls, v):
        if isinstance(v, str):
            return int(v.strip())
        return v
```

**Plain Validators**: Similar to before validators but "terminate validation immediately after returning, so no further validators are called." ([Pydantic Validators][4])

**Wrap Validators**: The most flexible option, allowing code execution before or after Pydantic validation through an optional handler parameter. ([Pydantic Validators][4])

```python
from pydantic import field_validator, ValidationInfo
from pydantic.functional_validators import WrapValidator

class User(BaseModel):
    name: str

    @field_validator('name', mode='wrap')
    @classmethod
    def validate_name(cls, v, handler, info: ValidationInfo):
        # Custom logic before validation
        result = handler(v)
        # Custom logic after validation
        return result
```

### Implementation Patterns

Two approaches exist ([Pydantic Validators][4]):

**Annotated Pattern**: Makes validators reusable across multiple fields and models by creating custom types.

```python
from typing import Annotated
from pydantic import AfterValidator

def check_positive(v: int) -> int:
    assert v > 0, 'must be positive'
    return v

PositiveInt = Annotated[int, AfterValidator(check_positive)]

class Model(BaseModel):
    count: PositiveInt
```

**Decorator Pattern**: Uses `@field_validator()` to apply validation functions to specific fields, supporting multiple field targets simultaneously.

### Model Validators

Three model validator types exist ([Pydantic Validators][4]):

- **After**: Run post-validation as instance methods; must return the validated instance
- **Before**: Execute pre-instantiation using classmethods; handle raw input data
- **Wrap**: Most flexible; allow conditional validation with handler delegation

```python
from pydantic import model_validator

class User(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'User':
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

### Raising Errors

Validators can raise `ValueError`, `AssertionError`, or `PydanticCustomError` to signal validation failures. The custom error type "provides extra flexibility" for detailed error reporting. ([Pydantic Validators][4])

```python
from pydantic import PydanticCustomError

@field_validator('email')
@classmethod
def validate_email(cls, v: str) -> str:
    if '@' not in v:
        raise PydanticCustomError(
            'invalid_email',
            'Email must contain @ symbol',
            {'value': v}
        )
    return v
```

### Validation Context

Both field and model validators accept optional `ValidationInfo` arguments providing access to already-validated data, user-defined context, validation mode, and field names. ([Pydantic Validators][4])

```python
from pydantic import field_validator, ValidationInfo

class User(BaseModel):
    name: str
    role: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo) -> str:
        if info.context and info.context.get('strict'):
            # Apply stricter validation
            pass
        return v

# Usage
user = User.model_validate(
    {'name': 'John', 'role': 'admin'},
    context={'strict': True}
)
```

## Serialization

Pydantic provides two primary approaches for converting models to other formats ([Pydantic Serialization][5]):

### Core Serialization Methods

**Python Mode (`model_dump()`)**: "Pydantic models (and model-like types such as dataclasses) will be (recursively) converted to dictionaries." This method preserves Python-native types like tuples. ([Pydantic Serialization][5])

```python
user = User(id=123, name='John Doe')
print(user.model_dump())
# {'id': 123, 'name': 'John Doe'}
```

**JSON Mode (`model_dump_json()`)**: Serializes directly to JSON-encoded strings, automatically converting unsupported types. For example, tuples become lists in the output. ([Pydantic Serialization][5])

```python
print(user.model_dump_json())
# '{"id":123,"name":"John Doe"}'
```

### Custom Serializers

Pydantic supports two serializer patterns at both field and model levels ([Pydantic Serialization][5]):

**Plain Serializers**: Execute unconditionally, bypassing standard Pydantic logic. Useful for arbitrary types or custom transformations.

```python
from pydantic import field_serializer

class User(BaseModel):
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()
```

**Wrap Serializers**: Provide flexibility to run code before/after Pydantic's standard serialization via a handler parameter.

```python
from pydantic import field_serializer

class User(BaseModel):
    name: str

    @field_serializer('name', mode='wrap')
    def serialize_name(self, value, handler, _info):
        result = handler(value)
        return result.upper()
```

The decorator pattern (`@field_serializer`) applies to multiple fields, while the Annotated pattern enables reusable serializers across models. ([Pydantic Serialization][5])

### Advanced Features

**Serialization Context**: Pass context objects to serialization methods, accessible within serializer functions via `info.context`. ([Pydantic Serialization][5])

```python
user.model_dump(context={'admin': True})
```

**Field Inclusion/Exclusion**: Control output through `exclude`, `include`, `exclude_none`, and `exclude_unset` parameters. ([Pydantic Serialization][5])

```python
user.model_dump(exclude={'password'})
user.model_dump(exclude_none=True)
user.model_dump(exclude_unset=True)
```

**Duck Typing**: Use `SerializeAsAny` annotation or `serialize_as_any` runtime parameter to include subclass fields in output. ([Pydantic Serialization][5])

## JSON Schema

Pydantic provides two main methods for JSON schema generation ([Pydantic JSON Schema][6]):

### Core Functions

- **`BaseModel.model_json_schema()`** - Returns a jsonable dict representing a model's schema
- **`TypeAdapter.json_schema()`** - Returns a jsonable dict for adapted types

These differ from serialization methods (`model_dump_json`, `dump_json`), which return JSON strings rather than schema dictionaries. ([Pydantic JSON Schema][6])

```python
schema = User.model_json_schema()
print(schema)
```

### Schema Modes

The `mode` parameter supports two options ([Pydantic JSON Schema][6]):
- **`'validation'`** (default) - Generates schema for validation
- **`'serialization'`** - Generates schema for serialization output

```python
schema = User.model_json_schema(mode='serialization')
```

### Customization

**Field-Level Options** ([Pydantic JSON Schema][6]):
- `title`, `description`, `examples` parameters in `Field()`
- `json_schema_extra` for adding custom properties
- `field_title_generator` for programmatic title generation

```python
class User(BaseModel):
    name: str = Field(
        title='Full Name',
        description='User full name',
        examples=['John Doe', 'Jane Smith']
    )
```

**Model-Level Options** via `ConfigDict` ([Pydantic JSON Schema][6]):
- `title` - Model name
- `json_schema_extra` - Additional schema properties
- `field_title_generator` and `model_title_generator`

```python
class User(BaseModel):
    model_config = ConfigDict(
        title='UserModel',
        json_schema_extra={'examples': [{'id': 1, 'name': 'John'}]}
    )
```

### Advanced Customization Tools

**`WithJsonSchema` annotation**: "preferred over implementing `__get_pydantic_json_schema__` for custom types" ([Pydantic JSON Schema][6])

**`SkipJsonSchema` annotation**: Excludes fields from generated schema ([Pydantic JSON Schema][6])

**Custom `GenerateJsonSchema` subclass**: Overrides the entire generation process ([Pydantic JSON Schema][6])

### Compliance Standards

The generated schemas conform to ([Pydantic JSON Schema][6]):
- JSON Schema Draft 2020-12
- OpenAPI Specification v3.1.0

Custom `$ref` templates can be specified via `ref_template` parameter for frameworks like OpenAPI.

## Performance

### Performance Characteristics

The validation engine is built on `pydantic-core`, implemented in Rust. According to the documentation, "Pydantic is among the fastest data validation libraries for Python." ([Why Pydantic][7]) A performance example demonstrated Pydantic was 3.45x faster than dedicated Python code when parsing JSON and validating URLs. ([Why Pydantic][7])

### Optimization Tips

**JSON Validation Method**: Use `model_validate_json()` instead of `model_validate(json.loads(...))`. The former validates directly during JSON parsing, while the latter creates intermediate Python objects unnecessarily. ([Pydantic Performance][8])

```python
# Faster
user = User.model_validate_json(json_string)

# Slower
import json
user = User.model_validate(json.loads(json_string))
```

**TypeAdapter Instantiation**: "instantiate it once, and reuse it" rather than creating new TypeAdapter instances repeatedly within functions. Each instantiation constructs new validators and serializers. ([Pydantic Performance][8])

**Type Specificity**: Replace generic abstract types with concrete ones for better performance ([Pydantic Performance][8]):
- Use `list` or `tuple` instead of `Sequence`
- Use `dict` instead of `Mapping`

**Validation Avoidance**: When validation isn't needed, use `Any` type annotation to bypass validation overhead entirely. ([Pydantic Performance][8])

**Union Handling**: Discriminated (tagged) unions outperform regular unions by using a discriminator field to identify types without trying multiple validation paths. ([Pydantic Performance][8])

```python
from typing import Literal, Union
from pydantic import BaseModel, Field

class Cat(BaseModel):
    type: Literal['cat']
    meow: str

class Dog(BaseModel):
    type: Literal['dog']
    bark: str

Animal = Annotated[Union[Cat, Dog], Field(discriminator='type')]
```

**TypedDict vs Nested Models**: "TypedDict is about ~2.5x faster than nested models" according to benchmark results. ([Pydantic Performance][8])

**Validator Selection**: Wrap validators should be avoided when performance is critical, as they materialize data in Python during validation, adding overhead. ([Pydantic Performance][8])

**Early Failure Strategy**: The `FailFast` annotation (v2.8+) allows sequence validation to stop on first error, trading comprehensive error reporting for speed gains. ([Pydantic Performance][8])

## Best Practices

### Model Organization

**Separate Concerns**: Create focused models for specific purposes:

```python
class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
```

**Use Model Inheritance**:

```python
class BaseUser(BaseModel):
    email: str

class User(BaseUser):
    id: int
    created_at: datetime
```

### Validation Strategies

**Prefer After Validators**: Safer than before validators as they work with validated data.

**Use Discriminated Unions**: For performance and clarity when handling multiple types.

**Leverage Context**: Pass validation context for environment-specific rules.

### Configuration Management

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False

    model_config = ConfigDict(env_file='.env')
```

### Error Handling

```python
from pydantic import ValidationError

try:
    user = User(**data)
except ValidationError as e:
    print(e.errors())  # List of error dictionaries
    print(e.json())     # JSON representation
```

## Common Workflows

### Basic Validation

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str

# Valid data
user = User(id=1, name='John', email='[email protected]')

# Invalid data
try:
    User(id='invalid', name='John', email='invalid')
except ValidationError as e:
    print(e)
```

### API Integration (with FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Configuration Loading

```python
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    app_name: str = "My App"
    database_url: str

    model_config = ConfigDict(env_file='.env')

config = Config()
```

### Data Transformation

```python
class UserInput(BaseModel):
    name: str
    age: str  # Receives as string

    @field_validator('age', mode='before')
    @classmethod
    def parse_age(cls, v):
        return int(v)

class UserOutput(BaseModel):
    name: str
    age: int

    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
```

## Integration with Other Tools

### With FastAPI

FastAPI uses Pydantic models for request/response validation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

@app.post("/users/", response_model=User)
async def create_user(user: User):
    return user
```

### With SQLAlchemy

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class UserSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

# Convert SQLAlchemy model to Pydantic
user_db = UserDB(id=1, name='John')
user_schema = UserSchema.model_validate(user_db)
```

### With mypy

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

# mypy will check types
user: User = User(id=1, name='John')
reveal_type(user.id)  # Revealed type is 'int'
```

### With Pydantic Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
```

## Troubleshooting

### Common Issues

**"Field required" errors**:
- Ensure all required fields are provided
- Use `| None = None` for optional fields
- Check field names match input data

**Type coercion not working**:
- Disable strict mode if enabled
- Check if using `Field(strict=True)`
- Verify input type is coercible

**Validation errors with nested models**:
- Ensure nested model structure matches input
- Check for circular references
- Use `model_config = ConfigDict(arbitrary_types_allowed=True)` for custom types

**JSON serialization errors**:
- Use `model_dump_json()` instead of `json.dumps(model.model_dump())`
- Implement custom serializers for non-JSON types
- Check for datetime/UUID serialization issues

### Debugging

**Inspect model schema**:
```python
print(User.model_json_schema())
```

**Check field information**:
```python
print(User.model_fields)
```

**Validate with detailed errors**:
```python
try:
    User(**data)
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc']}")
        print(f"Error: {error['msg']}")
        print(f"Type: {error['type']}")
```

**Use validation context for debugging**:
```python
User.model_validate(data, context={'debug': True})
```

## Comparison with Alternatives

### vs Dataclasses

**Pydantic Advantages**:
- Runtime validation
- Type coercion
- JSON Schema generation
- Custom validators

**Dataclasses Advantages**:
- Standard library (no dependencies)
- Simpler for basic use cases
- Better performance when validation not needed

### vs Marshmallow

**Pydantic Advantages**:
- Type hint-based (more Pythonic)
- Better performance
- Simpler syntax

**Marshmallow Advantages**:
- More explicit serialization control
- Richer ecosystem of extensions

### vs attrs

**Pydantic Advantages**:
- Runtime validation
- JSON Schema support
- Better API integration

**attrs Advantages**:
- More flexible initialization
- Smaller overhead

## Learning Path

**1. Basics**:
- Model definition
- Field types
- Basic validation

**2. Intermediate**:
- Custom validators
- Field configuration
- Serialization

**3. Advanced**:
- Performance optimization
- Complex validators
- Custom types
- JSON Schema customization

**4. Integration**:
- FastAPI integration
- Database ORMs
- Settings management
- Testing strategies

## Resources

### Official Resources

- Documentation: https://docs.pydantic.dev/
- GitHub Repository: https://github.com/pydantic/pydantic
- PyPI: https://pypi.org/project/pydantic/
- Changelog: https://docs.pydantic.dev/latest/changelog/

### Community

- GitHub Discussions: Q&A and feature requests
- Stack Overflow: `pydantic` tag
- Discord: Pydantic community server

### Related Tools

- pydantic-settings: Settings management
- pydantic-extra-types: Additional field types
- FastAPI: Web framework using Pydantic
- SQLModel: SQL databases with Pydantic models

## References

[1]: https://docs.pydantic.dev/latest/ "Pydantic Documentation"
[2]: https://docs.pydantic.dev/latest/concepts/models/ "Pydantic Models"
[3]: https://docs.pydantic.dev/latest/concepts/fields/ "Pydantic Fields"
[4]: https://docs.pydantic.dev/latest/concepts/validators/ "Pydantic Validators"
[5]: https://docs.pydantic.dev/latest/concepts/serialization/ "Pydantic Serialization"
[6]: https://docs.pydantic.dev/latest/concepts/json_schema/ "Pydantic JSON Schema"
[7]: https://docs.pydantic.dev/latest/why/ "Why Pydantic"
[8]: https://docs.pydantic.dev/latest/concepts/performance/ "Pydantic Performance"
