---
author: unknown
category: ai-frameworks
contributors: []
description: OpenAI and OpenAI-compatible server integration for Pydantic AI agents
last_updated: '2025-11-01'
related:
- agents.md
- pydantic-ai-links.md
sources:
- name: Pydantic AI OpenAI Documentation
  url: https://ai.pydantic.dev/models/openai/index.md
- name: Pydantic AI OpenAI API Reference
  url: https://ai.pydantic.dev/api/models/openai/index.md
status: stable
subcategory: model-providers
tags:
- pydantic-ai
- openai
- llm
- vllm
- ollama
- lm-studio
- azure
- model-providers
title: Pydantic AI OpenAI Integration
type: integration-guide
version: '1.0'
---

# Pydantic AI OpenAI Integration

Pydantic AI provides comprehensive support for OpenAI models and OpenAI-compatible servers including vLLM, Ollama, LM Studio, and many other providers. ([Pydantic AI OpenAI Documentation][1])

## Installation & Setup

### Package Installation

Pydantic AI supports OpenAI models through the `pydantic-ai-slim[openai]` package. Install via pip or uv: ([Pydantic AI OpenAI Documentation][1])

```bash
pip install pydantic-ai-slim[openai]
# or
uv add pydantic-ai-slim[openai]
```

### Authentication

Set the `OPENAI_API_KEY` environment variable after obtaining credentials from platform.openai.com: ([Pydantic AI OpenAI Documentation][1])

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Basic Usage

### Agent Shorthand

The simplest approach uses the agent shorthand syntax: ([Pydantic AI OpenAI Documentation][1])

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5-nano')
result = agent.run_sync('Hello, world!')
```

### Direct Model Instantiation

Alternatively, developers can instantiate `OpenAIChatModel` directly with just the model name, which automatically uses the standard OpenAI endpoint: ([Pydantic AI OpenAI API Reference][2])

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel

model = OpenAIChatModel('gpt-4o')
agent = Agent(model)
```

## Core Configuration

### OpenAIChatModel

A dataclass that interfaces with OpenAI's Chat Completions API. Key initialization parameters: ([Pydantic AI OpenAI API Reference][2])

- **model_name** (`OpenAIModelName`): Model identifier
- **provider** (string or `Provider[AsyncOpenAI]`): Defaults to `'openai'`; supports alternatives like Azure, DeepSeek, and others
- **profile** (`ModelProfileSpec | None`): Custom model configuration
- **settings** (`ModelSettings | None`): Default request settings

Properties include `model_name`, `system` (provider name), and `base_url`. ([Pydantic AI OpenAI API Reference][2])

### Custom Provider Configuration

For advanced setups, the `OpenAIProvider` class accepts programmatic parameters. Developers can pass a custom `AsyncOpenAI` client to customize organization, project, and base_url settings per OpenAI's API documentation: ([Pydantic AI OpenAI Documentation][1])

```python
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIProvider
from openai import AsyncOpenAI

custom_client = AsyncOpenAI(
    api_key='your-key',
    organization='your-org',
    project='your-project'
)

provider = OpenAIProvider(custom_client)
model = OpenAIChatModel('gpt-4o', provider=provider)
```

## Model Settings

### OpenAIChatModelSettings

OpenAI-specific settings available for Chat Completions: ([Pydantic AI OpenAI API Reference][2])

- **openai_reasoning_effort**: Controls reasoning depth (`'low'`, `'medium'`, `'high'`)
- **openai_logprobs**: Include token probability data
- **openai_user**: End-user identifier for abuse monitoring
- **openai_service_tier**: Service tier selection

```python
from pydantic_ai.settings import ModelSettings

result = agent.run_sync(
    'prompt',
    model_settings=ModelSettings(
        temperature=0.7,
        max_tokens=500,
        openai_reasoning_effort='high'
    )
)
```

## OpenAI Responses API

### Overview

Pydantic AI offers `OpenAIResponsesModel` for accessing OpenAI's Responses API alongside traditional Chat Completions. This enables built-in tools including: ([Pydantic AI OpenAI Documentation][1])

- Web search functionality
- Code interpreter capabilities
- Image generation
- File search operations
- Computer use automation

### Configuration

File search and computer use require passing `FileSearchToolParam` or `ComputerToolParam` through `OpenAIResponsesModelSettings`: ([Pydantic AI OpenAI Documentation][1])

```python
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai import Agent

model = OpenAIResponsesModel('gpt-4o')
agent = Agent(model)
```

### Context Management

The Responses API supports referencing previous responses via `openai_previous_response_id` to maintain conversation state. Setting this to `'auto'` automatically selects the most recent response ID, optimizing efficiency by leveraging server-side history. ([Pydantic AI OpenAI Documentation][1])

### OpenAIResponsesModelSettings

Extended settings for the Responses API: ([Pydantic AI OpenAI API Reference][2])

- **openai_builtin_tools**: Integrated tools (web search, code interpreter)
- **openai_reasoning_summary**: Output verbosity for reasoning (`'detailed'` or `'concise'`)
- **openai_truncation**: Context management strategy (`'disabled'` or `'auto'`)
- **openai_text_verbosity**: Response conciseness control

### Supported Providers

The Responses API supports fewer providers than Chat Completions: ([Pydantic AI OpenAI API Reference][2])

`'openai'`, `'deepseek'`, `'azure'`, `'openrouter'`, `'grok'`, `'fireworks'`, `'together'`, `'nebius'`, `'ovhcloud'`, `'gateway'`

## Azure OpenAI Support

### Configuration

The framework supports Azure through `AsyncAzureOpenAI`, requiring specific parameters: ([Pydantic AI OpenAI Documentation][1])

- `azure_endpoint`
- `api_version`
- `api_key`

### Environment Variables

Set these environment variables to enable the `AzureProvider` shorthand: ([Pydantic AI OpenAI Documentation][1])

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `OPENAI_API_VERSION`

```bash
export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com'
export AZURE_OPENAI_API_KEY='your-azure-key'
export OPENAI_API_VERSION='2024-08-01-preview'
```

### Usage Example

```python
from pydantic_ai import Agent

# Using shorthand with environment variables
agent = Agent('azure:gpt-4o')

# Or with explicit configuration
from pydantic_ai.models.openai import OpenAIChatModel
from openai import AsyncAzureOpenAI

azure_client = AsyncAzureOpenAI(
    azure_endpoint='https://your-resource.openai.azure.com',
    api_key='your-key',
    api_version='2024-08-01-preview'
)

model = OpenAIChatModel('gpt-4o', provider=azure_client)
agent = Agent(model)
```

([Pydantic AI OpenAI Documentation][1])

## OpenAI-Compatible Providers

Pydantic AI supports numerous providers implementing OpenAI's API specification. ([Pydantic AI OpenAI Documentation][1])

### DeepSeek

Uses `DEEPSEEK_API_KEY` environment variable: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('deepseek:deepseek-chat')
```

```bash
export DEEPSEEK_API_KEY='your-deepseek-key'
```

### Ollama

Supports local servers and Ollama Cloud: ([Pydantic AI OpenAI Documentation][1])

```python
# Local server (default: http://localhost:11434/v1)
agent = Agent('ollama:llama3.1')

# Ollama Cloud
export OLLAMA_BASE_URL='https://api.ollama.com/v1'
export OLLAMA_API_KEY='your-ollama-key'
```

### OpenRouter

Requires API key from openrouter.ai/keys: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('openrouter:anthropic/claude-3.5-sonnet')
```

```bash
export OPENROUTER_API_KEY='your-openrouter-key'
```

### Grok (xAI)

Configured via `GrokProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('grok:grok-2-latest')
```

```bash
export GROK_API_KEY='your-grok-key'
```

### Fireworks AI

Accessible through `FireworksProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('fireworks:llama-v3p1-70b-instruct')
```

```bash
export FIREWORKS_API_KEY='your-fireworks-key'
```

### Together AI

Uses `TOGETHER_API_KEY` environment variable: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('together:meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo')
```

```bash
export TOGETHER_API_KEY='your-together-key'
```

### GitHub Models

Requires GitHub personal access token with `models: read` permission: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('github:gpt-4o')
```

```bash
export GITHUB_TOKEN='your-github-token'
```

### Vercel AI Gateway

Uses `VERCEL_AI_GATEWAY_API_KEY` or `VERCEL_OIDC_TOKEN`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('gateway:openai:gpt-5-nano')
```

### MoonshotAI

Uses `MOONSHOTAI_API_KEY` environment variable: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('moonshotai:moonshot-v1-8k')
```

### Cerebras

Configured via `CerebrasProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('cerebras:llama3.1-8b')
```

```bash
export CEREBRAS_API_KEY='your-cerebras-key'
```

### Nebius AI Studio

Uses `NebiusProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('nebius:meta-llama/Meta-Llama-3.1-70B-Instruct')
```

```bash
export NEBIUS_API_KEY='your-nebius-key'
```

### OVHcloud AI Endpoints

Configured through `OVHcloudProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('ovhcloud:Meta-Llama-3.1-70B-Instruct')
```

```bash
export OVHCLOUD_API_KEY='your-ovhcloud-key'
```

### Heroku AI

Requires `HEROKU_INFERENCE_KEY` and optional `HEROKU_INFERENCE_URL`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('heroku:meta-llama/Meta-Llama-3.1-70B-Instruct')
```

### Azure AI Foundry

Accessible through `AzureProvider`: ([Pydantic AI OpenAI Documentation][1])

```python
agent = Agent('azure:gpt-4o')
```

### LiteLLM

Accepts custom `api_base` and `api_key` parameters for flexible routing: ([Pydantic AI OpenAI Documentation][1])

```python
from pydantic_ai.models.openai import OpenAIChatModel

model = OpenAIChatModel(
    'gpt-4o',
    provider='litellm',
    base_url='http://localhost:4000/v1'
)
```

## vLLM, Ollama, and LM Studio

These local inference servers implement the OpenAI-compatible API, allowing use with Pydantic AI: ([Pydantic AI OpenAI Documentation][1])

### vLLM Server

```bash
# Start vLLM server
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --api-key your-key
```

```python
from pydantic_ai.models.openai import OpenAIChatModel

model = OpenAIChatModel(
    'meta-llama/Meta-Llama-3.1-8B-Instruct',
    base_url='http://localhost:8000/v1',
    api_key='your-key'
)
agent = Agent(model)
```

### Ollama

```python
from pydantic_ai import Agent

# Using Ollama provider
agent = Agent('ollama:llama3.1')
```

### LM Studio

```python
from pydantic_ai.models.openai import OpenAIChatModel

model = OpenAIChatModel(
    'local-model',
    base_url='http://localhost:1234/v1',
    api_key='not-needed'
)
agent = Agent(model)
```

## Advanced Features

### Model Profile Customization

For providers with non-standard API requirements, developers can specify `ModelProfile` or `OpenAIModelProfile` to adjust JSON schema transformation and tool definition handling. This enables compatibility with models that lack strict tool definition support or require alternative schema formats. ([Pydantic AI OpenAI Documentation][1])

```python
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelProfile

profile = OpenAIModelProfile(
    # Custom schema transformations
)

model = OpenAIChatModel('custom-model', profile=profile)
```

### Custom HTTP Configuration

Providers accept custom `http_client` parameters (AsyncClient instances) for timeout configuration, proxy settings, and connection management across all compatible endpoints: ([Pydantic AI OpenAI Documentation][1])

```python
from httpx import AsyncClient
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIProvider

http_client = AsyncClient(
    timeout=30.0,
    proxies='http://proxy.example.com:8080'
)

provider = OpenAIProvider(http_client=http_client)
model = OpenAIChatModel('gpt-4o', provider=provider)
```

## API Methods

Both `OpenAIChatModel` and `OpenAIResponsesModel` implement async request handling: ([Pydantic AI OpenAI API Reference][2])

- **`request()`**: Non-streamed API calls
- **`request_stream()`**: Streamed responses with `AsyncIterator[StreamedResponse]`

Internal methods handle message mapping, tool definitions, and JSON schema conversion for structured outputs.

## Authentication Patterns

Most providers follow a consistent pattern: ([Pydantic AI OpenAI Documentation][1])

1. Set a provider-specific API key environment variable
2. Use shorthand syntax or explicitly instantiate the provider class

This flexibility supports both simple and complex deployment scenarios.

## Complete Provider Reference

| Provider | Shorthand | Environment Variable | Base URL |
|----------|-----------|---------------------|----------|
| OpenAI | `openai:model` | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| Azure OpenAI | `azure:model` | `AZURE_OPENAI_API_KEY` | Custom endpoint |
| DeepSeek | `deepseek:model` | `DEEPSEEK_API_KEY` | API-specific |
| Ollama | `ollama:model` | `OLLAMA_API_KEY` | `http://localhost:11434/v1` |
| OpenRouter | `openrouter:model` | `OPENROUTER_API_KEY` | API-specific |
| Grok | `grok:model` | `GROK_API_KEY` | API-specific |
| Fireworks | `fireworks:model` | `FIREWORKS_API_KEY` | API-specific |
| Together AI | `together:model` | `TOGETHER_API_KEY` | API-specific |
| GitHub Models | `github:model` | `GITHUB_TOKEN` | API-specific |
| Vercel Gateway | `gateway:provider:model` | `VERCEL_AI_GATEWAY_API_KEY` | API-specific |
| MoonshotAI | `moonshotai:model` | `MOONSHOTAI_API_KEY` | API-specific |
| Cerebras | `cerebras:model` | `CEREBRAS_API_KEY` | API-specific |
| Nebius | `nebius:model` | `NEBIUS_API_KEY` | API-specific |
| OVHcloud | `ovhcloud:model` | `OVHCLOUD_API_KEY` | API-specific |
| Heroku AI | `heroku:model` | `HEROKU_INFERENCE_KEY` | API-specific |

([Pydantic AI OpenAI Documentation][1])

## Best Practices

1. **Use environment variables** for API keys to avoid hardcoding credentials
2. **Start with shorthand syntax** for simple use cases, then move to explicit configuration when needed
3. **Test locally** with Ollama or vLLM before deploying to production
4. **Configure timeouts** via custom HTTP clients for production deployments
5. **Use Azure OpenAI** for enterprise deployments requiring compliance and data residency
6. **Leverage model profiles** when working with providers that have non-standard API requirements
7. **Enable reasoning effort** for complex tasks requiring deeper analysis
8. **Use the Responses API** when you need built-in tools like web search or code execution

## References

[1]: https://ai.pydantic.dev/models/openai/index.md "Pydantic AI OpenAI Documentation"
[2]: https://ai.pydantic.dev/api/models/openai/index.md "Pydantic AI OpenAI API Reference"