---
title: "FastAPI: Modern Python Web Framework"
description: "High-performance web framework for building APIs with Python type hints"
type: "framework-guide"
tags: ["fastapi", "python", "api", "rest", "async", "pydantic", "starlette", "openapi", "web-framework"]
category: "python"
subcategory: "web-frameworks"
version: "0.115"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "FastAPI Official Documentation"
    url: "https://fastapi.tiangolo.com/"
  - name: "FastAPI Tutorial"
    url: "https://fastapi.tiangolo.com/tutorial/"
  - name: "FastAPI First Steps"
    url: "https://fastapi.tiangolo.com/tutorial/first-steps/"
  - name: "FastAPI Path Parameters"
    url: "https://fastapi.tiangolo.com/tutorial/path-params/"
  - name: "FastAPI Query Parameters"
    url: "https://fastapi.tiangolo.com/tutorial/query-params/"
  - name: "FastAPI Request Body"
    url: "https://fastapi.tiangolo.com/tutorial/body/"
  - name: "FastAPI Dependencies"
    url: "https://fastapi.tiangolo.com/tutorial/dependencies/"
  - name: "FastAPI Security"
    url: "https://fastapi.tiangolo.com/tutorial/security/"
  - name: "FastAPI Deployment"
    url: "https://fastapi.tiangolo.com/deployment/"
  - name: "FastAPI Advanced Features"
    url: "https://fastapi.tiangolo.com/advanced/"
related: ["../pydantic/pydantic-library-guide.md"]
author: "unknown"
contributors: []
---

# FastAPI: Modern Python Web Framework

FastAPI is a contemporary web framework for constructing APIs using Python. It leverages standard Python type hints and is built on Starlette (for web functionality) and Pydantic (for data validation). ([FastAPI Documentation][1])

## Overview

FastAPI ranks among the fastest Python frameworks available, comparable to NodeJS and Go. ([FastAPI Documentation][1]) The framework automatically handles data validation, type conversion, and interactive documentation generation, enabling rapid development with strong type safety.

### Key Features

FastAPI provides several distinguishing capabilities:

- **High Performance**: Comparable to NodeJS and Go, ranking among the fastest Python frameworks available
- **Rapid Development**: Estimated 200-300% increase in feature development speed
- **Error Reduction**: Approximately 40% reduction in developer-induced bugs
- **Strong Editor Integration**: Full autocompletion and type-checking support
- **Automatic Documentation**: Self-generating interactive API documentation via Swagger UI and ReDoc
- **Standards Compliance**: Built on OpenAPI and JSON Schema standards

([FastAPI Documentation][1])

### Performance Characteristics

TechEmpower independent benchmarks position FastAPI applications as "one of the fastest Python frameworks available," surpassed only by Starlette and Uvicorn (which FastAPI uses internally). ([FastAPI Documentation][1])

### Core Capabilities

The framework automatically handles:
- Data validation from multiple sources (JSON, path parameters, query strings, cookies, headers, forms, files)
- Type conversion between network and Python data
- Interactive documentation generation
- Error messaging for invalid data

([FastAPI Documentation][1])

## Installation

### Basic Installation

```bash
pip install "fastapi[standard]"
```

This includes default optional dependencies like `fastapi-cloud-cli` for deployment capabilities. ([FastAPI Tutorial][2])

### Using uv

```bash
# Add to project
uv add "fastapi[standard]"

# Or install globally
uv tool install fastapi-cli
```

### Minimal Installation

For production with custom dependencies:

```bash
pip install fastapi
pip install uvicorn[standard]
```

## Getting Started

### Creating a Basic API

The simplest FastAPI application requires minimal code ([FastAPI First Steps][3]):

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Save this as `main.py`.

### Running the Application

Execute the development server using ([FastAPI First Steps][3]):

```bash
fastapi dev main.py
```

The server launches at `http://127.0.0.1:8000`. As the documentation notes, "Running in development mode, for production use: **fastapi run**". ([FastAPI First Steps][3])

### Interactive Documentation

FastAPI automatically generates two documentation interfaces ([FastAPI First Steps][3]):

- **Swagger UI**: Available at `/docs` - provides an interactive interface for testing endpoints
- **ReDoc**: Available at `/redoc` - offers an alternative documentation view

### OpenAPI Schema

FastAPI automatically generates an OpenAPI schema accessible at `/openapi.json`. This schema enables automatic documentation generation and supports client code generation for frontend and mobile applications. ([FastAPI First Steps][3])

## Core Concepts

### Path Operation Decorator

The `@app.get("/")` syntax tells FastAPI which HTTP method and URL path the function handles. This decorator pattern works with other methods like `@app.post()`, `@app.put()`, and `@app.delete()`. ([FastAPI First Steps][3])

### Path Operation Function

The decorated function processes requests and returns data. Functions can be asynchronous (`async def`) or standard Python functions. ([FastAPI First Steps][3])

### Type Hints

FastAPI leverages standard Python type hints to provide:
- Automatic data validation
- Type conversion
- Editor autocompletion
- API documentation generation

## Path Parameters

Path Parameters are variables declared in URL routes using Python format string syntax. FastAPI automatically extracts these values and passes them to your function. ([FastAPI Path Parameters][4])

### Basic Declaration

```python
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

([FastAPI Path Parameters][4])

### Type Annotations & Auto-Conversion

When you declare parameter types using Python annotations, FastAPI automatically converts incoming data. As the documentation states: "with that type declaration, **FastAPI** gives you automatic request 'parsing.'" ([FastAPI Path Parameters][4])

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Data Validation

Type declarations trigger automatic validation. For example, declaring `item_id: int` will reject non-integer values with descriptive error messages. ([FastAPI Path Parameters][4])

### Automatic Documentation

The same type declarations generate interactive API documentation in Swagger UI and ReDoc without additional effort. ([FastAPI Path Parameters][4])

### Order Matters

Path operations are evaluated sequentially. Fixed routes like `/users/me` must be declared before parameterized routes like `/users/{user_id}` to prevent the parameter from matching. ([FastAPI Path Parameters][4])

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

### Enumeration Support

Use Python `Enum` classes to restrict path parameters to predefined values. The documentation explains you should "inherit from `str` and from `Enum`" so the API can properly recognize string values. ([FastAPI Path Parameters][4])

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}
```

### Path-Within-Path

Use the `:path` converter syntax to capture entire file paths within a parameter ([FastAPI Path Parameters][4]):

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

## Query Parameters

Query parameters are key-value pairs appearing after the `?` in URLs, separated by `&` characters. In FastAPI, function parameters not in the path are automatically treated as query parameters. ([FastAPI Query Parameters][5])

### Basic Usage

```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

([FastAPI Query Parameters][5])

### Type Conversion & Validation

FastAPI automatically converts query parameters to declared Python types and validates them. As noted in the documentation: "All the same process that applied for path parameters also applies for query parameters." ([FastAPI Query Parameters][5])

### Default Values

Query parameters can have defaults, making them optional. Example: `skip: int = 0` defaults to 0 if not provided in the URL. ([FastAPI Query Parameters][5])

### Optional Parameters

Set defaults to `None` for truly optional parameters ([FastAPI Query Parameters][5]):

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Boolean Conversion

Boolean parameters accept multiple formats: `1`, `true`, `True`, `yes`, `on` all convert to `True`. ([FastAPI Query Parameters][5])

### Required Parameters

Omitting a default value makes a query parameter required. The framework returns a validation error with details like: `"type": "missing", "msg": "Field required"` when required parameters are absent. ([FastAPI Query Parameters][5])

### Multiple Parameters

You can mix required parameters, optional parameters with defaults, and optional parameters set to `None` in the same endpoint without declaring them in any specific order. ([FastAPI Query Parameters][5])

## Request Bodies

A request body is data sent from the client to your API. FastAPI uses **Pydantic models** to handle this data with automatic validation and type checking. ([FastAPI Request Body][6])

### Creating a Data Model

Define a class inheriting from `BaseModel` with typed attributes ([FastAPI Request Body][6]):

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

- Required fields have no default value
- Optional fields use `None` as default
- Standard Python type hints apply

### Automatic Features

FastAPI delivers several benefits with minimal code ([FastAPI Request Body][6]):

- **Type validation** and conversion
- **Editor autocomplete support** for model attributes
- **Interactive API documentation** (Swagger UI, ReDoc)
- **Clear error messages** pinpointing validation failures

### Parameter Recognition

When combining multiple parameter types, FastAPI distinguishes them by ([FastAPI Request Body][6]):
- Path parameters matching route variables
- Singular types (`int`, `str`, etc.) as query parameters
- Pydantic models as request bodies

### HTTP Methods for Request Bodies

Use `POST`, `PUT`, `DELETE`, or `PATCH` for request bodies. While FastAPI supports `GET` with bodies, this violates REST conventions and lacks universal tooling support. ([FastAPI Request Body][6])

### Using the Request Body

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

## Dependency Injection

According to the FastAPI documentation, **"Dependency Injection" means, in programming, that there is a way for your code to declare things that it requires to work and use: "dependencies".** ([FastAPI Dependencies][7])

The framework then automatically handles providing these needed dependencies to your functions, minimizing code repetition.

### How Dependencies Work

Dependencies in FastAPI are regular functions that can accept the same parameters as path operation functions. When a request arrives, FastAPI ([FastAPI Dependencies][7]):

1. Calls the dependency function with correct parameters
2. Retrieves the result
3. Assigns that result to the path operation function parameter

### Declaring Dependencies

You declare dependencies using the `Depends()` function within your path operation parameters ([FastAPI Dependencies][7]):

```python
from fastapi import Depends, FastAPI
from typing import Annotated

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

### Key Use Cases

Dependencies help with ([FastAPI Dependencies][7]):
- Shared logic across endpoints
- Database connection management
- Security and authentication enforcement
- Role-based requirements
- Reducing code duplication

### Advanced Features

FastAPI supports hierarchical dependencies (dependencies that depend on other dependencies), all integrated automatically into OpenAPI documentation for interactive API docs. ([FastAPI Dependencies][7])

## Security

FastAPI addresses a critical development challenge: **security implementation typically comprises 50% or more of application code** in many frameworks. FastAPI simplifies this with built-in tools. ([FastAPI Security][8])

### Authentication Standards Supported

**OAuth2** is a primary specification that enables authentication through multiple methods, including third-party providers like Google and GitHub. The framework also supports **OpenID Connect**, which extends OAuth2 with standardized specifications for improved interoperability. ([FastAPI Security][8])

### OpenAPI Security Schemes

FastAPI leverages OpenAPI standards, implementing three primary security categories ([FastAPI Security][8]):

- **apiKey**: Application-specific keys via query parameter, header, or cookie
- **http**: Standard HTTP authentication including Bearer tokens and Basic auth
- **oauth2**: Multiple flows, with the "password" flow suitable for same-application authentication

### Built-in Tools

According to the documentation: "FastAPI provides several tools for each of these security schemes in the `fastapi.security` module that simplify using these security mechanisms." ([FastAPI Security][8]) These utilities integrate automatically with interactive API documentation.

### Example: OAuth2 with Password Flow

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Advanced Features

The Advanced User Guide covers additional features beyond the core tutorial. ([FastAPI Advanced][10])

### Middleware & CORS

Configure Cross-Origin Resource Sharing (CORS) and custom middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Background Tasks

Execute tasks after returning a response:

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"notification sent to {email}")
    return {"message": "Notification sent"}
```

### WebSockets

Full WebSocket support for real-time communication:

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### Custom Responses

Return HTML, streaming, files, or custom response types:

```python
from fastapi.responses import HTMLResponse

@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return "<html><body><h1>Hello World</h1></body></html>"
```

## Deployment

Deploying an application involves making it "available to the users" by placing it on a remote machine with proper server infrastructure. ([FastAPI Deployment][9])

### Development vs Production

**Development mode:**
```bash
fastapi dev main.py
```

**Production mode:**
```bash
fastapi run main.py
```

([FastAPI First Steps][3])

### Production Server Options

**Uvicorn** (ASGI server):
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Gunicorn with Uvicorn workers**:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

Basic Dockerfile for FastAPI:

```dockerfile
FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

### Cloud Deployment

FastAPI deployment section provides guidance on ([FastAPI Deployment][9]):
- HTTPS configuration
- Manual server operation
- Cloud provider options
- Worker configuration with Uvicorn
- Docker containerization

## Testing

FastAPI is built for easy testing using Python's standard testing tools.

### Basic Testing

```python
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

### Testing with Dependencies

Override dependencies for testing:

```python
from fastapi import Depends

def override_dependency():
    return {"override": True}

app.dependency_overrides[original_dependency] = override_dependency
```

### Async Testing

For async tests, use `pytest-asyncio`:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

## Best Practices

### Project Structure

Organize larger projects using routers:

```
app/
├── __init__.py
├── main.py
├── dependencies.py
├── routers/
│   ├── __init__.py
│   ├── items.py
│   └── users.py
└── models/
    ├── __init__.py
    ├── item.py
    └── user.py
```

### Using Routers

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/items/")
async def read_items():
    return [{"name": "Item 1"}]

# In main.py
from .routers import items

app.include_router(items.router)
```

### Configuration Management

Use environment variables and settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### Error Handling

Implement custom exception handlers:

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )
```

### Database Integration

Use SQLAlchemy or other ORMs with dependencies:

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Response Models

Use response models for data validation and documentation:

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    # Save item to database
    return item
```

### Status Codes

Use explicit status codes:

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

## Performance Optimization

### Async/Await

Use async functions for I/O-bound operations:

```python
import httpx

@app.get("/external-data/")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()
```

### Connection Pooling

Use connection pools for databases and external services to reduce overhead.

### Caching

Implement caching for expensive operations:

```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()
```

### Response Compression

Enable gzip compression:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## Common Workflows

### Development Workflow

```bash
# Create project
mkdir my-api
cd my-api

# Initialize with uv
uv init
uv add "fastapi[standard]"

# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

# Run development server
fastapi dev main.py
```

### Testing Workflow

```bash
# Add testing dependencies
uv add --dev pytest httpx

# Create tests
mkdir tests
cat > tests/test_main.py << 'EOF'
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
EOF

# Run tests
pytest
```

### Deployment Workflow

```bash
# Build Docker image
docker build -t my-api .

# Run container
docker run -d --name my-api -p 80:80 my-api

# Or deploy to cloud
fastapi-cloud deploy
```

## Integration with Other Tools

### With uv

```bash
uv add "fastapi[standard]"
uv run fastapi dev main.py
```

### With Ruff

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "FAST"]
```

### With mypy

```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
follow_imports = "normal"
strict_optional = true
```

### With SQLAlchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### With Alembic (Migrations)

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### Common Issues

**"422 Unprocessable Entity":**
- Validation error - check request body matches Pydantic model
- Verify query parameter types match declarations
- Use `/docs` to see expected schema

**"Module not found" errors:**
- Check import paths in multi-file projects
- Ensure `__init__.py` files exist in packages
- Verify relative imports use correct syntax

**Async/Sync mixing:**
- Use `async def` for I/O-bound operations
- Use regular `def` for CPU-bound operations
- Don't mix blocking and non-blocking code without proper handling

**CORS errors:**
- Add CORSMiddleware with appropriate origins
- Verify allowed methods and headers
- Check browser console for specific CORS errors

### Debugging

**Enable debug logging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

**Use FastAPI's exception handlers:**
```python
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()},
    )
```

**Test endpoints interactively:**
- Use `/docs` for Swagger UI
- Use `/redoc` for ReDoc
- Check `/openapi.json` for schema validation

## Resources

### Official Resources

- Documentation: https://fastapi.tiangolo.com/
- GitHub Repository: https://github.com/tiangolo/fastapi
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Advanced Guide: https://fastapi.tiangolo.com/advanced/

### Community

- Discord: FastAPI community server
- GitHub Discussions: Q&A and feature requests
- Stack Overflow: `fastapi` tag

### Related Tools

- Starlette: https://www.starlette.io/
- Pydantic: https://docs.pydantic.dev/
- Uvicorn: https://www.uvicorn.org/
- SQLAlchemy: https://www.sqlalchemy.org/

## Comparison with Other Frameworks

### vs Flask

**FastAPI Advantages:**
- Automatic data validation
- Built-in async support
- Auto-generated documentation
- Type safety with Python hints

**Flask Advantages:**
- Simpler for basic applications
- More mature ecosystem
- Greater flexibility in structure

### vs Django REST Framework

**FastAPI Advantages:**
- Better performance
- Simpler codebase
- Modern async support
- Faster development

**Django REST Framework Advantages:**
- Full-featured admin interface
- Built-in ORM
- More comprehensive authentication

### vs Express.js (Node.js)

**FastAPI Advantages:**
- Python ecosystem
- Type safety built-in
- Automatic validation

**Express.js Advantages:**
- JavaScript ecosystem
- More middleware options
- Larger community

## Learning Path

**1. Basics** (Tutorial sections):
- First steps
- Path and query parameters
- Request body with Pydantic models

**2. Intermediate** (Tutorial sections):
- Dependencies
- Security and authentication
- Database integration

**3. Advanced** (Advanced Guide):
- Custom middleware
- WebSockets
- Background tasks
- Testing strategies

**4. Production** (Deployment):
- Docker containerization
- Cloud deployment
- Monitoring and logging
- Performance optimization

## References

[1]: https://fastapi.tiangolo.com/ "FastAPI Official Documentation"
[2]: https://fastapi.tiangolo.com/tutorial/ "FastAPI Tutorial"
[3]: https://fastapi.tiangolo.com/tutorial/first-steps/ "FastAPI First Steps"
[4]: https://fastapi.tiangolo.com/tutorial/path-params/ "FastAPI Path Parameters"
[5]: https://fastapi.tiangolo.com/tutorial/query-params/ "FastAPI Query Parameters"
[6]: https://fastapi.tiangolo.com/tutorial/body/ "FastAPI Request Body"
[7]: https://fastapi.tiangolo.com/tutorial/dependencies/ "FastAPI Dependencies"
[8]: https://fastapi.tiangolo.com/tutorial/security/ "FastAPI Security"
[9]: https://fastapi.tiangolo.com/deployment/ "FastAPI Deployment"
[10]: https://fastapi.tiangolo.com/advanced/ "FastAPI Advanced Features"
