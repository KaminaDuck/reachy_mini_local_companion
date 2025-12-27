---
author: unknown
category: ai-frameworks
contributors: []
description: Complete reference for building production-grade AI agents with Pydantic
  AI
last_updated: '2025-11-01'
related:
- pydantic-ai-links.md
- openai-integration.md
sources:
- name: Pydantic AI Agents Documentation
  url: https://ai.pydantic.dev/agents/index.md
- name: Pydantic AI Tools Documentation
  url: https://ai.pydantic.dev/tools/index.md
- name: Pydantic AI Dependencies Documentation
  url: https://ai.pydantic.dev/dependencies/index.md
- name: Pydantic AI Message History Documentation
  url: https://ai.pydantic.dev/message-history/index.md
- name: Pydantic AI Agent API Reference
  url: https://ai.pydantic.dev/api/agent/index.md
status: stable
subcategory: agent-frameworks
tags:
- pydantic-ai
- agents
- llm
- python
- tools
- dependencies
- streaming
- type-safety
title: Pydantic AI Agents
type: framework-guide
version: '1.0'
---

# Pydantic AI Agents Reference

Pydantic AI is a Python agent framework designed to make it less painful to build production-grade applications with Generative AI. ([Pydantic AI Agents Documentation][1])

## Overview

An agent in Pydantic AI serves as "a container for instructions, function tools, structured output types, dependency constraints, and LLM models." ([Pydantic AI Agents Documentation][1]) Agents are designed for reuse—instantiated once as module globals and reused throughout applications, similar to how FastAPI apps are structured. They employ generic typing for both dependencies and outputs, enabling robust type safety. ([Pydantic AI Agents Documentation][1])

## Core Architecture

Each agent encapsulates the following components: ([Pydantic AI Agents Documentation][1])

| Component | Purpose |
|-----------|---------|
| **Instructions** | Developer-defined guidelines for LLM behavior |
| **Function tools & toolsets** | Callable functions the LLM invokes during generation |
| **Structured output type** | Enforced datatype for final responses |
| **Dependency type constraint** | Dynamic context available to tools and instructions |
| **LLM model** | Optional default model specification |
| **Model settings** | Fine-tuning parameters (temperature, max_tokens, etc.) |

## Agent Creation

### Basic Instantiation

Agents are created with type hints indicating dependency and output types: ([Pydantic AI Agents Documentation][1])

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-5-nano',
    deps_type=int,
    output_type=bool,
    system_prompt='Your instructions here'
)
```

The type signature follows the pattern: `Agent[DependencyType, OutputType]` ([Pydantic AI Agents Documentation][1])

### Minimal Example

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5-nano')
result = agent.run_sync('What is the capital of France?')
```

([Pydantic AI Agent API Reference][5])

## Instructions vs System Prompts

Pydantic AI distinguishes between two types of prompts: ([Pydantic AI Agents Documentation][1])

**Instructions** (recommended): Included only with the current agent; excluded when message history exists.

**System Prompts**: Preserved in message history across multiple runs and agents.

Both support static definitions via constructor parameters and dynamic generation via decorators:

```python
@agent.instructions
def dynamic_instruction(ctx: RunContext[str]) -> str:
    return f"User: {ctx.deps}"
```

([Pydantic AI Agents Documentation][1])

## Running Agents

### Execution Methods

Pydantic AI provides multiple execution modes: ([Pydantic AI Agents Documentation][1])

| Method | Type | Returns | Use Case |
|--------|------|---------|----------|
| `run()` | Async | RunResult | Standard asynchronous execution |
| `run_sync()` | Sync | RunResult | Blocking execution |
| `run_stream()` | Async context manager | StreamedRunResult | Text/output streaming |
| `run_stream_events()` | Async iterable | AgentStreamEvent sequence | Raw event streaming |
| `iter()` | Async context manager | AgentRun | Graph node iteration |

### Result Types

- **RunResult**: Contains final output with usage statistics
- **StreamedRunResult**: Enables streaming via `stream_text()` or `stream_output()`
- **RunUsage**: Token counts, request counts, tool call metrics

([Pydantic AI Agents Documentation][1])

## Streaming Capabilities

### Text Streaming

```python
async with agent.run_stream('prompt') as response:
    async for text in response.stream_text():
        print(text)
```

([Pydantic AI Agents Documentation][1])

### Event Streaming

Capture granular execution details via event handlers:

```python
async def handle_event(event: AgentStreamEvent):
    if isinstance(event, PartStartEvent):
        # Process new response part
    elif isinstance(event, FunctionToolCallEvent):
        # Track tool invocation
```

([Pydantic AI Agents Documentation][1])

### Graph Iteration

Manual node-by-node control via `agent.iter()` enables custom logic injection:

```python
async with agent.iter('prompt') as run:
    async for node in run:
        if Agent.is_model_request_node(node):
            # Custom handling
```

([Pydantic AI Agents Documentation][1])

## Function Tools

### Defining Tools

Function tools enable models to perform actions and retrieve information to enhance responses. As the documentation states: "Function tools use the model's 'tools' or 'functions' API to let the model know what is available to call." ([Pydantic AI Tools Documentation][2])

### Tool Registration

Pydantic AI offers three registration methods: ([Pydantic AI Tools Documentation][2])

1. **`@agent.tool`** (default) - For tools needing agent context access
2. **`@agent.tool_plain`** - For tools without context requirements
3. **`tools` keyword argument** - Accepts plain functions or Tool instances

### Tool Parameters and Schema

Function parameters (except `RunContext`) build the tool's schema. Pydantic AI extracts docstrings to populate parameter descriptions, supporting Google, NumPy, and Sphinx formats. You can enforce descriptions via `require_parameter_descriptions=True`. ([Pydantic AI Tools Documentation][2])

### Return Types

"Tools can return anything that Pydantic can serialize to JSON." ([Pydantic AI Tools Documentation][2])

### Tool Example

```python
@agent.tool
async def tool_name(ctx: RunContext[DepsType], param: str) -> str:
    """Tool description visible to LLM"""
    return result
```

([Pydantic AI Agents Documentation][1])

Tools receive `RunContext` containing dependencies and retry information. The LLM may invoke tools iteratively based on responses.

## Dependency Injection

### What Are Dependencies?

Pydantic AI's dependency injection system supplies data and services to agents, tools, system prompts, and output validators. The framework emphasizes using established Python patterns rather than introducing specialized "magic," prioritizing type safety and testability. ([Pydantic AI Dependencies Documentation][3])

### Defining Dependencies

Dependencies can be any Python type, though dataclasses serve as convenient containers for multiple related objects. When creating an agent, pass the dependency type (not an instance) to the `deps_type` parameter: ([Pydantic AI Dependencies Documentation][3])

```python
from dataclasses import dataclass

@dataclass
class MyDeps:
    api_key: str
    database: Database

agent = Agent('openai:gpt-5-nano', deps_type=MyDeps)
```

This enables static type checking without runtime overhead.

### Accessing Dependencies

Functions that receive dependencies must accept `RunContext` as their first parameter. This context object—parameterized with the dependency type—provides access to actual dependency instances through the `.deps` attribute: ([Pydantic AI Dependencies Documentation][3])

```python
result = agent.run_sync('prompt', deps=MyDeps(api_key="...", database=db))
```

As the documentation notes: "RunContext is parameterized with the type of the dependencies, if this type is incorrect, static type checkers will raise an error." ([Pydantic AI Dependencies Documentation][3])

### Async vs Synchronous Dependencies

System prompts, tools, and validators run in an async context. Non-coroutine functions execute via `run_in_executor` in a thread pool. Notably, using `run_sync` versus `run` is independent of dependency synchronicity—"agents are always run in an async context." ([Pydantic AI Dependencies Documentation][3])

### Usage Across Agent Components

Dependencies integrate with: ([Pydantic AI Dependencies Documentation][3])
- **System prompts**: Fetch contextual data before agent execution
- **Tools**: Access external APIs or databases with authentication
- **Output validators**: Verify agent responses against external criteria

### Testing and Overriding

The `.override()` method allows dependency substitution during testing, enabling custom implementations without modifying application code paths. ([Pydantic AI Dependencies Documentation][3])

## Messages and Chat History

### Message Types

Pydantic AI uses two primary message classes: ([Pydantic AI Message History Documentation][4])

- **ModelRequest**: Contains system prompts and user input, structured with `SystemPromptPart` and `UserPromptPart` components
- **ModelResponse**: Holds model outputs as `TextPart` objects, including token usage and timestamp metadata

### Accessing Messages

After an agent run completes, retrieve conversations via the result object: ([Pydantic AI Message History Documentation][4])

- `all_messages()` - "returns all messages, including messages from prior runs"
- `new_messages()` - "returns only the messages from the current run"

Both methods have JSON variants (`all_messages_json()`, `new_messages_json()`).

### Multi-Turn Conversations

To maintain context across multiple interactions, pass prior messages to subsequent runs:

```python
result1 = agent.run_sync('initial prompt')
result2 = agent.run_sync(
    'follow-up',
    message_history=result1.new_messages()
)
```

([Pydantic AI Agents Documentation][1])

When `message_history` is provided and non-empty, the agent skips generating a new system prompt, assuming the existing history includes one. ([Pydantic AI Message History Documentation][4])

### Persistence

Messages can be converted to JSON using `ModelMessagesTypeAdapter`:

```python
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic.type_adapter import to_jsonable_python

as_python_objects = to_jsonable_python(result.new_messages())
same_history = ModelMessagesTypeAdapter.validate_python(as_python_objects)
```

([Pydantic AI Message History Documentation][4])

This enables storing conversations in databases or sharing across platforms.

### History Processing

The `history_processors` parameter allows intercepting and modifying messages before model requests. Common use cases include filtering sensitive data, reducing token costs, and summarizing older exchanges. ([Pydantic AI Message History Documentation][4])

## Advanced Configuration

### Model Settings

Three-tier precedence for settings: ([Pydantic AI Agents Documentation][1])

1. Model-level defaults
2. Agent-level defaults (override model)
3. Run-time overrides (highest priority)

```python
from pydantic_ai.settings import ModelSettings

result = agent.run_sync(
    'prompt',
    model_settings=ModelSettings(temperature=0.0, max_tokens=500)
)
```

### Usage Limits

Prevent excessive resource consumption: ([Pydantic AI Agents Documentation][1])

```python
from pydantic_ai.settings import UsageLimits

UsageLimits(
    response_tokens_limit=100,
    request_limit=3,
    tool_calls_limit=5
)
```

### Retry and Error Handling

Tools and output functions can trigger retries:

```python
from pydantic_ai import ModelRetry

@agent.tool
def tool(ctx: RunContext) -> str:
    if error_condition:
        raise ModelRetry('Provide guidance for retry')
    return result
```

([Pydantic AI Agents Documentation][1])

Access retry count via `ctx.retry`.

### Model Error Handling

Capture execution messages when errors occur:

```python
from pydantic_ai import capture_run_messages, UnexpectedModelBehavior

with capture_run_messages() as messages:
    try:
        result = agent.run_sync('prompt')
    except UnexpectedModelBehavior as e:
        # Access exchanged messages for diagnostics
```

([Pydantic AI Agents Documentation][1])

## Agent Class API

### Constructor Parameters

#### Core Configuration
- **`model`**: Model identifier (string, `KnownModelName`, or `Model` instance). Optional if provided at runtime.
- **`output_type`**: Validation schema for model responses (defaults to `str`)
- **`deps_type`**: Type for dependency injection (defaults to `NoneType`)
- **`name`**: Agent identifier for logging; auto-inferred if omitted

#### Behavior Control
- **`instructions`**: Static or dynamic instruction strings/callables
- **`system_prompt`**: Initial system prompts (string or sequence)
- **`retries`**: Default retry count for tool calls/validation (default: 1)
- **`output_retries`**: Specific retry limit for validation (inherits from `retries` if unset)
- **`end_strategy`**: Handling strategy for concurrent tool calls and results (`'early'` default)

#### Tools & Execution
- **`tools`**: Pre-registered tool functions
- **`builtin_tools`**: Model-specific built-in capabilities
- **`toolsets`**: Reusable tool collections and MCP servers
- **`prepare_tools`/`prepare_output_tools`**: Custom tool preparation logic per step

#### Model Configuration
- **`model_settings`**: Default request settings (merged with runtime settings)
- **`defer_model_check`**: Postpone environment validation until first run

#### Advanced Options
- **`instrument`**: OpenTelemetry integration (boolean or `InstrumentationSettings`)
- **`history_processors`**: Message history transformation functions
- **`event_stream_handler`**: Custom event handling during execution

([Pydantic AI Agent API Reference][5])

### Key Decorators
- **`@agent.tool`**: Register context-aware tool (receives `RunContext`)
- **`@agent.tool_plain`**: Register simple tool (no context)
- **`@agent.instructions`**: Register dynamic instructions
- **`@agent.system_prompt`**: Register dynamic system prompts (supports `dynamic=True`)
- **`@agent.output_validator`**: Register result validation
- **`@agent.toolset`**: Register toolset provider

([Pydantic AI Agent API Reference][5])

### Key Methods
- **`iter()`**: Async context manager for streaming graph node execution
- **`override()`**: Context manager for temporary runtime customization (name, deps, model, tools, etc.)
- **`instrument_all()`**: Static method to set default instrumentation globally

([Pydantic AI Agent API Reference][5])

## Type Safety

Pydantic AI integrates with static type checkers (mypy, pyright). Agent generic parameters enforce correct dependency and output types—type mismatches are caught before runtime. ([Pydantic AI Agents Documentation][1])

## Best Practices

1. **Instantiate agents once** as module-level constants for reuse
2. **Use instructions over system_prompt** unless message history must be preserved
3. **Employ type hints** for IDE support and static validation
4. **Set usage limits** when tools or requests could create loops
5. **Stream for large responses** to improve perceived responsiveness
6. **Use dependencies** instead of global state for dynamic context
7. **Validate tool outputs** via Pydantic models for automatic validation and retry

([Pydantic AI Agents Documentation][1])

## References

[1]: https://ai.pydantic.dev/agents/index.md "Pydantic AI Agents Documentation"
[2]: https://ai.pydantic.dev/tools/index.md "Pydantic AI Tools Documentation"
[3]: https://ai.pydantic.dev/dependencies/index.md "Pydantic AI Dependencies Documentation"
[4]: https://ai.pydantic.dev/message-history/index.md "Pydantic AI Message History Documentation"
[5]: https://ai.pydantic.dev/api/agent/index.md "Pydantic AI Agent API Reference"