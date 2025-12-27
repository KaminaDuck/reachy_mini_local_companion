---
author: unknown
category: ai-frameworks
contributors: []
description: Complete guide to implementing A2A Protocol servers with Pydantic AI
  and FastA2A
last_updated: '2025-08-16'
related:
- agents.md
- pydantic-ai-links.md
sources:
- name: Pydantic AI A2A Documentation
  url: https://ai.pydantic.dev/a2a/
- name: FastA2A API Reference
  url: https://ai.pydantic.dev/api/fasta2a/
- name: FastA2A GitHub Repository
  url: https://github.com/pydantic/fasta2a
- name: FastA2A PyPI Package
  url: https://pypi.org/project/fasta2a/
- name: Pydantic AI Documentation
  url: https://ai.pydantic.dev/
status: stable
subcategory: agent-frameworks
tags:
- pydantic-ai
- a2a
- agent2agent
- fasta2a
- protocol
- agents
- interoperability
- asgi
- starlette
title: Pydantic AI A2A Integration
type: integration-guide
version: 0.2.3
---

# Pydantic AI A2A Integration

Complete guide to implementing A2A (Agent2Agent) Protocol servers using Pydantic AI and the FastA2A library, enabling agent interoperability and cross-framework communication.

## Overview

FastA2A is a framework-agnostic Python implementation of the A2A Protocol that enables AI agents to communicate and collaborate across different platforms and frameworks. ([FastA2A GitHub][3]) The library was originally part of Pydantic AI but was separated to support broader ecosystem adoption. ([FastA2A GitHub][3])

### What is A2A?

The Agent2Agent (A2A) Protocol is an open standard introduced by Google that enables communication and interoperability between AI agents, regardless of the framework or vendor they are built on. ([Pydantic AI A2A Docs][1])

### Why FastA2A?

FastA2A provides a structured approach to exposing agentic functionality through a standardized protocol. ([FastA2A GitHub][3]) Key benefits include:

- **Framework agnostic** - Works with any agentic framework, not just Pydantic AI
- **Production ready** - Built on Starlette for ASGI compatibility
- **Flexible architecture** - Bring your own Storage, Broker, and Worker implementations
- **Type safe** - Leverages Pydantic for validation and type safety
- **Observable** - Integrated OpenTelemetry support

## Installation

### Basic Installation

```bash
pip install fasta2a
```

Or using uv:
```bash
uv add fasta2a
```

([FastA2A PyPI][4])

### With Pydantic AI

```bash
pip install 'pydantic-ai-slim[a2a]'
```

([Pydantic AI A2A Docs][1])

### Dependencies

FastA2A requires:
- **Starlette** - ASGI framework for HTTP server
- **Pydantic** - Data validation and serialization
- **OpenTelemetry API** - Distributed tracing support

([FastA2A GitHub][3])

## Quick Start with Pydantic AI

The simplest way to expose a Pydantic AI agent as an A2A server: ([Pydantic AI A2A Docs][1])

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5', instructions='Be fun!')
app = agent.to_a2a()
```

Deploy with any ASGI server:
```bash
uvicorn agent_to_a2a:app --host 0.0.0.0 --port 8000
```

This automatically:
- Creates an A2A-compliant server
- Configures Agent Card at `/.well-known/agent.json`
- Handles message routing and task lifecycle
- Persists conversation history
- Converts agent outputs to A2A artifacts

## Core Architecture

FastA2A is built around three essential components: ([FastA2A API Reference][2])

### 1. Storage

Persists both A2A-formatted tasks and agent-specific context. ([FastA2A API Reference][2])

**Dual Purpose:**
- **Protocol compliance** - Stores tasks in A2A format for client access
- **Agent optimization** - Stores rich internal state (tool calls, reasoning traces)

**Interface:**
```python
from fasta2a import Storage

class Storage(Generic[ContextT], ABC):
    async def load_task(
        self,
        task_id: str,
        history_length: int | None = None
    ) -> Task | None:
        """Retrieve task by ID with optional history limit"""

    async def submit_task(
        self,
        context_id: str,
        message: Message
    ) -> Task:
        """Create new task from incoming message"""

    async def update_task(
        self,
        task_id: str,
        state: TaskState,
        new_artifacts: list[Artifact] | None = None,
        new_messages: list[Message] | None = None
    ) -> Task:
        """Update task state and append artifacts/messages"""

    async def load_context(
        self,
        context_id: str
    ) -> ContextT | None:
        """Load agent-specific context by ID"""

    async def update_context(
        self,
        context_id: str,
        context: ContextT
    ) -> None:
        """Persist updated context"""
```

([FastA2A API Reference][2])

**Built-in Implementation:**
```python
from fasta2a.storage import InMemoryStorage

storage = InMemoryStorage()
```

### 2. Broker

Manages task queuing and scheduling, coordinating between the HTTP server and worker execution. ([FastA2A API Reference][2])

**Interface:**
```python
from fasta2a import Broker

class Broker(ABC):
    async def run_task(self, params: TaskSendParams) -> None:
        """Queue task for execution"""

    async def cancel_task(self, params: TaskIdParams) -> None:
        """Request task cancellation"""

    async def receive_task_operations(self) -> AsyncIterator[TaskOperation]:
        """Receive commands from server (for workers)"""

    async def __aenter__(self):
        """Start broker"""

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Shutdown broker"""
```

([FastA2A API Reference][2])

**Built-in Implementation:**
```python
from fasta2a.broker import InMemoryBroker

broker = InMemoryBroker()
```

**Key Characteristics:**
- Enables worker separation - workers can "live outside the web server" on separate machines or processes ([FastA2A GitHub][3])
- Supports both in-process and distributed task execution
- Maintains connections between Storage and Worker

### 3. Worker

Executes tasks using the specific agentic framework implementation. ([FastA2A API Reference][2])

**Interface:**
```python
from fasta2a import Worker

class Worker(Generic[ContextT], ABC):
    def __init__(self, storage: Storage[ContextT], broker: Broker):
        self.storage = storage
        self.broker = broker

    async def run(self) -> AsyncIterator[None]:
        """Start worker loop accepting task operations"""
        async for operation in self.broker.receive_task_operations():
            match operation['kind']:
                case 'run':
                    await self.run_task(operation['params'])
                case 'cancel':
                    await self.cancel_task(operation['params'])

    async def run_task(self, params: TaskSendParams) -> None:
        """Execute task - implement in subclass"""

    async def cancel_task(self, params: TaskIdParams) -> None:
        """Cancel task - implement in subclass"""

    def build_message_history(
        self,
        history: list[Message]
    ) -> list[Any]:
        """Convert A2A messages to framework-specific format"""

    def build_artifacts(self, result: Any) -> list[Artifact]:
        """Convert agent results to A2A artifacts"""
```

([FastA2A API Reference][2])

## Core Concepts

### Tasks

A task represents one complete execution of an agent. ([Pydantic AI A2A Docs][1])

**Lifecycle:**
1. Client sends message to agent
2. New task created with state `"submitted"`
3. Agent executes until completion or failure
4. Final outputs stored as task artifacts
5. Task transitions to terminal state (`"completed"`, `"failed"`, `"rejected"`, `"canceled"`)

**Task Structure:**
```python
from fasta2a import Task

task = {
    'id': 'task_123',              # Unique identifier
    'context_id': 'ctx_abc',       # Associated conversation
    'kind': 'task',                # Type marker
    'status': {
        'state': 'completed',      # Current state
        'message': None,           # Optional status message
        'timestamp': '2025-05-01T12:00:00Z'
    },
    'history': [...],              # Message log
    'artifacts': [...],            # Generated results
    'metadata': {}                 # Extension data
}
```

([FastA2A API Reference][2])

**Task States:**
- `"submitted"` - Task accepted, queued for execution
- `"working"` - Task actively executing
- `"input-required"` - Awaiting additional user input
- `"auth-required"` - Requires external authentication
- `"completed"` - Successfully finished
- `"canceled"` - Canceled by client request
- `"failed"` - Failed due to error
- `"rejected"` - Rejected by agent (invalid request, etc.)
- `"unknown"` - Unrecognized state

([FastA2A API Reference][2])

### Contexts

A context represents a conversation thread that can span multiple tasks. ([Pydantic AI A2A Docs][1])

**Context ID Behavior:**
- **New messages without `context_id`** - Generate new context ID, start fresh conversation
- **Messages with existing `context_id`** - Continue conversation with full message history

**Example Flow:**
```python
# First message - new context
response1 = client.send_message({
    'role': 'user',
    'parts': [{'kind': 'text', 'text': 'Hello'}]
})
# Returns task with new context_id: 'ctx_abc'

# Follow-up message - same context
response2 = client.send_message({
    'role': 'user',
    'parts': [{'kind': 'text', 'text': 'What is 2+2?'}],
    'context_id': 'ctx_abc'  # Maintains conversation
})
# Agent has access to full history including "Hello" message
```

## FastA2A Server Creation

### Basic Server with Custom Components

```python
from fasta2a import FastA2A
from fasta2a.broker import InMemoryBroker
from fasta2a.storage import InMemoryStorage

# Initialize components
storage = InMemoryStorage()
broker = InMemoryBroker()

# Create A2A server
app = FastA2A(
    storage=storage,
    broker=broker,
    name='Recipe Agent',
    url='http://localhost:8000',
    version='1.0.0',
    description='AI agent for recipe recommendations',
    debug=True
)
```

([FastA2A API Reference][2])

### Full Configuration

```python
from fasta2a import FastA2A, Skill, AgentProvider

app = FastA2A(
    storage=storage,
    broker=broker,

    # Agent metadata
    name='Recipe Agent',
    url='https://agent.example.com',
    version='2.1.0',
    description='Multi-cuisine recipe recommendations with dietary preferences',

    # Provider information
    provider=AgentProvider(
        organization='Culinary AI Inc',
        url='https://culinary-ai.com'
    ),

    # Skills declaration
    skills=[
        Skill(
            id='recipe-search',
            name='Recipe Search',
            description='Search recipes by ingredients and cuisine',
            tags=['cooking', 'search', 'recipes'],
            examples=['Find me Italian pasta recipes', 'Recipes with chicken'],
            input_modes=['application/json'],
            output_modes=['application/json']
        ),
        Skill(
            id='nutrition-info',
            name='Nutrition Information',
            description='Analyze nutritional content of recipes',
            tags=['nutrition', 'health'],
            input_modes=['application/json'],
            output_modes=['application/json']
        )
    ],

    # Server configuration
    debug=False
)
```

([FastA2A API Reference][2])

### Constructor Parameters

**Required:**
- `storage: Storage` - Task and context persistence
- `broker: Broker` - Task scheduling and execution

**Agent Metadata:**
- `name: str | None` - Agent identifier (default: 'My Agent')
- `url: str` - Agent endpoint (default: 'http://localhost:8000')
- `version: str` - Agent version (default: '1.0.0')
- `description: str | None` - Human-readable description
- `provider: AgentProvider | None` - Organization details

**Capabilities:**
- `skills: list[Skill] | None` - Declared agent capabilities

**Server Configuration:**
- `debug: bool` - Debug mode flag (default: False)
- `routes, middleware, exception_handlers, lifespan` - Starlette ASGI configuration

([FastA2A API Reference][2])

## Agent Card Configuration

FastA2A automatically generates an Agent Card at `/.well-known/agent.json` (RFC 8615 compliant). ([FastA2A API Reference][2])

### Agent Card Structure

```json
{
  "name": "Recipe Agent",
  "description": "AI agent for recipe recommendations",
  "url": "http://localhost:8000",
  "version": "1.0.0",
  "protocol_version": "0.3.0",
  "capabilities": {
    "streaming": false,
    "push_notifications": false,
    "state_transition_history": false
  },
  "default_input_modes": ["application/json"],
  "default_output_modes": ["application/json"],
  "skills": [
    {
      "id": "recipe-search",
      "name": "Recipe Search",
      "description": "Search recipes by ingredients",
      "tags": ["cooking", "search"],
      "examples": ["Find me pasta recipes"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"]
    }
  ],
  "provider": {
    "organization": "Culinary AI Inc",
    "url": "https://culinary-ai.com"
  }
}
```

**Default Values:**
- `default_input_modes`: `['application/json']` ([FastA2A API Reference][2])
- `default_output_modes`: `['application/json']` ([FastA2A API Reference][2])

### Skills Definition

Skills represent individual agent capabilities: ([FastA2A API Reference][2])

```python
from fasta2a import Skill

skill = Skill(
    id='unique-skill-id',           # Required: Unique identifier
    name='Skill Name',               # Required: Display name
    description='What this does',   # Required: Capability explanation
    tags=['tag1', 'tag2'],           # Categorization keywords
    examples=[                       # Usage examples for discovery
        'Example prompt 1',
        'Example prompt 2'
    ],
    input_modes=['application/json'], # Accepted MIME types
    output_modes=['application/json'] # Response MIME types
)
```

## Message Handling

### Message Structure

Messages are the primary communication mechanism between clients and agents: ([FastA2A API Reference][2])

```python
from fasta2a import Message

message = {
    'role': 'user',              # 'user' or 'agent'
    'parts': [                   # Content segments
        {
            'kind': 'text',
            'text': 'Hello, agent!'
        }
    ],
    'kind': 'message',           # Event classifier
    'message_id': 'msg_123',     # Unique identifier
    'context_id': 'ctx_abc',     # Conversation context
    'task_id': 'task_456',       # Associated task
    'reference_task_ids': [],    # Related tasks
    'metadata': {},              # Custom data
    'extensions': []             # Protocol extensions
}
```

### Part Types

**Text Part:**
```python
{
    'kind': 'text',
    'text': 'Message content here'
}
```

**File Part (Bytes):**
```python
{
    'kind': 'file',
    'file': {
        'bytes': 'base64-encoded-content',
        'mime_type': 'application/pdf'
    }
}
```

**File Part (URI):**
```python
{
    'kind': 'file',
    'file': {
        'uri': 'https://example.com/file.pdf',
        'mime_type': 'application/pdf'
    }
}
```

**Data Part:**
```python
{
    'kind': 'data',
    'data': {
        'key': 'value',
        'nested': {'field': 123}
    }
}
```

([FastA2A API Reference][2])

## Artifact Generation

Artifacts are agent-generated outputs composed of multiple parts: ([FastA2A API Reference][2])

```python
from fasta2a import Artifact

artifact = {
    'artifact_id': 'art_789',       # Unique reference
    'name': 'Analysis Results',     # Display title
    'description': 'Summary',       # Content description
    'parts': [                      # Content segments (required)
        {
            'kind': 'text',
            'text': 'Result data'
        },
        {
            'kind': 'data',
            'data': {'score': 0.95}
        }
    ],
    'metadata': {},                 # Custom data
    'extensions': [],               # Feature flags
    'append': False,                # Accumulate vs replace
    'last_chunk': True              # Stream terminator
}
```

### Pydantic AI Artifact Conversion

Pydantic AI automatically converts agent outputs to artifacts: ([Pydantic AI A2A Docs][1])

- **String outputs** → `TextPart`
- **Structured data** (dicts, Pydantic models) → `DataPart`
- **Complete message history** → Stored including tool calls

## Worker Implementation

### Custom Worker Example

```python
from dataclasses import dataclass
from fasta2a import Worker, TaskSendParams, TaskIdParams
from fasta2a import Artifact, TextPart

@dataclass
class MyContext:
    """Agent-specific context structure"""
    user_id: str
    preferences: dict
    conversation_history: list

class MyAgentWorker(Worker[MyContext]):
    async def run_task(self, params: TaskSendParams) -> None:
        """Execute task with custom agent logic"""
        # Load context
        context = await self.storage.load_context(params['context_id'])
        if context is None:
            context = MyContext(
                user_id='default',
                preferences={},
                conversation_history=[]
            )

        # Load task
        task = await self.storage.load_task(params['id'])
        if task is None:
            return

        # Update task to working state
        await self.storage.update_task(
            params['id'],
            state='working'
        )

        try:
            # Execute agent logic
            result = await self.execute_agent(
                params['message'],
                context,
                task['history']
            )

            # Convert result to artifact
            artifacts = [
                Artifact(
                    artifact_id=f"art_{params['id']}",
                    parts=[
                        TextPart(kind='text', text=result)
                    ]
                )
            ]

            # Update task to completed
            await self.storage.update_task(
                params['id'],
                state='completed',
                new_artifacts=artifacts
            )

            # Update context
            context.conversation_history.append(params['message'])
            await self.storage.update_context(
                params['context_id'],
                context
            )

        except Exception as e:
            # Handle errors
            await self.storage.update_task(
                params['id'],
                state='failed'
            )

    async def cancel_task(self, params: TaskIdParams) -> None:
        """Handle task cancellation"""
        await self.storage.update_task(
            params['id'],
            state='canceled'
        )

    async def execute_agent(
        self,
        message: Message,
        context: MyContext,
        history: list[Message]
    ) -> str:
        """Custom agent execution logic"""
        # Implement your agent here
        return "Agent response"
```

### Running Worker

```python
import asyncio
from fasta2a.broker import InMemoryBroker
from fasta2a.storage import InMemoryStorage

async def main():
    storage = InMemoryStorage()
    broker = InMemoryBroker()

    worker = MyAgentWorker(storage=storage, broker=broker)

    # Start worker loop
    async for _ in worker.run():
        pass  # Worker processes tasks continuously

if __name__ == '__main__':
    asyncio.run(main())
```

## Pydantic AI Integration Details

### Automatic Conversion

When using `agent.to_a2a()`, Pydantic AI handles: ([Pydantic AI A2A Docs][1])

1. **Message History** - Automatically persists complete conversation including tool calls
2. **Artifact Generation** - Converts outputs:
   - `str` → `TextPart`
   - Structured data → `DataPart`
3. **Task Management** - Creates and tracks tasks through completion
4. **Context Threading** - Maintains conversation continuity via `context_id`

### Example with Dependencies

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class UserPreferences:
    dietary_restrictions: list[str]
    favorite_cuisines: list[str]

agent = Agent(
    'openai:gpt-5',
    deps_type=UserPreferences,
    instructions='Recommend recipes based on user preferences'
)

@agent.tool
async def search_recipes(
    ctx: RunContext[UserPreferences],
    ingredients: list[str]
) -> dict:
    """Search for recipes matching ingredients and preferences"""
    # Access dependencies
    restrictions = ctx.deps.dietary_restrictions
    cuisines = ctx.deps.favorite_cuisines

    # Implement search logic
    return {
        'recipes': [...],
        'filtered_by': restrictions
    }

# Convert to A2A server
app = agent.to_a2a()
```

Clients can then interact via the A2A protocol while the agent uses full Pydantic AI capabilities including tools, dependencies, and type safety.

## JSON-RPC Protocol Support

FastA2A implements the A2A JSON-RPC 2.0 transport: ([FastA2A API Reference][2])

### Supported Methods

**Message Operations:**
- `message/send` - Submit user message, returns task
- `message/stream` - Streaming variant (if supported)

**Task Operations:**
- `tasks/get` - Retrieve task state
- `tasks/cancel` - Terminate execution
- `tasks/resubscribe` - Reconnect to task

**Push Notification Configuration:**
- `tasks/pushNotification/set` - Configure webhook
- `tasks/pushNotification/get` - Fetch configuration
- `tasks/pushNotificationConfig/list` - Enumerate configs
- `tasks/pushNotificationConfig/delete` - Remove config

### Request/Response Format

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "Hello"}]
    }
  }
}
```

**Success Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "task": {
      "id": "task_123",
      "status": {"state": "submitted"},
      ...
    }
  }
}
```

**Error Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": {"detail": "Missing required field"}
  }
}
```

([FastA2A API Reference][2])

### Error Codes

| Code | Message | Purpose |
|------|---------|---------|
| -32700 | Invalid JSON payload | Parse failure |
| -32600 | Request validation error | Invalid request structure |
| -32601 | Method not found | Unknown operation |
| -32602 | Invalid parameters | Argument mismatch |
| -32603 | Internal error | Server exception |
| -32001 | Task not found | Missing task ID |
| -32002 | Task not cancelable | Invalid state for cancellation |
| -32003 | Push notification not supported | Feature unavailable |
| -32004 | Operation not supported | Unsupported operation |
| -32005 | Incompatible content types | MIME type mismatch |
| -32006 | Invalid agent response | Malformed response |

([FastA2A API Reference][2])

## Client Usage

### A2AClient

FastA2A provides a simple client for testing: ([FastA2A API Reference][2])

```python
from fasta2a.client import A2AClient
import httpx

# Create client
async with httpx.AsyncClient() as http_client:
    client = A2AClient(
        base_url='http://localhost:8000',
        http_client=http_client
    )

    # Send message
    response = await client.send_message({
        'role': 'user',
        'parts': [{'kind': 'text', 'text': 'Hello'}]
    })

    if 'error' in response:
        print(f"Error: {response['error']}")
    else:
        task = response['result']['task']
        print(f"Task ID: {task['id']}")
        print(f"State: {task['status']['state']}")

    # Get task status
    task_response = await client.get_task(task['id'])
    if 'result' in task_response:
        task = task_response['result']['task']
        print(f"State: {task['status']['state']}")

        if task['artifacts']:
            for artifact in task['artifacts']:
                for part in artifact['parts']:
                    if part['kind'] == 'text':
                        print(f"Result: {part['text']}")
```

### Exception Handling

```python
from fasta2a.client import UnexpectedResponseError

try:
    response = await client.send_message(message)
except UnexpectedResponseError as e:
    print(f"HTTP {e.status_code}: {e.content}")
```

([FastA2A API Reference][2])

## Production Deployment

### ASGI Server Deployment

FastA2A is built on Starlette, making it compatible with any ASGI server: ([FastA2A GitHub][3])

**Uvicorn:**
```bash
uvicorn myagent:app --host 0.0.0.0 --port 8000 --workers 4
```

**Gunicorn with Uvicorn workers:**
```bash
gunicorn myagent:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Hypercorn:**
```bash
hypercorn myagent:app --bind 0.0.0.0:8000
```

### Distributed Workers

Workers can run separately from the web server: ([FastA2A GitHub][3])

**Server Process:**
```python
# server.py
from fasta2a import FastA2A
from fasta2a.broker import RedisBroker  # Example
from fasta2a.storage import PostgresStorage  # Example

storage = PostgresStorage(connection_string='...')
broker = RedisBroker(redis_url='redis://localhost:6379')

app = FastA2A(
    storage=storage,
    broker=broker,
    name='Production Agent',
    url='https://agent.example.com'
)
```

**Worker Process:**
```python
# worker.py
import asyncio
from myagent import MyAgentWorker
from fasta2a.broker import RedisBroker
from fasta2a.storage import PostgresStorage

async def main():
    storage = PostgresStorage(connection_string='...')
    broker = RedisBroker(redis_url='redis://localhost:6379')

    worker = MyAgentWorker(storage=storage, broker=broker)

    async for _ in worker.run():
        pass  # Process tasks continuously

if __name__ == '__main__':
    asyncio.run(main())
```

Run separately:
```bash
# Terminal 1 - HTTP server
uvicorn server:app --host 0.0.0.0 --port 8000

# Terminal 2 - Worker(s)
python worker.py
```

### Environment Configuration

```python
import os
from fasta2a import FastA2A

app = FastA2A(
    storage=storage,
    broker=broker,
    name=os.getenv('AGENT_NAME', 'My Agent'),
    url=os.getenv('AGENT_URL', 'http://localhost:8000'),
    version=os.getenv('AGENT_VERSION', '1.0.0'),
    debug=os.getenv('DEBUG', 'false').lower() == 'true'
)
```

## OpenTelemetry Integration

FastA2A includes OpenTelemetry API dependency for distributed tracing: ([FastA2A GitHub][3])

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint='http://localhost:4317')
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# FastA2A will automatically instrument requests
app = FastA2A(storage=storage, broker=broker, ...)
```

## Best Practices

### 1. Understand the Architecture

Before implementation, understand the three core components (Storage, Broker, Worker) and how context maintains conversation continuity across multiple tasks. ([Pydantic AI A2A Docs][1])

### 2. Choose Appropriate Storage

**In-Memory Storage** - Development and testing only
```python
from fasta2a.storage import InMemoryStorage
storage = InMemoryStorage()  # Data lost on restart
```

**Persistent Storage** - Production deployments
- Implement custom `Storage` class
- Use databases (PostgreSQL, MongoDB, etc.)
- Persist both tasks and context
- Handle concurrent access safely

### 3. Implement Robust Workers

- Handle exceptions gracefully
- Update task states appropriately
- Implement cancellation support
- Log execution details for debugging
- Use appropriate context types for your agent

### 4. Configure Skills Accurately

- Provide clear, descriptive skill names and descriptions
- Include realistic examples for discovery
- Specify accurate input/output MIME types
- Use meaningful tags for categorization

### 5. Deploy with Scalability

- Use distributed broker for multi-worker setups
- Run workers separately from HTTP server
- Scale workers independently based on load
- Monitor task queue depth
- Implement health checks

### 6. Security Considerations

- Validate all incoming messages
- Sanitize user inputs before agent processing
- Implement authentication (see A2A security guide)
- Rate limit task creation
- Audit task execution
- Protect sensitive context data

### 7. Observability

- Enable OpenTelemetry tracing
- Log task state transitions
- Monitor execution times
- Track error rates
- Alert on stuck tasks

### 8. Testing

- Test with in-memory components first
- Validate Agent Card generation
- Test task lifecycle (submit → working → completed)
- Test context threading across multiple tasks
- Test error handling and edge cases

## Limitations and Considerations

### Current Limitations

1. **Opinionated Task Creation** - FastA2A "will always create a Task and run it on the background" rather than offering stateless alternatives ([FastA2A GitHub][3])

2. **Default Capabilities** - Default Agent Card capabilities are limited:
   - `streaming: false`
   - `push_notifications: false`
   - `state_transition_history: false`

3. **Content Type Support** - Default input/output modes limited to `application/json` ([FastA2A API Reference][2])

### Design Decisions

- **Framework Agnostic** - Requires custom Worker implementation for non-Pydantic AI frameworks
- **Async-First** - All operations are async, no synchronous API
- **ASGI-Based** - Requires ASGI-compatible deployment infrastructure

## Complete Example: Recipe Agent

```python
# recipe_agent.py
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from fasta2a import Skill

@dataclass
class RecipePreferences:
    dietary_restrictions: list[str]
    favorite_cuisines: list[str]
    skill_level: str

# Create Pydantic AI agent
agent = Agent(
    'openai:gpt-5',
    deps_type=RecipePreferences,
    instructions='''
    You are a helpful recipe recommendation agent.
    Consider user's dietary restrictions and preferences.
    Provide detailed, easy-to-follow recipes.
    '''
)

@agent.tool
async def search_recipes(
    ctx: RunContext[RecipePreferences],
    query: str,
    max_results: int = 5
) -> list[dict]:
    """Search recipe database based on query and preferences"""
    # Implement recipe search
    return [
        {
            'title': 'Pasta Carbonara',
            'ingredients': ['pasta', 'eggs', 'cheese'],
            'difficulty': 'easy'
        }
    ]

@agent.tool
async def get_nutrition_info(
    ctx: RunContext[RecipePreferences],
    recipe_title: str
) -> dict:
    """Get nutritional information for a recipe"""
    # Implement nutrition lookup
    return {
        'calories': 450,
        'protein': '15g',
        'carbs': '55g'
    }

# Convert to A2A server with skills
app = agent.to_a2a(
    name='Recipe Agent',
    url='https://recipes.example.com',
    version='2.0.0',
    description='AI-powered recipe recommendations with dietary preferences',
    skills=[
        Skill(
            id='recipe-search',
            name='Recipe Search',
            description='Search recipes by ingredients, cuisine, or dietary needs',
            tags=['cooking', 'search', 'recipes'],
            examples=[
                'Find me Italian pasta recipes',
                'Low-carb chicken recipes',
                'Vegan desserts with chocolate'
            ],
            input_modes=['application/json'],
            output_modes=['application/json']
        ),
        Skill(
            id='nutrition-analysis',
            name='Nutrition Analysis',
            description='Analyze nutritional content of recipes',
            tags=['nutrition', 'health', 'analysis'],
            examples=[
                'What are the calories in Pasta Carbonara?',
                'Nutrition info for chocolate cake'
            ],
            input_modes=['application/json'],
            output_modes=['application/json']
        )
    ]
)

# Deploy with: uvicorn recipe_agent:app --host 0.0.0.0 --port 8000
```

## References

[1]: https://ai.pydantic.dev/a2a/ "Pydantic AI A2A Documentation"
[2]: https://ai.pydantic.dev/api/fasta2a/ "FastA2A API Reference"
[3]: https://github.com/pydantic/fasta2a "FastA2A GitHub Repository"
[4]: https://pypi.org/project/fasta2a/ "FastA2A PyPI Package"
[5]: https://ai.pydantic.dev/ "Pydantic AI Documentation"