---
title: "Pydantic AI Function Tools"
description: "Comprehensive guide to defining and using function tools in Pydantic AI agents"
type: "framework-guide"
tags: ["pydantic-ai", "tools", "function-tools", "agents", "llm", "dependencies", "toolsets", "rag"]
category: "ai-frameworks"
subcategory: "agent-frameworks"
version: "1.0"
last_updated: "2025-11-04"
status: "stable"
sources:
  - name: "Pydantic AI Function Tools Documentation"
    url: "https://ai.pydantic.dev/tools/index.md"
  - name: "Pydantic AI Tools API Reference"
    url: "https://ai.pydantic.dev/api/tools/index.md"
  - name: "Pydantic AI Toolsets API Reference"
    url: "https://ai.pydantic.dev/api/toolsets/index.md"
  - name: "Pydantic AI Agents Documentation"
    url: "https://ai.pydantic.dev/agents/index.md"
  - name: "Pydantic AI Dependencies Guide"
    url: "https://ai.pydantic.dev/dependencies/index.md"
  - name: "Pydantic AI Common Tools"
    url: "https://ai.pydantic.dev/common-tools/index.md"
  - name: "Pydantic AI Testing Guide"
    url: "https://ai.pydantic.dev/testing/index.md"
related: ["pydantic-ai-links.md"]
author: "unknown"
contributors: []
---

# Pydantic AI Function Tools

## Overview

Function tools in Pydantic AI enable LLM agents to perform actions and retrieve information to enhance response generation. ([Function Tools Documentation][1]) They serve as the "R" component of RAG (Retrieval-Augmented Generation), allowing models to request supplementary data beyond vector search capabilities. ([Function Tools Documentation][1])

Tools are Python functions (sync or async) that agents can invoke during execution. ([Function Tools Documentation][1]) The framework automatically generates JSON schemas from function signatures, and Pydantic validates tool arguments with validation errors passed back to the LLM for retry. ([Function Tools Documentation][1])

### Core Architecture

Function tools use the model's functions API under the hood. ([Function Tools Documentation][1]) The distinction between function tools and structured outputs is primarily semantic—both use the model's functions API, but tools execute function implementations while structured outputs produce final results. ([Function Tools Documentation][1])

Tools can return any JSON-serializable data, enabling flexible information retrieval and action execution patterns. ([Function Tools Documentation][1])

## Tool Definition

### Decorator-Based Registration

The most common pattern for defining tools uses decorators on the agent instance. ([Function Tools Documentation][1])

**Context-Aware Tools** - Use `@agent.tool` for tools that need access to dependencies or agent state:

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4')

@agent.tool
async def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps
```

**Stateless Tools** - Use `@agent.tool_plain` for tools without dependencies:

```python
import random

@agent.tool_plain
def roll_dice() -> int:
    """Roll a dice."""
    return random.randint(1, 6)
```

Using `@agent.tool_plain` clarifies intent and improves performance for stateless operations. ([Function Tools Documentation][1])

### Parameter Schema Generation

All function parameters except `RunContext` contribute to the tool's JSON schema. ([Function Tools Documentation][1]) The framework supports dataclasses, TypedDict, and Pydantic models as parameters. ([Function Tools Documentation][1])

**Single-Parameter Optimization**: When a tool has one parameter representing a JSON schema object, the schema simplifies to that object structure directly. ([Function Tools Documentation][1]) This avoids unnecessary nesting in the tool interface.

### Docstring Integration

Tool docstrings serve as LLM descriptions, helping models understand when and how to use tools. ([Function Tools Documentation][1]) Parameter descriptions are extracted from docstrings in Google, NumPy, or Sphinx formats. ([Function Tools Documentation][1])

```python
from dataclasses import dataclass

@dataclass
class LatLng:
    lat: float
    lng: float

@weather_agent.tool
async def get_lat_lng(ctx: RunContext[Deps], location_description: str) -> LatLng:
    """Get the latitude and longitude of a location.

    Args:
        location_description: Human-readable location description

    Returns:
        LatLng object with coordinates
    """
    r = await ctx.deps.client.get(
        'https://demo-endpoints.pydantic.workers.dev/latlng',
        params={'location': location_description},
    )
    r.raise_for_status()
    return LatLng.model_validate_json(r.content)
```

Use `require_parameter_descriptions=True` to enforce parameter documentation. ([Tools API Reference][2]) Configure format via `docstring_format` parameter. ([Tools API Reference][2])

## Registration Methods

### Constructor Registration

Tools can be registered directly when creating the agent. ([Function Tools Documentation][1])

**Direct Function Registration**:

```python
def roll_dice() -> int:
    """Roll a dice."""
    return random.randint(1, 6)

agent = Agent(
    'google-gla:gemini-2.5-flash',
    tools=[roll_dice, get_player_name],
)
```

**Using Tool Class** for fine-grained control:

```python
from pydantic_ai.tools import Tool

agent = Agent(
    'openai:gpt-4',
    tools=[
        Tool(roll_dice, takes_ctx=False),
        Tool(get_player_name, takes_ctx=True),
    ]
)
```

The Tool class enables custom configuration including retries, naming, and execution behavior. ([Tools API Reference][2])

### Toolset Registration

For advanced scenarios with multiple tool sources, use toolsets. ([Toolsets API Reference][3])

```python
agent = Agent(
    'openai:gpt-4',
    toolsets=[my_toolset, mcp_toolset],
)
```

Toolsets provide organizational structure and advanced capabilities like filtering, prefixing, and approval workflows. ([Toolsets API Reference][3])

## Dependency Injection

### RunContext Structure

Tools access execution context through `RunContext[DependencyType]`. ([Dependencies Guide][5])

```python
@dataclass
class RunContext:
    deps: AgentDepsT              # Injected dependencies
    model: Model                  # LLM instance
    usage: Usage                  # Token consumption metrics
    messages: list[Message]       # Conversation history
    tracer: Tracer               # Execution tracing
    tool_name: str | None         # Current tool name
    tool_call_id: str | None      # Tool call identifier
    retry: int                    # Current retry attempt

    @property
    def last_attempt(self) -> bool:
        """Indicates final retry before failure"""
```

([Dependencies Guide][5])

### Dependency Patterns

Dependencies can be any Python type, with dataclasses recommended for grouping multiple dependencies. ([Dependencies Guide][5])

```python
from dataclasses import dataclass
import httpx

@dataclass
class Deps:
    client: httpx.AsyncClient
    api_key: str

agent = Agent('openai:gpt-4', deps_type=Deps)

@agent.tool
async def fetch_data(ctx: RunContext[Deps], query: str) -> dict:
    """Fetch data from external API.

    Args:
        query: Search query string
    """
    response = await ctx.deps.client.get(
        'https://api.example.com/search',
        params={'q': query},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    response.raise_for_status()
    return response.json()
```

Dependencies are passed during agent execution. ([Dependencies Guide][5]) Async dependencies work best with async tool functions. ([Dependencies Guide][5])

```python
async with httpx.AsyncClient() as client:
    deps = Deps(client=client, api_key='secret')
    result = await agent.run('Find information about Python', deps=deps)
```

### Testing and Override

Override dependencies for testing using context managers. ([Testing Guide][7])

```python
with agent.override(deps=test_deps):
    result = agent.run_sync('test prompt')
```

This enables dependency injection without modifying production code. ([Testing Guide][7])

## Tool Execution

### Execution Flow

The standard execution sequence follows these steps: ([Function Tools Documentation][1])

1. Agent sends prompts to the model with available tool definitions
2. Model decides which tools to invoke based on context
3. Agent executes tools with validated parameters
4. Tool results return to model
5. Model receives outputs and continues reasoning
6. Process repeats until model produces final response

### Visibility and Monitoring

The `all_messages()` method reveals the complete interaction sequence including tool calls. ([Function Tools Documentation][1]) When streaming, `FunctionToolCallEvent` and `FunctionToolResultEvent` provide real-time visibility. ([Function Tools Documentation][1])

Usage tracking includes tool call counts via the Usage object. ([Function Tools Documentation][1]) The `tool_calls_limit` parameter caps successful executions per run. ([Agents Documentation][4])

### Retry Behavior

Tools support automatic retries for handling transient failures. ([Tools API Reference][2])

```python
@agent.tool(retries=2)
async def fallible_operation(ctx: RunContext[Deps]) -> str:
    """Operation that might need retries"""
    # Tool logic with potential failures
    if ctx.retry > 0:
        # Handle retry logic
        pass
    return result
```

Validation errors automatically trigger retries, with error details passed to the LLM for correction. ([Function Tools Documentation][1])

## Advanced Features

### Tool Class Configuration

The Tool class provides extensive configuration options. ([Tools API Reference][2])

```python
Tool(
    function=my_function,
    takes_ctx=False,
    max_retries=3,
    name="custom_name",
    description="Custom description",
    prepare=prepare_callback,
    docstring_format="google",
    require_parameter_descriptions=True,
    schema_generator=CustomSchemaGenerator,
    strict=True,
    sequential=True,
    requires_approval=True,
    metadata={"custom": "data"}
)
```

### Dynamic Tool Preparation

Prepare callbacks enable runtime modification of tool definitions based on context. ([Tools API Reference][2])

```python
async def prepare_tool(ctx: RunContext, tool_def: ToolDefinition) -> ToolDefinition:
    """Modify tool definition at runtime based on context"""
    # Conditionally modify tool based on user permissions, state, etc.
    if ctx.deps.user.is_admin:
        tool_def.description += " (Admin mode)"
    return tool_def

Tool(my_function, prepare=prepare_tool)
```

### Deferred Tool Execution

Tools can be marked for external execution or human approval. ([Tools API Reference][2])

- `kind="external"` - Execution happens outside agent run
- `kind="unapproved"` - Requires human approval

`DeferredToolRequests` and `DeferredToolResults` manage the workflow. ([Tools API Reference][2])

### Tool Approval Workflows

Require human-in-the-loop for sensitive operations. ([Toolsets API Reference][3])

```python
from pydantic_ai.toolsets import FunctionToolset

toolset = FunctionToolset()

@toolset.tool
async def delete_records(ctx: RunContext[Deps], record_ids: list[int]) -> str:
    """Delete records from database."""
    await ctx.deps.db.delete_many(record_ids)
    return f'Deleted {len(record_ids)} records'

# Require approval for specific tools
approved_toolset = toolset.approval_required(['delete_records'])

# Or require approval for all tools
approved_toolset = toolset.approval_required()
```

## Toolsets

### AbstractToolset Interface

Toolsets manage collections of tools with three core responsibilities: ([Toolsets API Reference][3])

1. List available tools
2. Validate tool arguments
3. Execute tool calls

### FunctionToolset

Organize related tools using FunctionToolset. ([Toolsets API Reference][3])

```python
from pydantic_ai.toolsets import FunctionToolset

toolset = FunctionToolset()

@toolset.tool
async def my_tool(ctx: RunContext[Deps], param: str) -> str:
    """Tool documentation"""
    return result
```

### CombinedToolset

Aggregate multiple toolsets with automatic conflict detection. ([Toolsets API Reference][3])

```python
from pydantic_ai.toolsets import CombinedToolset

combined = CombinedToolset([toolset1, toolset2, mcp_toolset])
agent = Agent('openai:gpt-4', toolsets=[combined])
```

### Wrapper Toolsets

Wrapper toolsets provide cross-cutting functionality: ([Toolsets API Reference][3])

- **FilteredToolset** - Restricts available tools based on filters
- **PrefixedToolset** - Adds prefixes to prevent name conflicts
- **RenamedToolset** - Maps tool names via dictionary
- **PreparedToolset** - Dynamically modifies tool definitions
- **ApprovalRequiredToolset** - Enforces human-in-the-loop patterns

**Chaining Operations**:

```python
toolset = (
    my_toolset
    .filtered(lambda name: not name.startswith('_'))
    .prefixed('myapp_')
    .approval_required(['delete_data'])
)
```

### FastMCP Integration

Integrate Model Context Protocol (MCP) servers as toolsets. ([Toolsets API Reference][3])

```python
from pydantic_ai.toolsets import FastMCPToolset

mcp_toolset = FastMCPToolset(mcp_client)
agent = Agent('openai:gpt-4', toolsets=[mcp_toolset])
```

This enables agents to access tools from MCP servers seamlessly. ([Toolsets API Reference][3])

## Common Built-in Tools

### DuckDuckGo Search

Free web search via DuckDuckGo API. ([Common Tools Documentation][6])

```python
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

agent = Agent(
    'openai:o3-mini',
    tools=[duckduckgo_search_tool()]
)
```

Requires installation: `pydantic-ai-slim[duckduckgo]` ([Common Tools Documentation][6])

### Tavily Search

Paid search service with free exploration credits. ([Common Tools Documentation][6])

```python
from pydantic_ai.common_tools.tavily import tavily_search_tool

agent = Agent(
    'openai:o3-mini',
    tools=[tavily_search_tool(api_key)]
)
```

Requires installation: `pydantic-ai-slim[tavily]` ([Common Tools Documentation][6])
Sign up at Tavily for API key. ([Common Tools Documentation][6])

## Best Practices

### Documentation

- Always include comprehensive docstrings for tools ([Function Tools Documentation][1])
- Document all parameters using supported formats (Google, NumPy, Sphinx) ([Tools API Reference][2])
- Use `require_parameter_descriptions=True` for validation enforcement ([Tools API Reference][2])

### Context Awareness

- Use `@agent.tool_plain` for stateless operations ([Function Tools Documentation][1])
- Use `@agent.tool` only when accessing dependencies or agent state ([Function Tools Documentation][1])
- This clarifies intent and improves performance ([Function Tools Documentation][1])

### Tool Design

- Keep tools focused on single responsibilities
- Return structured, typed data rather than unstructured strings ([Function Tools Documentation][1])
- Use Pydantic models for complex return types ([Function Tools Documentation][1])

### Error Handling

- Raise descriptive exceptions that the LLM can understand ([Function Tools Documentation][1])
- Let validation errors propagate—framework passes them to LLM for retry ([Function Tools Documentation][1])
- Use retry configuration for flaky operations ([Tools API Reference][2])

### Reusability

- Register tools via constructor when sharing across agents ([Function Tools Documentation][1])
- Use toolsets for organizing related tools ([Toolsets API Reference][3])
- Leverage wrapper toolsets for cross-cutting concerns ([Toolsets API Reference][3])

### Testing

- Use `TestModel` for basic tool execution verification ([Testing Guide][7])
- Use `FunctionModel` for conditional logic and specific paths ([Testing Guide][7])
- Use `agent.override()` for dependency injection in tests ([Testing Guide][7])
- Set `ALLOW_MODEL_REQUESTS=False` to prevent accidental API calls ([Testing Guide][7])
- Use `capture_run_messages()` to inspect tool calls ([Testing Guide][7])

### Performance

- Prefer async tools for I/O-bound operations ([Function Tools Documentation][1])
- Use tool limits to prevent runaway execution ([Agents Documentation][4])
- Consider caching for expensive operations

### Security

- Use approval workflows for sensitive operations ([Toolsets API Reference][3])
- Validate and sanitize tool inputs beyond type checking
- Implement proper access controls in dependency injection ([Dependencies Guide][5])

## Usage Examples

### Basic Tool with Dependencies

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
import httpx

@dataclass
class Deps:
    client: httpx.AsyncClient
    api_key: str

agent = Agent('openai:gpt-4', deps_type=Deps)

@agent.tool
async def fetch_data(ctx: RunContext[Deps], query: str) -> dict:
    """Fetch data from external API.

    Args:
        query: Search query string
    """
    response = await ctx.deps.client.get(
        'https://api.example.com/search',
        params={'q': query},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    response.raise_for_status()
    return response.json()

# Run agent with dependencies
async with httpx.AsyncClient() as client:
    deps = Deps(client=client, api_key='secret')
    result = await agent.run('Find information about Python', deps=deps)
```

### Multiple Tools with Sequential Execution

```python
@agent.tool
async def get_coordinates(ctx: RunContext[Deps], location: str) -> dict:
    """Get latitude and longitude for a location.

    Args:
        location: Location name or address
    """
    response = await ctx.deps.client.get(
        'https://geocoding-api.example.com',
        params={'address': location}
    )
    return response.json()

@agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lng: float) -> str:
    """Get weather for coordinates.

    Args:
        lat: Latitude
        lng: Longitude
    """
    response = await ctx.deps.client.get(
        'https://weather-api.example.com',
        params={'lat': lat, 'lon': lng}
    )
    data = response.json()
    return f"{data['condition']}, {data['temp']}°F"

# Agent automatically chains tools
result = await agent.run('What is the weather in New York?', deps=deps)
```

### Tool with Approval

```python
from pydantic_ai.toolsets import FunctionToolset

toolset = FunctionToolset()

@toolset.tool
async def delete_records(ctx: RunContext[Deps], record_ids: list[int]) -> str:
    """Delete records from database.

    Args:
        record_ids: List of record IDs to delete
    """
    await ctx.deps.db.delete_many(record_ids)
    return f'Deleted {len(record_ids)} records'

# Require approval for this tool
approved_toolset = toolset.approval_required(['delete_records'])
agent = Agent('openai:gpt-4', toolsets=[approved_toolset])
```

### Testing Tools

```python
from pydantic_ai import models
from pydantic_ai.messages import ModelMessage, ModelRequest, ToolCallPart

async def test_fetch_data_tool():
    """Test the fetch_data tool in isolation"""

    # Create test dependencies
    test_deps = Deps(
        client=MockAsyncClient(),
        api_key='test_key'
    )

    # Override dependencies for testing
    with agent.override(deps=test_deps):
        # Use FunctionModel to force specific tool calls
        m = models.FunctionModel()
        m.add_call_response(
            ModelRequest(parts=[ToolCallPart(tool_name='fetch_data', args={'query': 'test'})]),
            ModelMessage(parts=['Success'])
        )

        with agent.override(model=m):
            result = await agent.run('test query')
            assert 'Success' in result.data
```

## References

[1]: https://ai.pydantic.dev/tools/index.md "Pydantic AI Function Tools Documentation"
[2]: https://ai.pydantic.dev/api/tools/index.md "Pydantic AI Tools API Reference"
[3]: https://ai.pydantic.dev/api/toolsets/index.md "Pydantic AI Toolsets API Reference"
[4]: https://ai.pydantic.dev/agents/index.md "Pydantic AI Agents Documentation"
[5]: https://ai.pydantic.dev/dependencies/index.md "Pydantic AI Dependencies Guide"
[6]: https://ai.pydantic.dev/common-tools/index.md "Pydantic AI Common Tools"
[7]: https://ai.pydantic.dev/testing/index.md "Pydantic AI Testing Guide"
