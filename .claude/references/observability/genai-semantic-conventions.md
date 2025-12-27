---
author: unknown
category: observability
contributors: []
description: Comprehensive reference for OpenTelemetry Generative AI semantic conventions
  covering LLMs, embeddings, and agentic workflows
last_updated: '2025-11-01'
related:
- semantic-conventions.md
- opentelemetry-best-practices.md
- ../python/pydantic-ai/phoenix-integration.md
sources:
- name: OpenTelemetry GenAI Semantic Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- name: GenAI Span Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
- name: GenAI Event Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
- name: GenAI Metrics Conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/
- name: GenAI Attributes Registry
  url: https://opentelemetry.io/docs/specs/semconv/attributes-registry/gen-ai/
status: stable
subcategory: telemetry-standards
tags:
- opentelemetry
- genai
- llm
- ai
- semantic-conventions
- observability
- agents
- embeddings
- telemetry
- instrumentation
title: OpenTelemetry GenAI Semantic Conventions
type: standard-spec
version: '1.1'
---

# OpenTelemetry GenAI Semantic Conventions

Comprehensive reference for OpenTelemetry Generative AI semantic conventions providing standardized observability for LLMs, embeddings, agents, and AI workflows.

## Overview

OpenTelemetry GenAI semantic conventions define standardized telemetry for generative AI systems including large language models (LLMs), embedding models, and agentic workflows. ([OpenTelemetry GenAI Semantic Conventions][1])

**Purpose**: Enable consistent observability across AI applications regardless of:
- Model provider (OpenAI, Anthropic, AWS Bedrock, Azure, Google, open-source)
- Programming language or framework
- Deployment environment

**Scope**: ([OpenTelemetry GenAI Semantic Conventions][1])
- LLM inference operations (chat, completion, text generation)
- Embedding generation
- Tool/function calling
- Multi-turn conversations
- Agentic workflows

**Stability**: All GenAI conventions are currently in **Development** status, meaning they may change without notice. Organizations can opt into latest experimental versions via the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable with the value `gen_ai_latest_experimental`. ([OpenTelemetry GenAI Semantic Conventions][1])

**Important**: Existing instrumentations using v1.36.0 or earlier should NOT automatically upgrade to newer versions. Instead, implement the stability opt-in mechanism to manage transitions. ([OpenTelemetry GenAI Semantic Conventions][1])

## GenAI Spans

Three primary span types provide comprehensive AI observability. ([GenAI Span Conventions][2])

### Inference Spans

**Purpose**: Represents client calls to GenAI models that generate responses or request tool execution. ([GenAI Span Conventions][2])

**Span Naming**: `{gen_ai.operation.name} {gen_ai.request.model}` ([GenAI Span Conventions][2])

Examples:
- `chat gpt-4`
- `text_completion claude-3-opus`
- `generate_content gemini-pro`

**Span Kind**: `CLIENT` (or `INTERNAL` for same-process execution) ([GenAI Span Conventions][2])

**Status**: Follows the OpenTelemetry Recording Errors specification for error handling. ([GenAI Span Conventions][2])

#### Required Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.operation.name` | string | Operation type | `chat`, `text_completion`, `generate_content` |
| `gen_ai.provider.name` | string | Provider identifier | `openai`, `anthropic`, `aws.bedrock`, `azure`, `google`, `vertex_ai` |

([GenAI Span Conventions][2])

#### Conditionally Required

| Attribute | Condition | Description | Example | Stability |
|-----------|-----------|-------------|---------|-----------|
| `gen_ai.request.model` | If available | Model name being invoked | `gpt-4`, `claude-3-opus-20240229` | Development |
| `gen_ai.output.type` | If known | Requested output format | `text`, `json`, `image`, `speech` | Development |
| `gen_ai.conversation.id` | If available | Conversation session identifier | `uuid-123` | Development |
| `error.type` | On errors | Error classification | `timeout`, `rate_limit_exceeded`, `invalid_request` | Stable |
| `server.address` | If applicable | Server hostname or IP | `api.openai.com` | Stable |
| `server.port` | If server.address set | Server port number | `443` | Stable |

([GenAI Span Conventions][2])

#### Token Usage (Recommended)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.usage.input_tokens` | int | Tokens consumed in prompt | `150` |
| `gen_ai.usage.output_tokens` | int | Tokens generated in response | `75` |

([GenAI Span Conventions][2])

**Cost Calculation Pattern**:
```python
input_cost = input_tokens * input_price_per_1k_tokens / 1000
output_cost = output_tokens * output_price_per_1k_tokens / 1000
total_cost = input_cost + output_cost
```

#### Model Parameters (Recommended)

Capture generation settings to understand behavior and reproduce results: ([GenAI Span Conventions][2])

| Attribute | Type | Description | Typical Range |
|-----------|------|------|---------------|
| `gen_ai.request.temperature` | double | Creativity/randomness control | 0.0-2.0 |
| `gen_ai.request.top_p` | double | Nucleus sampling threshold | 0.0-1.0 |
| `gen_ai.request.top_k` | double | Top-k sampling limit | Integer |
| `gen_ai.request.max_tokens` | int | Maximum tokens to generate | Integer |
| `gen_ai.request.frequency_penalty` | double | Repetition penalty | -2.0 to 2.0 |
| `gen_ai.request.presence_penalty` | double | Topic repetition penalty | -2.0 to 2.0 |
| `gen_ai.request.stop_sequences` | string[] | Custom termination patterns | `["END", "\n\n"]` |
| `gen_ai.request.seed` | int | Deterministic generation seed (requests with same seed more likely to return same result) | Integer |
| `gen_ai.request.choice_count` | int | Target number of completions to generate | Integer |

([GenAI Attributes Registry][5])

#### Response Metadata (Recommended)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.response.finish_reasons` | string[] | Completion status per choice | `["stop"]`, `["length", "stop"]` |
| `gen_ai.response.id` | string | Unique response identifier | `chatcmpl-123` |
| `gen_ai.response.model` | string | Actual model used (may differ from request) | `gpt-4-0613` |

([GenAI Span Conventions][2])

**Finish Reasons** ([GenAI Span Conventions][2]):
- `stop`: Natural completion
- `length`: Max tokens reached
- `tool_calls`: Model requests tool execution
- `content_filter`: Content policy violation
- `function_call`: (Deprecated) Use `tool_calls`

#### Content Capture (Opt-In)

**Default Behavior**: Omit prompts and completions to minimize storage costs and privacy risks. ([GenAI Span Conventions][2])

**Opt-In Attributes**:

| Attribute | Type | Description | Format |
|-----------|------|-------------|--------|
| `gen_ai.input.messages` | JSON string | Chat history provided to model | Structured array |
| `gen_ai.output.messages` | JSON string | Model responses for each choice | Structured array |
| `gen_ai.system_instructions` | JSON string | System prompts/instructions | Structured format |
| `gen_ai.tool.definitions` | JSON string | Available tool specifications | Structured array |

([GenAI Span Conventions][2])

**Message Structure** (JSON schema): ([GenAI Span Conventions][2])

```json
{
  "role": "user|assistant|system|tool",
  "content": "Message text or structured content",
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\": \"Boston\"}"
      }
    }
  ]
}
```

**Privacy Warning**: Input/output attributes "likely to contain sensitive information including user/PII data". ([GenAI Event Conventions][3])

### Embeddings Spans

**Purpose**: Handles embedding generation operations for vector representations.

**Span Naming**: `{gen_ai.operation.name} {gen_ai.request.model}` ([GenAI Span Conventions][2])

Example: `embeddings text-embedding-3-large`

**Span Kind**: `CLIENT`

#### Key Attributes

| Attribute | Requirement | Description | Example |
|-----------|-------------|-------------|---------|
| `gen_ai.operation.name` | Required | Always `embeddings` | `embeddings` |
| `gen_ai.provider.name` | Required | Provider identifier | `openai`, `cohere`, `vertex_ai` |
| `gen_ai.request.model` | Conditionally Required | Embedding model name | `text-embedding-3-large` |
| `gen_ai.embeddings.dimension.count` | Recommended | Output vector dimensionality | `512`, `1024`, `1536`, `3072` |
| `gen_ai.request.encoding_formats` | Recommended | Requested output formats | `["float"]`, `["base64"]` |

([GenAI Span Conventions][2])

#### Token Usage

Embedding operations also consume tokens:

| Attribute | Description |
|-----------|-------------|
| `gen_ai.usage.input_tokens` | Tokens in input text |

([GenAI Span Conventions][2])

### Tool Execution Spans

**Purpose**: Captures tool/function invocation during agentic workflows.

**Span Naming**: `execute_tool {gen_ai.tool.name}` ([GenAI Span Conventions][2])

Example: `execute_tool get_weather`

**Span Kind**: `INTERNAL` (represents local processing) ([GenAI Span Conventions][2])

#### Tool-Specific Attributes

| Attribute | Requirement | Type | Description | Example |
|-----------|-------------|------|-------------|---------|
| `gen_ai.tool.name` | Recommended | string | Tool identifier | `get_weather`, `search_database` |
| `gen_ai.tool.type` | Recommended | string | Category: `function`, `extension`, `datastore` | `function` |
| `gen_ai.tool.call.id` | Recommended | string | Unique invocation identifier | `call_abc123` |
| `gen_ai.tool.call.arguments` | Opt-In | JSON string | Input parameters (structured object) | `{"location": "Boston", "units": "celsius"}` |
| `gen_ai.tool.call.result` | Opt-In | JSON string | Return value from execution | `{"temperature": 22, "conditions": "sunny"}` |

([GenAI Span Conventions][2])

#### Tool Call Workflow Pattern

```
Inference Span (chat gpt-4)
  ├─> Tool Execution Span (execute_tool get_weather)
  ├─> Tool Execution Span (execute_tool search_database)
  └─> Inference Span (chat gpt-4) [follow-up with tool results]
```

Parent inference span includes tool call requests; child spans execute tools; subsequent inference span provides tool results back to model. ([GenAI Span Conventions][2])

### Agent Spans

**Purpose**: Captures higher-level agentic behaviors and multi-step reasoning workflows. ([GenAI Span Conventions][2])

**Span Naming**: Varies based on agent framework and operation type

**Span Kind**: `INTERNAL` or `CLIENT` depending on context

#### Agent-Specific Attributes

| Attribute | Requirement | Type | Description | Example |
|-----------|-------------|------|-------------|---------|
| `gen_ai.agent.id` | Recommended | string | Unique agent identifier | `agent-uuid-123` |
| `gen_ai.agent.name` | Recommended | string | Human-readable agent name | `research_assistant` |
| `gen_ai.agent.description` | Opt-In | string | Free-form agent description | `Conducts web research and summarization` |
| `gen_ai.data_source.id` | Recommended | string | External database/storage identifier | `vector_db_prod` |

([GenAI Attributes Registry][5])

**Agent Workflow Pattern**:
```
Agent Span (research_assistant)
  ├─> Inference Span (chat gpt-4) [planning]
  ├─> Tool Execution Span (execute_tool web_search)
  ├─> Tool Execution Span (execute_tool vector_search)
  ├─> Inference Span (chat gpt-4) [synthesis]
  └─> Evaluation Event (faithfulness)
```

## GenAI Events

Two primary event types for detailed AI operation tracking. ([GenAI Event Conventions][3])

### Client Inference Operation Details Event

**Event Name**: `gen_ai.client.inference.operation.details` ([GenAI Event Conventions][3])

**Purpose**: Captures detailed content including chat history, prompts, completions, and tool interactions (Opt-In for privacy).

#### Key Attributes

| Attribute | Requirement | Type | Description |
|-----------|-------------|------|-------------|
| `gen_ai.operation.name` | Required | string | Operation type |
| `gen_ai.request.model` | Conditionally Required | string | Model name |
| `gen_ai.input.messages` | Opt-In | array | Chat history as structured array (not JSON string) |
| `gen_ai.output.messages` | Opt-In | array | Model responses as structured array |
| `gen_ai.usage.input_tokens` | Recommended | int | Input token count |
| `gen_ai.usage.output_tokens` | Recommended | int | Output token count |
| `error.type` | Conditionally Required | string | Error classification if failed |

([GenAI Event Conventions][3])

**Event vs. Span Content Attributes**:
- **Spans**: Use JSON strings for `gen_ai.input.messages`, `gen_ai.output.messages`
- **Events**: Use structured arrays directly (native types)

([GenAI Event Conventions][3])

**Security Note**: "Input and output message attributes are likely to contain sensitive information including user/PII data." ([GenAI Event Conventions][3])

### Evaluation Result Event

**Event Name**: `gen_ai.evaluation.result` ([GenAI Event Conventions][3])

**Purpose**: Captures quality, accuracy, or characteristic evaluations of GenAI outputs.

#### Key Attributes

| Attribute | Requirement | Type | Description | Example |
|-----------|-------------|------|-------------|---------|
| `gen_ai.evaluation.name` | Required | string | Evaluation metric name | `faithfulness`, `relevance`, `toxicity` |
| `gen_ai.evaluation.score.value` | Conditionally Required* | double | Numeric score | `0.95`, `8.5` |
| `gen_ai.evaluation.score.label` | Conditionally Required* | string | Categorical label | `excellent`, `pass`, `fail` |
| `gen_ai.evaluation.explanation` | Recommended | string | Reasoning for score | `Answer directly addresses question with supporting evidence` |

*At least one of `score.value` or `score.label` required. ([GenAI Event Conventions][3])

**Use Cases**:
- RAG evaluation (faithfulness, answer relevance, context relevance)
- Safety evaluation (toxicity, bias, harmful content)
- Quality evaluation (coherence, fluency, factuality)
- Custom business metrics

## GenAI Metrics

Comprehensive metrics for AI cost, performance, and usage monitoring. ([GenAI Metrics Conventions][4])

### Client-Side Metrics

#### Token Usage (Recommended)

**Metric**: `gen_ai.client.token.usage` ([GenAI Metrics Conventions][4])
- **Instrument**: Histogram
- **Unit**: `{token}`
- **Purpose**: Number of input and output tokens used
- **Status**: Development (Recommended)

**Bucket Boundaries**: `[1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, 67108864]` ([GenAI Metrics Conventions][4])

**Bucket Rationale**: Exponential scale covering single tokens to multi-million token contexts (e.g., Claude 100M token context window).

**Required Attributes**:
- `gen_ai.operation.name`
- `gen_ai.provider.name`
- `gen_ai.token.type` (input or output)

**Conditional/Recommended**:
- `gen_ai.request.model` (conditionally required if available)
- `gen_ai.response.model` (recommended)
- `server.address` (recommended)
- `server.port` (if server.address set)

**Cost Tracking Pattern**:
```python
# Record token usage
token_histogram.record(
    input_tokens,
    attributes={
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": "openai",
        "gen_ai.token.type": "input",
        "gen_ai.request.model": "gpt-4",
    }
)

# Calculate costs in application
total_cost = (input_tokens * $0.03 / 1000) + (output_tokens * $0.06 / 1000)
```

#### Operation Duration (Required)

**Metric**: `gen_ai.client.operation.duration` ([GenAI Metrics Conventions][4])
- **Instrument**: Histogram
- **Unit**: `s` (seconds)
- **Purpose**: GenAI operation duration including network latency

**Required Attributes**: Same as token usage

**Additional**:
- `error.type` (if operation failed)

**Bucket Recommendations**: `[0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24, 20.48, 40.96, 81.92]` ([GenAI Metrics Conventions][4])

### Server-Side Metrics

All server-side metrics are Recommended. ([GenAI Metrics Conventions][4])

#### Request Duration

**Metric**: `gen_ai.server.request.duration`
- **Instrument**: Histogram
- **Unit**: `s`
- **Purpose**: Time-to-last byte or last output token
- **Measures**: Total server processing time including prefill and decode

#### Time to First Token

**Metric**: `gen_ai.server.time_to_first_token`
- **Instrument**: Histogram
- **Unit**: `s`
- **Purpose**: Measures queue and prefill phase
- **Use Case**: User-perceived latency (when first token appears)

#### Time Per Output Token

**Metric**: `gen_ai.server.time_per_output_token`
- **Instrument**: Histogram
- **Unit**: `s`
- **Purpose**: Measures decode phase of LLM inference
- **Status**: Development (Recommended)
- **Calculation**: `(total_time - time_to_first_token) / (output_tokens - 1)`
- **Description**: "Time per output token generated after the first token" ([GenAI Metrics Conventions][4])

**Bucket Boundaries**: `[0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 2.5]` ([GenAI Metrics Conventions][4])

#### Time to First Token

**Metric**: `gen_ai.server.time_to_first_token`
- **Instrument**: Histogram
- **Unit**: `s`
- **Purpose**: Measures queue and prefill phase latency
- **Status**: Development (Recommended)
- **Description**: "Time to generate first token for successful responses" ([GenAI Metrics Conventions][4])
- **Use Case**: Critical for user-perceived latency (streaming experiences)

**Bucket Boundaries**: `[0.001, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]` ([GenAI Metrics Conventions][4])

**All server metrics use same required attributes as client metrics.** ([GenAI Metrics Conventions][4])

## Content Handling Strategies

Three approaches for managing AI content with varying privacy/cost trade-offs. ([GenAI Span Conventions][2])

### Strategy 1: No Capture (Default, Recommended)

**Approach**: Omit `gen_ai.input.messages`, `gen_ai.output.messages`, tool arguments/results entirely.

**Advantages**:
- No PII exposure
- Minimal storage costs
- Fast span processing

**Disadvantages**:
- Cannot debug prompt issues
- Cannot reproduce exact interactions
- Limited error analysis

**Use When**: Privacy regulations prohibit content storage, or cost minimization is critical.

### Strategy 2: Direct Attribute Storage (Opt-In)

**Approach**: Record content on spans via attributes, on events via structured arrays.

**Span Attributes** (JSON strings):
```python
span.set_attribute("gen_ai.input.messages", json.dumps([
    {"role": "user", "content": "What is the capital of France?"}
]))
span.set_attribute("gen_ai.output.messages", json.dumps([
    {"role": "assistant", "content": "The capital of France is Paris."}
]))
```

**Event Attributes** (native arrays):
```python
span.add_event("gen_ai.client.inference.operation.details", attributes={
    "gen_ai.input.messages": [
        {"role": "user", "content": "What is the capital of France?"}
    ],
    "gen_ai.output.messages": [
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]
})
```

**Advantages**:
- Immediate content access in traces
- Simple implementation
- No external dependencies

**Disadvantages**:
- High storage costs for long conversations
- PII in observability backend
- Span size limits may be exceeded

**Use When**: Development/staging environments, short interactions, controlled data.

### Strategy 3: External Storage with References (Production)

**Approach**: Upload content externally (S3, blob storage), store references on spans.

**Pattern**:
```python
# Upload content
content_id = upload_to_storage({
    "input": messages,
    "output": completions,
    "timestamp": datetime.now()
})

# Store reference
span.set_attribute("gen_ai.content.reference.id", content_id)
span.set_attribute("gen_ai.content.reference.url", f"s3://bucket/{content_id}")
```

**Advantages**:
- Scalable for large content
- Separate retention policies
- Reduced span sizes
- Can apply encryption at rest

**Disadvantages**:
- Additional infrastructure
- Retrieval latency
- Coordination between systems

**Use When**: Production environments, long conversations, compliance requirements, cost optimization.

## PII Protection Patterns

### Content Filtering

**Before Recording**:
```python
def sanitize_content(messages):
    for msg in messages:
        # Remove email addresses
        msg['content'] = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', msg['content'])
        # Remove phone numbers
        msg['content'] = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', msg['content'])
        # Remove credit cards
        msg['content'] = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CC]', msg['content'])
    return messages

span.set_attribute("gen_ai.input.messages", json.dumps(sanitize_content(messages)))
```

### Hashing Identifiers

**For User Tracking without PII**:
```python
import hashlib

user_id_hash = hashlib.sha256(user_id.encode()).hexdigest()
span.set_attribute("user.id.hash", user_id_hash)  # Pseudonymized
```

### Truncation

**Limit Content Length**:
```python
def truncate_messages(messages, max_chars=500):
    for msg in messages:
        if len(msg['content']) > max_chars:
            msg['content'] = msg['content'][:max_chars] + "... [truncated]"
    return messages
```

### Consent-Based Capture

**Conditional Recording**:
```python
if user.has_opted_in_to_telemetry():
    span.set_attribute("gen_ai.input.messages", json.dumps(messages))
```

## Provider-Specific Patterns

### OpenAI

**Provider Name**: `openai` ([GenAI Attributes Registry][5])

**Common Models**: `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-3.5-turbo`, `text-embedding-3-large`, `text-embedding-3-small`

**OpenAI-Specific Extensions**:
```python
span.set_attributes({
    "gen_ai.provider.name": "openai",
    "gen_ai.request.model": "gpt-4",
    "gen_ai.openai.request.organization": "org-abc123",  # Custom extension
    "gen_ai.openai.request.user": user_hash,  # End-user tracking
})
```

### Anthropic

**Provider Name**: `anthropic` ([GenAI Attributes Registry][5])

**Common Models**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`

**Anthropic-Specific Patterns**:
- Use `gen_ai.system_instructions` for system prompts (Claude requires explicit system messages)
- Tool calling uses structured format similar to OpenAI

### AWS Bedrock

**Provider Name**: `aws.bedrock` ([GenAI Attributes Registry][5])

**Model Discrimination**:
```python
# Bedrock hosts multiple providers
span.set_attributes({
    "gen_ai.provider.name": "aws.bedrock",
    "gen_ai.request.model": "anthropic.claude-3-sonnet-20240229-v1:0",
    "cloud.provider": "aws",
    "cloud.platform": "aws_bedrock",
})
```

### Azure OpenAI

**Provider Names**: `azure.ai.openai` (Azure OpenAI Service), `azure.ai.inference` (Azure AI Inference API) ([GenAI Attributes Registry][5])

**Deployment-Specific**:
```python
span.set_attributes({
    "gen_ai.provider.name": "azure",
    "gen_ai.request.model": "gpt-4",  # Base model
    "gen_ai.azure.deployment_name": "my-gpt4-deployment",  # Custom extension
    "server.address": "myresource.openai.azure.com",
    "cloud.provider": "azure",
})
```

### Google Vertex AI / Gemini

**Provider Names**: `vertex_ai`, `google` ([GenAI Attributes Registry][5])

**Common Models**: `gemini-pro`, `gemini-pro-vision`, `text-bison`, `chat-bison`

**Vertex AI Pattern**:
```python
span.set_attributes({
    "gen_ai.provider.name": "vertex_ai",
    "gen_ai.request.model": "gemini-pro",
    "cloud.provider": "gcp",
    "cloud.platform": "gcp_vertex_ai",
})
```

### Open-Source Models (Ollama, vLLM)

**Provider Names**: Use specific identifier such as `ollama`, `vllm`, or custom values

**Local Deployment**:
```python
span.set_attributes({
    "gen_ai.provider.name": "ollama",
    "gen_ai.request.model": "llama2:70b",
    "server.address": "localhost",
    "server.port": 11434,
    "deployment.environment.name": "local",
})
```

### Other Notable Providers

**Additional Well-Known Providers** ([GenAI Attributes Registry][5]):
- `cohere` - Cohere LLM and embedding models
- `deepseek` - DeepSeek AI models
- `gcp.gemini` - Google Gemini API
- `gcp.gen_ai` - Google GenAI Studio
- `groq` - Groq inference platform
- `ibm.watsonx.ai` - IBM watsonx.ai
- `mistral_ai` - Mistral AI models
- `perplexity` - Perplexity AI
- `x_ai` - xAI (formerly Twitter AI)

## Agentic Workflow Patterns

### Multi-Turn Conversations

**Conversation Tracking**:
```python
conversation_id = str(uuid.uuid4())

# First turn
with tracer.start_as_current_span("chat gpt-4") as span:
    span.set_attributes({
        "gen_ai.conversation.id": conversation_id,  # Custom extension
        "gen_ai.conversation.turn": 1,
    })

# Second turn
with tracer.start_as_current_span("chat gpt-4") as span:
    span.set_attributes({
        "gen_ai.conversation.id": conversation_id,
        "gen_ai.conversation.turn": 2,
    })
```

### Tool Calling Workflow

**Complete Trace Structure**:
```
Inference Span (chat gpt-4) - Request with tool definitions
  ├─> Tool Execution Span (execute_tool get_weather)
  ├─> Tool Execution Span (execute_tool search_database)
Inference Span (chat gpt-4) - Provide tool results, get final answer
```

**Implementation**:
```python
# Step 1: Initial request
with tracer.start_as_current_span("chat gpt-4") as inference_span:
    inference_span.set_attributes({
        "gen_ai.operation.name": "chat",
        "gen_ai.request.model": "gpt-4",
    })

    response = client.chat(
        messages=[{"role": "user", "content": "What's the weather in Boston?"}],
        tools=[get_weather_tool_definition]
    )

    if response.finish_reason == "tool_calls":
        tool_calls = response.tool_calls

        # Step 2: Execute tools
        tool_results = []
        for tool_call in tool_calls:
            with tracer.start_as_current_span(f"execute_tool {tool_call.function.name}") as tool_span:
                tool_span.set_attributes({
                    "gen_ai.tool.name": tool_call.function.name,
                    "gen_ai.tool.call.id": tool_call.id,
                })

                result = execute_tool(tool_call.function.name, tool_call.function.arguments)
                tool_results.append(result)

        # Step 3: Provide results back to model
        with tracer.start_as_current_span("chat gpt-4") as final_span:
            final_span.set_attributes({
                "gen_ai.operation.name": "chat",
                "gen_ai.request.model": "gpt-4",
            })

            final_response = client.chat(
                messages=[
                    {"role": "user", "content": "What's the weather in Boston?"},
                    {"role": "assistant", "tool_calls": tool_calls},
                    *[{"role": "tool", "content": str(r)} for r in tool_results]
                ]
            )
```

### Reasoning Traces

**Pattern for Chain-of-Thought**:
```python
with tracer.start_as_current_span("reasoning_chain") as parent:
    parent.set_attribute("gen_ai.reasoning.type", "chain_of_thought")

    # Step 1: Decompose problem
    with tracer.start_as_current_span("chat gpt-4") as span:
        span.set_attribute("gen_ai.reasoning.step", "decomposition")

    # Step 2: Solve subproblems
    for i, subproblem in enumerate(subproblems):
        with tracer.start_as_current_span("chat gpt-4") as span:
            span.set_attribute("gen_ai.reasoning.step", f"solve_{i}")

    # Step 3: Synthesize answer
    with tracer.start_as_current_span("chat gpt-4") as span:
        span.set_attribute("gen_ai.reasoning.step", "synthesis")
```

## Complete Examples

### Basic Inference Span

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("chat gpt-4", kind=SpanKind.CLIENT) as span:
    # Required
    span.set_attributes({
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": "openai",
        "gen_ai.request.model": "gpt-4",
    })

    # Model parameters (Recommended)
    span.set_attributes({
        "gen_ai.request.temperature": 0.7,
        "gen_ai.request.max_tokens": 500,
        "gen_ai.request.top_p": 0.9,
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "What is OpenTelemetry?"}],
            temperature=0.7,
            max_tokens=500,
        )

        # Token usage (Recommended)
        span.set_attributes({
            "gen_ai.usage.input_tokens": response.usage.prompt_tokens,
            "gen_ai.usage.output_tokens": response.usage.completion_tokens,
        })

        # Response metadata (Recommended)
        span.set_attributes({
            "gen_ai.response.id": response.id,
            "gen_ai.response.model": response.model,
            "gen_ai.response.finish_reasons": [choice.finish_reason for choice in response.choices],
        })

    except Exception as e:
        span.set_status(Status(StatusCode.ERROR))
        span.set_attribute("error.type", type(e).__name__)
        span.record_exception(e)
        raise
```

### Embeddings Span

```python
with tracer.start_as_current_span("embeddings text-embedding-3-large", kind=SpanKind.CLIENT) as span:
    span.set_attributes({
        "gen_ai.operation.name": "embeddings",
        "gen_ai.provider.name": "openai",
        "gen_ai.request.model": "text-embedding-3-large",
        "gen_ai.embeddings.dimension.count": 3072,
    })

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input="OpenTelemetry provides observability for AI systems"
    )

    span.set_attribute("gen_ai.usage.input_tokens", response.usage.prompt_tokens)
```

### Tool Execution Span

```python
with tracer.start_as_current_span("execute_tool get_weather", kind=SpanKind.INTERNAL) as span:
    span.set_attributes({
        "gen_ai.tool.name": "get_weather",
        "gen_ai.tool.type": "function",
        "gen_ai.tool.call.id": "call_abc123",
    })

    # Opt-In: Record arguments
    arguments = {"location": "Boston", "units": "celsius"}
    span.set_attribute("gen_ai.tool.call.arguments", json.dumps(arguments))

    # Execute tool
    result = get_weather(**arguments)

    # Opt-In: Record result
    span.set_attribute("gen_ai.tool.call.result", json.dumps(result))
```

### Evaluation Event

```python
span.add_event(
    "gen_ai.evaluation.result",
    attributes={
        "gen_ai.evaluation.name": "faithfulness",
        "gen_ai.evaluation.score.value": 0.95,
        "gen_ai.evaluation.explanation": "Response accurately reflects source documents with no hallucinations",
    }
)
```

### Token Usage Metric

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
token_histogram = meter.create_histogram(
    name="gen_ai.client.token.usage",
    unit="{token}",
    description="Number of input and output tokens used",
)

# Record input tokens
token_histogram.record(
    150,
    attributes={
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": "openai",
        "gen_ai.token.type": "input",
        "gen_ai.request.model": "gpt-4",
        "server.address": "api.openai.com",
    }
)

# Record output tokens
token_histogram.record(
    75,
    attributes={
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": "openai",
        "gen_ai.token.type": "output",
        "gen_ai.request.model": "gpt-4",
        "server.address": "api.openai.com",
    }
)
```

## Deprecated Attributes

The following attributes have been deprecated and should not be used in new implementations. ([GenAI Attributes Registry][5])

| Deprecated Attribute | Replacement | Notes |
|---------------------|-------------|-------|
| `gen_ai.system` | `gen_ai.provider.name` | Provider identification standardized |
| `gen_ai.usage.prompt_tokens` | `gen_ai.usage.input_tokens` | Terminology alignment |
| `gen_ai.usage.completion_tokens` | `gen_ai.usage.output_tokens` | Terminology alignment |
| `gen_ai.prompt` | *Removed* | Use `gen_ai.input.messages` instead |
| `gen_ai.completion` | *Removed* | Use `gen_ai.output.messages` instead |
| `gen_ai.openai.*` | Provider-agnostic equivalents | OpenAI-specific attributes replaced |

**Migration Path**: Update instrumentation to use replacement attributes. The deprecated attributes may be removed in future stable versions.

## Attribute Quick Reference

### Operation Attributes

| Attribute | Requirement | Values |
|-----------|-------------|--------|
| `gen_ai.operation.name` | Required | `chat`, `text_completion`, `generate_content`, `embeddings`, `create_agent`, `invoke_agent`, `execute_tool` |
| `gen_ai.provider.name` | Required | `openai`, `anthropic`, `aws.bedrock`, `azure.ai.openai`, `azure.ai.inference`, `gcp.gemini`, `gcp.vertex_ai`, `google`, `cohere`, `mistral_ai`, `groq`, `deepseek`, `ibm.watsonx.ai`, `perplexity`, `x_ai`, `ollama` |

### Model Attributes

| Attribute | Requirement | Example |
|-----------|-------------|---------|
| `gen_ai.request.model` | Conditionally Required | `gpt-4`, `claude-3-opus-20240229` |
| `gen_ai.response.model` | Recommended | `gpt-4-0613` |
| `gen_ai.response.id` | Recommended | `chatcmpl-123` |

### Token Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.usage.input_tokens` | int | Input/prompt tokens |
| `gen_ai.usage.output_tokens` | int | Generated/completion tokens |
| `gen_ai.token.type` | string | `input` or `output` (metrics only) |

### Request Parameters

| Attribute | Type | Range |
|-----------|------|-------|
| `gen_ai.request.temperature` | double | 0.0-2.0 |
| `gen_ai.request.top_p` | double | 0.0-1.0 |
| `gen_ai.request.top_k` | int | Integer |
| `gen_ai.request.max_tokens` | int | Integer |
| `gen_ai.request.frequency_penalty` | double | -2.0 to 2.0 |
| `gen_ai.request.presence_penalty` | double | -2.0 to 2.0 |

### Tool Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.tool.name` | string | Tool identifier |
| `gen_ai.tool.type` | string | `function`, `extension`, `datastore` |
| `gen_ai.tool.call.id` | string | Unique call identifier |
| `gen_ai.tool.call.arguments` | JSON string | Input parameters |
| `gen_ai.tool.call.result` | JSON string | Return value |


## Related References

- [Semantic Conventions](semantic-conventions.md) - Broader OpenTelemetry conventions context
- [OpenTelemetry Best Practices](opentelemetry-best-practices.md) - Implementation patterns
- [Pydantic AI Phoenix Integration](../pydantic-ai/phoenix-integration.md) - Practical AI agent integration

[1]: https://opentelemetry.io/docs/specs/semconv/gen-ai/ "OpenTelemetry GenAI Semantic Conventions"
[2]: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ "GenAI Span Conventions"
[3]: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/ "GenAI Event Conventions"
[4]: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/ "GenAI Metrics Conventions"
[5]: https://opentelemetry.io/docs/specs/semconv/attributes-registry/gen-ai/ "GenAI Attributes Registry"