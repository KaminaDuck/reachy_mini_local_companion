---
author: unknown
category: observability
contributors: []
description: Comprehensive reference for OpenInference span kinds with examples and
  patterns
last_updated: '2025-01-15'
related:
- docker-compose-deployment.md
- tracing-links.md
sources:
- name: OpenInference Semantic Conventions
  url: https://arize-ai.github.io/openinference/spec/semantic_conventions.html
- name: Phoenix Tracing Documentation
  url: https://arize.com/docs/phoenix/tracing
status: stable
subcategory: tracing
tags:
- tracing
- openinference
- spans
- patterns
- observability
- phoenix
- llm
title: OpenInference Span Kinds Reference
type: pattern-reference
version: '1.0'
---

# OpenInference Span Kinds - Complete Reference

## Overview

OpenInference defines semantic span kinds that classify operations in LLM applications. Each span kind has specific attributes and use cases, enabling Phoenix to render traces appropriately in the UI.

**Reference Documentation:**
- [OpenInference Semantic Conventions Spec](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)
- [What are Traces - Span Kinds](file://.local/references/phoenix/docs/tracing/concepts-tracing/what-are-traces.md#L60-L92)
- [Manual Instrumentation Guide](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md)
- [Base OTEL Setup](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/custom-spans.md)

---

## 1. CHAIN

**Definition:** A starting point or link between different LLM application steps. Represents general logic operations, functions, or code blocks that connect components.

**Use Cases:**
- Entry point for LLM application requests
- Glue code passing context from retriever to LLM
- General orchestration logic
- Business logic functions

**Key Attributes:**
- `openinference.span.kind` = "CHAIN"
- `input.value` - Input to the chain
- `output.value` - Output from the chain

**Example (Decorator):**
```python
from phoenix.otel import register

tracer_provider = register(project_name="my-app")
tracer = tracer_provider.get_tracer(__name__)

@tracer.chain
def my_orchestration_logic(input: str) -> str:
    # Business logic here
    return "processed output"
```

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "chain-span-name",
    openinference_span_kind="chain",
) as span:
    span.set_input("input data")
    result = process_data()
    span.set_output(result)
    span.set_status(Status(StatusCode.OK))
```

**Documentation:**
- [Chain Examples](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md#L108-L151)
- [Arize Docs: Chains](https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/instrument-python#chains)

---

## 2. LLM

**Definition:** Represents a call to a Large Language Model for chat completions or text generation.

**Use Cases:**
- OpenAI, Anthropic, Llama, or other LLM API calls
- Chat completions
- Text generation
- Streaming responses

**Key Attributes:**
- `openinference.span.kind` = "LLM"
- `llm.model_name` - Model identifier (e.g., "gpt-4", "claude-3-5-sonnet")
- `llm.system` - Provider (e.g., "openai", "anthropic")
- `llm.input_messages` - Array of input messages with role/content
- `llm.output_messages` - Array of output messages
- `llm.token_count.prompt` - Input token count
- `llm.token_count.completion` - Output token count
- `llm.token_count.total` - Total tokens
- `llm.invocation_parameters` - Model parameters (temperature, max_tokens, etc.)
- `llm.tools` - Available tools for function calling

**Example (Decorator):**
```python
from openai import OpenAI

openai_client = OpenAI()

@tracer.llm
def invoke_llm(messages: List[ChatCompletionMessageParam]) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content or ""

invoke_llm([{"role": "user", "content": "Hello, world!"}])
```

**Example (Context Manager):**
```python
messages = [{"role": "user", "content": "Hello, world!"}]
with tracer.start_as_current_span("llm_span", openinference_span_kind="llm") as span:
    span.set_input(messages)
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
    except Exception as error:
        span.record_exception(error)
        span.set_status(Status(StatusCode.ERROR))
    else:
        span.set_output(response)
        span.set_status(Status(StatusCode.OK))
```

**Auto-Instrumentation:**
```python
from phoenix.otel import register

# Auto-instrument OpenAI
tracer_provider = register(
    project_name="my-llm-app",
    auto_instrument=True  # Automatically traces OpenAI calls
)
```

**Documentation:**
- [LLM Span Examples](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md#L228-L335)
- [OpenAI Integration](file://.local/references/phoenix/docs/section-integrations/llm-providers/openai/openai-tracing.md)
- [Arize Docs: LLM Tracing](https://arize.com/docs/phoenix/integrations/openai)
- [OpenInference LLM Attributes](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)

---

## 3. TOOL

**Definition:** Represents a call to an external tool such as calculators, APIs, weather services, or any function execution invoked by an LLM.

**Use Cases:**
- Function calls during LLM agent execution
- External API calls (weather, calculator, database queries)
- Custom tool implementations
- LLM function calling tools

**Key Attributes:**
- `openinference.span.kind` = "TOOL"
- `tool.name` - Name of the tool
- `tool.description` - Tool description
- `tool.parameters` - Input parameters
- `tool.json_schema` - JSON schema for tool definition
- `input.value` - Tool input
- `output.value` - Tool output

**Example (Decorator):**
```python
@tracer.tool
def get_weather(city: str, units: str = "celsius") -> str:
    """
    Fetches current weather for a given city.
    """
    # Call weather API
    return f"Weather in {city}: 22°{units[0].upper()}"

# Tool metadata automatically extracted from function signature and docstring
get_weather("San Francisco", units="fahrenheit")
```

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "tool-span",
    openinference_span_kind="tool",
) as span:
    span.set_input("San Francisco")
    span.set_tool(
        name="get_weather",
        description="Fetches weather for a city",
        parameters={"city": "San Francisco", "units": "celsius"},
    )
    result = call_weather_api("San Francisco")
    span.set_output(result)
    span.set_status(Status(StatusCode.OK))
```

**Example (With LLM Function Calling):**
```python
from openai import OpenAI

openai_client = OpenAI()

@tracer.tool
def calculate(expression: str) -> float:
    """Evaluates a mathematical expression"""
    return eval(expression)  # Use safe_eval in production

# LLM can call this tool
tools = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluates a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"}
            },
            "required": ["expression"]
        }
    }
}]
```

**Documentation:**
- [Tool Examples](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md#L180-L224)
- [Arize Docs: Tools](https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/instrument-python#tools)

---

## 4. AGENT

**Definition:** High-level span encompassing calls to LLMs and Tools. Represents a reasoning block that acts on tools using LLM guidance.

**Use Cases:**
- Top-level or near top-level span for agent invocations
- ReAct agent patterns
- Multi-step reasoning with tool usage
- Autonomous agent workflows

**Key Attributes:**
- `openinference.span.kind` = "AGENT"
- `agent.name` - Agent identifier
- `input.value` - Agent input/query
- `output.value` - Agent final response
- Child spans: LLM and TOOL spans

**Example (Decorator):**
```python
@tracer.agent
def research_agent(query: str) -> str:
    """
    Multi-step agent that researches a topic using tools and LLM reasoning.
    """
    # Agent logic with LLM calls and tool usage
    return "Research findings..."

research_agent("What are the latest AI developments?")
```

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "agent-span",
    openinference_span_kind="agent",
) as span:
    span.set_input("User query")
    span.set_attribute("agent.name", "research_agent")

    # Agent orchestration logic
    response = execute_agent_loop()

    span.set_output(response)
    span.set_status(Status(StatusCode.OK))
```

**Example (Real Implementation):**
```python
from openinference.semconv.trace import SpanAttributes
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def agent_router(message, context):
    """Agent with routing logic"""
    with tracer.start_as_current_span("code_based_agent") as span:
        span.set_attribute(SpanAttributes.INPUT_VALUE, message)
        span.set_attribute(SpanAttributes.OPENINFERENCE_SPAN_KIND, "AGENT")

        # Route to appropriate tools/LLMs
        agent_response = router(message, context)

        span.set_attribute(SpanAttributes.OUTPUT_VALUE, agent_response)
        span.set_status(trace.Status(trace.StatusCode.OK))
        return agent_response
```

**Documentation:**
- [Agent Examples](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md#L154-L176)
- [Agent Framework Example](file://.local/references/phoenix/examples/agent_framework_comparison/code_based_agent/main.py)
- [Arize Docs: Agents](https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/instrument-python#agents)

---

## 5. RETRIEVER

**Definition:** Represents a data retrieval step, typically from vector stores, databases, or document stores.

**Use Cases:**
- Vector similarity search
- Database queries for context
- Document retrieval from knowledge bases
- RAG (Retrieval-Augmented Generation) retrieval step

**Key Attributes:**
- `openinference.span.kind` = "RETRIEVER"
- `retrieval.documents` - Array of retrieved documents
  - `retrieval.documents.N.document.id` - Document identifier
  - `retrieval.documents.N.document.content` - Document text/content
  - `retrieval.documents.N.document.score` - Relevance score
  - `retrieval.documents.N.document.metadata` - Document metadata (JSON)
- `input.value` - Query used for retrieval

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "retrieve_documents",
    openinference_span_kind="retriever",
) as span:
    span.set_input("user query about postal service")

    # Perform vector search
    results = vector_store.similarity_search(query, k=3)

    # Set retrieved documents
    for idx, doc in enumerate(results):
        span.set_attribute(f"retrieval.documents.{idx}.document.id", doc.id)
        span.set_attribute(f"retrieval.documents.{idx}.document.content", doc.text)
        span.set_attribute(f"retrieval.documents.{idx}.document.score", doc.score)
        span.set_attribute(f"retrieval.documents.{idx}.document.metadata",
                          json.dumps(doc.metadata))

    span.set_status(Status(StatusCode.OK))
```

**Example Span (from traces):**
```json
{
    "name": "retrieve",
    "attributes": {
        "openinference.span.kind": "RETRIEVER",
        "input.value": "tell me about postal service",
        "retrieval.documents.0.document.id": "6d4e27be-1d6d-4084-a619-351a44834f38",
        "retrieval.documents.0.document.score": 0.7711453293100421,
        "retrieval.documents.0.document.content": "<document-chunk-1>",
        "retrieval.documents.0.document.metadata": "{\"page_label\": \"7\", \"file_name\": \"101.pdf\"}"
    }
}
```

**Auto-Instrumentation (LlamaIndex):**
```python
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register
from llama_index.core import VectorStoreIndex

tracer_provider = register()
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

# Retriever spans automatically created
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")  # RETRIEVER spans auto-traced
```

**Documentation:**
- [Retriever Span Example](file://.local/references/phoenix/docs/tracing/concepts-tracing/what-are-traces.md#L145-L185)
- [LlamaIndex Integration](file://.local/references/phoenix/docs/section-integrations/python/llamaindex/llamaindex-tracing.md)
- [RAG Evaluation Guide](file://.local/references/phoenix/docs/use-cases/rag-evaluation.md)

---

## 6. RERANKER

**Definition:** Represents the reranking of a set of input documents, typically using cross-encoders to compute relevance scores.

**Use Cases:**
- Reranking retrieved documents by relevance
- Cross-encoder scoring
- Top-K selection from retrieved candidates
- Improving RAG precision

**Key Attributes:**
- `openinference.span.kind` = "RERANKER"
- `reranker.model_name` - Reranker model identifier
- `reranker.query` - Query used for reranking
- `reranker.input_documents` - Documents before reranking
- `reranker.output_documents` - Documents after reranking (top-K)
- `reranker.top_k` - Number of documents returned

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "rerank_documents",
    openinference_span_kind="reranker",
) as span:
    query = "What are the benefits of RAG?"
    span.set_attribute("reranker.query", query)
    span.set_attribute("reranker.model_name", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    span.set_attribute("reranker.top_k", 5)

    # Rerank documents
    reranked_docs = cross_encoder.rerank(query, retrieved_documents, top_k=5)

    span.set_output(reranked_docs)
    span.set_status(Status(StatusCode.OK))
```

**Use in RAG Pipeline:**
```python
# Full RAG pipeline with RETRIEVER and RERANKER spans
@tracer.chain
def rag_pipeline(query: str) -> str:
    # RETRIEVER span (auto-instrumented or manual)
    documents = vector_store.similarity_search(query, k=20)

    # RERANKER span
    with tracer.start_as_current_span("rerank", openinference_span_kind="reranker") as span:
        span.set_attribute("reranker.query", query)
        span.set_attribute("reranker.top_k", 5)
        top_docs = reranker.rerank(query, documents, top_k=5)

    # LLM span
    context = "\n".join([doc.content for doc in top_docs])
    response = llm.invoke(f"Context: {context}\n\nQuestion: {query}")

    return response
```

**Documentation:**
- [OpenInference Reranker Spec](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)
- [Span Kinds Overview](file://.local/references/phoenix/docs/tracing/concepts-tracing/what-are-traces.md#L74-L76)

---

## 7. EMBEDDING

**Definition:** Represents a call to an LLM or embedding service for generating vector embeddings.

**Use Cases:**
- Generating embeddings for queries
- Document embedding during indexing
- Semantic similarity calculations
- OpenAI ada-2, Cohere, or other embedding models

**Key Attributes:**
- `openinference.span.kind` = "EMBEDDING"
- `embedding.model_name` - Embedding model identifier
- `embedding.text` - Input text for embedding
- `embedding.embeddings` - Array of generated embeddings
- `embedding.vector` - The embedding vector

**Example (Context Manager):**
```python
with tracer.start_as_current_span(
    "generate_embedding",
    openinference_span_kind="embedding",
) as span:
    text = "What is Phoenix tracing?"
    span.set_attribute("embedding.model_name", "text-embedding-ada-002")
    span.set_attribute("embedding.text", text)

    # Generate embedding
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    embedding_vector = response.data[0].embedding

    span.set_attribute("embedding.vector", embedding_vector)
    span.set_status(Status(StatusCode.OK))
```

**Auto-Instrumentation (OpenAI):**
```python
from phoenix.otel import register

# Auto-instruments embedding calls
tracer_provider = register(auto_instrument=True)

# EMBEDDING spans automatically created
import openai
client = openai.OpenAI()
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello world"
)
```

**Documentation:**
- [Embedding Span Kind](file://.local/references/phoenix/docs/tracing/concepts-tracing/what-are-traces.md#L82-L84)
- [OpenAI Integration](file://.local/references/phoenix/docs/section-integrations/llm-providers/openai/openai-tracing.md)

---

## 8. GUARDRAIL

**Definition:** Represents guardrail checks that protect against jailbreaks by modifying or rejecting LLM responses containing undesirable content.

**Use Cases:**
- Content filtering and safety checks
- PII detection and redaction
- Toxicity detection
- Output validation
- Input sanitization
- Compliance checks

**Key Attributes:**
- `openinference.span.kind` = "GUARDRAIL"
- `input.value` - Content being checked
- `output.value` - Filtered/modified content or validation result
- Custom attributes for specific guardrail types

**Example (Guardrails AI):**
```python
from guardrails import Guard
from guardrails.hub import TwoWords
from phoenix.otel import register

# Setup tracing
tracer_provider = register(
    project_name="my-llm-app",
    auto_instrument=True
)

# Use guardrails
guard = Guard().use(TwoWords())
response = guard(
    llm_api=openai.chat.completions.create,
    prompt="What is another name for America?",
    model="gpt-3.5-turbo",
)
# GUARDRAIL spans automatically created
```

**Example (Manual):**
```python
with tracer.start_as_current_span(
    "content_filter",
    openinference_span_kind="guardrail",
) as span:
    span.set_input(llm_response)

    # Check for toxic content
    is_safe = toxicity_checker.check(llm_response)

    if not is_safe:
        filtered_response = "[Content filtered]"
        span.set_attribute("guardrail.action", "reject")
    else:
        filtered_response = llm_response
        span.set_attribute("guardrail.action", "pass")

    span.set_output(filtered_response)
    span.set_status(Status(StatusCode.OK))
```

**Documentation:**
- [Guardrails AI Integration](file://.local/references/phoenix/docs/section-integrations/python/guardrails-ai/guardrails-ai-tracing.md)
- [Guardrails AI Framework](https://www.guardrailsai.com/)
- [OpenInference Guardrail Spec](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)

---

## 9. EVALUATOR

**Definition:** Represents a call to a function or process performing evaluation of language model outputs.

**Use Cases:**
- LLM-as-judge evaluation
- Automated quality scoring
- Hallucination detection
- Relevance scoring
- Answer correctness evaluation
- Typically used by Phoenix during automatic evaluation tracing

**Key Attributes:**
- `openinference.span.kind` = "EVALUATOR"
- `input.value` - Content being evaluated
- `output.value` - Evaluation result/score
- Custom evaluation metrics

**Example (Manual Evaluation):**
```python
with tracer.start_as_current_span(
    "evaluate_response",
    openinference_span_kind="evaluator",
) as span:
    span.set_input({
        "question": question,
        "answer": llm_response,
        "context": retrieved_docs
    })

    # Run evaluation
    eval_result = evaluator.evaluate(
        question=question,
        answer=llm_response,
        context=retrieved_docs
    )

    span.set_attribute("evaluation.score", eval_result.score)
    span.set_attribute("evaluation.reasoning", eval_result.reasoning)
    span.set_output(eval_result)
    span.set_status(Status(StatusCode.OK))
```

**Phoenix Automatic Evaluation:**
```python
import phoenix as px
from phoenix.evals import OpenAIModel, llm_classify

# Phoenix automatically creates EVALUATOR spans
eval_model = OpenAIModel(model="gpt-4")

# Run evaluations - EVALUATOR spans auto-created
rails = ["hallucination", "relevance", "toxicity"]
for rail in rails:
    px.Client().log_evaluations(
        SpanEvaluations(eval_name=rail, dataframe=eval_df)
    )
```

**Documentation:**
- [LLM Evaluations Guide](file://.local/references/phoenix/docs/tracing/how-to-tracing/feedback-and-annotations/llm-evaluations.md)
- [Span Kinds Table](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md#L95-L106)

---

## 10. UNKNOWN

**Definition:** Default span kind when the operation type is not specified or doesn't fit other categories.

**Use Cases:**
- Fallback for unclassified operations
- Custom operations without specific semantic meaning
- Temporary spans during development

**Key Attributes:**
- `openinference.span.kind` = "UNKNOWN"

**Example:**
```python
with tracer.start_as_current_span(
    "custom_operation",
    openinference_span_kind="unknown",
) as span:
    span.set_input(data)
    result = custom_processing(data)
    span.set_output(result)
```

---

## Complete Span Kind Table

| Span Kind | Primary Use | Typical Position | Auto-Instrumented |
|-----------|-------------|------------------|-------------------|
| **CHAIN** | Orchestration logic, entry points | Top/mid-level | Framework-dependent |
| **LLM** | Language model API calls | Mid-level | ✓ (OpenAI, Anthropic, etc.) |
| **TOOL** | External function/API calls | Leaf nodes | Framework-dependent |
| **AGENT** | Multi-step reasoning with tools | Top-level | Framework-dependent |
| **RETRIEVER** | Document/data retrieval | Mid-level | ✓ (LlamaIndex, LangChain) |
| **RERANKER** | Document reranking | Mid-level | Framework-dependent |
| **EMBEDDING** | Embedding generation | Leaf nodes | ✓ (OpenAI, Cohere) |
| **GUARDRAIL** | Safety/validation checks | Any level | ✓ (Guardrails AI) |
| **EVALUATOR** | Quality evaluation | Any level | ✓ (Phoenix evals) |
| **UNKNOWN** | Unclassified operations | Any level | N/A |

---

## Common Patterns

### RAG Pipeline
```
CHAIN (rag_pipeline)
├── EMBEDDING (query_embedding)
├── RETRIEVER (vector_search)
├── RERANKER (rerank_top_k)
└── LLM (generate_answer)
```

### Agent with Tools
```
AGENT (research_agent)
├── LLM (reasoning_step_1)
├── TOOL (web_search)
├── LLM (reasoning_step_2)
├── TOOL (calculator)
└── LLM (final_answer)
```

### Safe LLM Call
```
CHAIN (safe_llm_pipeline)
├── GUARDRAIL (input_validation)
├── LLM (generate_response)
└── GUARDRAIL (output_filtering)
```

---

## Additional Resources

**Official Documentation:**
- [Phoenix Tracing Documentation](https://arize.com/docs/phoenix/tracing)
- [OpenInference Specification](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)
- [Phoenix Integrations](https://arize.com/docs/phoenix/integrations)

**Local Reference Files:**
- [How-to Tracing](file://.local/references/phoenix/docs/tracing/how-to-tracing/README.md)
- [What are Traces](file://.local/references/phoenix/docs/tracing/concepts-tracing/what-are-traces.md)
- [Instrument Python](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/instrument-python.md)
- [Custom Spans](file://.local/references/phoenix/docs/tracing/how-to-tracing/setup-tracing/custom-spans.md)

**Integration Guides:**
- [OpenAI](file://.local/references/phoenix/docs/section-integrations/llm-providers/openai/openai-tracing.md)
- [LlamaIndex](file://.local/references/phoenix/docs/section-integrations/python/llamaindex/llamaindex-tracing.md)
- [Guardrails AI](file://.local/references/phoenix/docs/section-integrations/python/guardrails-ai/guardrails-ai-tracing.md)

**Example Code:**
- [Agent Framework Comparison](file://.local/references/phoenix/examples/agent_framework_comparison/)
- [Tracing Tutorials](file://.local/references/phoenix/tutorials/tracing/)