---
author: unknown
category: ai-frameworks
contributors: []
description: Complete guide to integrating Pydantic AI agents with Arize Phoenix observability
  on local Docker stack
last_updated: '2025-08-16'
related:
- agents.md
- openai-integration.md
- ../../observability/arize/docker-compose-deployment.md
- ../../observability/arize/span-kinds-reference.md
- ../../observability/opentelemetry-best-practices.md
- ../../observability/semantic-conventions.md
- ../../observability/genai-semantic-conventions.md
sources:
- name: Arize Phoenix Docker Documentation
  url: https://arize.com/docs/phoenix/self-hosting/deployment-options/docker
- name: Phoenix OTEL Setup Guide
  url: https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/setup-using-phoenix-otel
- name: Pydantic AI Logfire Documentation
  url: https://ai.pydantic.dev/logfire/
- name: SigNoz Pydantic AI Observability
  url: https://signoz.io/docs/pydantic-ai-observability/
- name: OpenInference PydanticAI GitHub
  url: https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-pydantic-ai
- name: Phoenix Pydantic AI Tracing Documentation
  url: https://arize.com/docs/phoenix/integrations/pydantic/pydantic-tracing
- name: Docker Compose Networking Documentation
  url: https://docs.docker.com/compose/networking/
- name: Phoenix Authentication Documentation
  url: https://docs.arize.com/phoenix/self-hosting/authentication
status: stable
subcategory: observability
tags:
- pydantic-ai
- phoenix
- arize
- opentelemetry
- docker-compose
- tracing
- observability
- otlp
title: Pydantic AI + Arize Phoenix Integration for Docker Compose
type: integration-guide
version: '1.0'
---

# Pydantic AI + Arize Phoenix Integration for Docker Compose

Complete integration guide for connecting Pydantic AI agents with Arize Phoenix observability platform using Docker Compose for fully local deployment.

## Overview

This integration enables comprehensive observability for Pydantic AI applications using Arize Phoenix as the tracing backend. The setup leverages OpenTelemetry Protocol (OTLP) for trace data transmission, with Phoenix acting as the OTLP collector and visualization platform. ([Arize Phoenix Docker Documentation][1], [Phoenix OTEL Setup Guide][2])

### Architecture

```
Pydantic AI Agent (OpenTelemetry instrumented)
    ↓ OTLP traces (HTTP/gRPC)
    ↓ http://phoenix:6006/v1/traces OR grpc://phoenix:4317
Phoenix Docker Container (OTLP collector + UI)
    ↓ persists traces
PostgreSQL Database (recommended for production)
```

### Key Components

1. **Pydantic AI Application**: Python application using Pydantic AI agents with built-in OpenTelemetry instrumentation
2. **Arize Phoenix**: OTLP collector and observability UI running in Docker
3. **PostgreSQL Database**: Persistent storage for Phoenix trace data (optional for development)

## Pydantic AI OpenTelemetry Configuration

### Native Instrumentation

Pydantic AI features native OpenTelemetry support that can be enabled globally or per-agent. ([Pydantic AI Logfire Documentation][3])

#### Global Instrumentation

```python
from pydantic_ai import Agent

# Enable instrumentation for all agents
Agent.instrument_all()

# Create agents normally
agent = Agent('openai:gpt-5-nano')
result = agent.run_sync('Hello, world!')
```

#### Per-Agent Instrumentation

```python
from pydantic_ai import Agent, InstrumentationSettings

# Configure instrumentation settings
instrumentation = InstrumentationSettings(
    version=2,  # OpenTelemetry semantic conventions version
    include_content=True,  # Include prompts/completions
    event_mode='logs'  # Use logs instead of JSON arrays
)

# Create agent with specific instrumentation
agent = Agent(
    'openai:gpt-5-nano',
    instrument=instrumentation
)
```

([Pydantic AI Logfire Documentation][3])

### InstrumentationSettings Options

| Parameter | Type | Purpose | Default |
|-----------|------|---------|---------|
| `version` | int | OTel semantic conventions version (1, 2, or 3) | 2 |
| `event_mode` | str | Event format: `'json_array'` or `'logs'` | `'json_array'` |
| `include_content` | bool | Include prompts/completions/tool args | True |
| `include_binary_content` | bool | Include binary data in events | True |
| `tracer_provider` | TracerProvider | Custom OTel tracer provider | None |
| `event_logger_provider` | LoggerProvider | Custom OTel logger provider | None |

**Note**: Setting `event_mode='logs'` aligns with OpenTelemetry Semantic Conventions for Generative AI, improving compatibility with generic OTLP collectors. ([SigNoz Pydantic AI Observability][4])

### OTLP Exporter Configuration

#### Method 1: Environment Variables (Recommended for Docker)

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:6006
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_RESOURCE_ATTRIBUTES=service.name=my-pydantic-app
```

When running inside Docker Compose, use the service name:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://phoenix:6006
```

([SigNoz Pydantic AI Observability][4])

#### Method 2: Programmatic Configuration

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from pydantic_ai import Agent

# Create resource with service name
resource = Resource.create({"service.name": "my-pydantic-app"})

# Configure tracer provider
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure OTLP exporter
endpoint = "http://phoenix:6006/v1/traces"
exporter = OTLPSpanExporter(endpoint=endpoint)

# Add span processor
span_processor = BatchSpanProcessor(exporter)
tracer_provider.add_span_processor(span_processor)

# Enable Pydantic AI instrumentation
Agent.instrument_all()

# Create and use agent
agent = Agent('openai:gpt-5-nano')
result = agent.run_sync('What is the capital of France?')
```

([Pydantic AI Logfire Documentation][3], [SigNoz Pydantic AI Observability][4])

## Arize Phoenix Docker Configuration

### Port Configuration

Phoenix exposes three ports for different protocols: ([Arize Phoenix Docker Documentation][1])

| Port | Protocol | Purpose | Environment Variable |
|------|----------|---------|---------------------|
| 6006 | HTTP | UI + OTLP HTTP collector (`/v1/traces`) | `PHOENIX_PORT` |
| 4317 | gRPC | OTLP gRPC collector | `PHOENIX_GRPC_PORT` |
| 9090 | HTTP | Prometheus metrics (optional) | `PHOENIX_ENABLE_PROMETHEUS=true` |

### OTLP Endpoints

**HTTP Endpoint**: `http://phoenix:6006/v1/traces` (uses HTTP/Protobuf protocol)

**gRPC Endpoint**: `http://phoenix:4317` (uses gRPC protocol)

([Phoenix OTEL Setup Guide][2])

### Docker Images

Available on Docker Hub: `arizephoenix/phoenix`

**Recommended Tags**:
- `12.9.0`, `12.8.0`, `12.7.1`, etc. - Specific versions (production)
- `latest` - Latest stable (development only)
- `nightly` - Latest features (testing)

([Arize Phoenix Docker Documentation][1])

### Essential Environment Variables

#### Core Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PHOENIX_PORT` | HTTP server port | 6006 | 8080 |
| `PHOENIX_GRPC_PORT` | gRPC collector port | 4317 | 4318 |
| `PHOENIX_HOST` | Bind address | `0.0.0.0` | `127.0.0.1` |
| `PHOENIX_WORKING_DIR` | Data directory for SQLite | `~/.phoenix/` | `/data` |
| `PHOENIX_LOG_LEVEL` | Logging verbosity | INFO | DEBUG |

#### Database Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `PHOENIX_SQL_DATABASE_URL` | PostgreSQL connection URL | `postgresql://user:pass@host:5432/db` |
| `PHOENIX_DEFAULT_RETENTION_POLICY_DAYS` | Trace retention period | `30` |

#### Authentication

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `PHOENIX_ENABLE_AUTH` | Enable authentication | No | `true` |
| `PHOENIX_SECRET` | JWT signing secret (min 32 chars) | If auth enabled | Random string |
| `PHOENIX_API_KEY` | Default API key for clients | No | Long random string |

([Arize Phoenix Docker Documentation][1])

## Docker Compose Examples

### Minimal Setup (SQLite)

Suitable for development and testing:

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    ports:
      - "6006:6006"  # UI and HTTP OTLP collector
      - "4317:4317"  # gRPC OTLP collector
    environment:
      - PHOENIX_WORKING_DIR=/data
    volumes:
      - phoenix_data:/data
    restart: unless-stopped

volumes:
  phoenix_data:
    driver: local
```

([Arize Phoenix Docker Documentation][1])

### Production Setup (PostgreSQL)

Recommended for production deployments:

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "6006:6006"
      - "4317:4317"
      - "9090:9090"  # Prometheus metrics
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/phoenix
      - PHOENIX_ENABLE_PROMETHEUS=true
      - PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=30
      - PHOENIX_LOG_LEVEL=INFO
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=phoenix
      - POSTGRES_INITDB_ARGS=--data-checksums
    volumes:
      - phoenix_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d phoenix"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    restart: unless-stopped

volumes:
  phoenix_db:
    driver: local
```

([Arize Phoenix Docker Documentation][1])

## Complete Integration Example

### Project Structure

```
project/
├── docker-compose.yml
├── .env
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
```

### docker-compose.yml (Full Stack)

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:12.9.0
    container_name: phoenix
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "6006:6006"  # UI and HTTP OTLP
      - "4317:4317"  # gRPC OTLP
      - "9090:9090"  # Prometheus
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/phoenix
      - PHOENIX_ENABLE_PROMETHEUS=true
      - PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=30
      - PHOENIX_LOG_LEVEL=INFO
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: phoenix-db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=phoenix
      - POSTGRES_INITDB_ARGS=--data-checksums
    volumes:
      - phoenix_db:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d phoenix"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    restart: unless-stopped

  pydantic-app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: pydantic-ai-app
    depends_on:
      phoenix:
        condition: service_started
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://phoenix:6006
      - OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
      - OTEL_RESOURCE_ATTRIBUTES=service.name=pydantic-ai-app
      - PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  phoenix_db:
    driver: local
```

### .env

```bash
DB_PASSWORD=secure_random_password_here
OPENAI_API_KEY=sk-your-openai-key-here
```

### app/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]
```

### app/requirements.txt

```
pydantic-ai
openai
opentelemetry-sdk
opentelemetry-exporter-otlp
opentelemetry-api
```

### app/main.py

```python
import os
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from pydantic_ai import Agent

def setup_telemetry():
    """Configure OpenTelemetry to send traces to Phoenix"""
    # Create resource with service name
    resource = Resource.create({
        "service.name": os.getenv("OTEL_RESOURCE_ATTRIBUTES", "pydantic-ai-app")
    })

    # Configure tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Configure OTLP exporter
    endpoint = f"{os.getenv('PHOENIX_COLLECTOR_ENDPOINT', 'http://localhost:6006')}/v1/traces"
    exporter = OTLPSpanExporter(endpoint=endpoint)

    # Add batch span processor
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

    print(f"Telemetry configured. Sending traces to: {endpoint}")

def main():
    """Main application entry point"""
    # Setup telemetry
    setup_telemetry()

    # Enable Pydantic AI instrumentation
    Agent.instrument_all()

    # Create agent
    agent = Agent('openai:gpt-5-nano')

    # Run agent in loop
    queries = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "What are the main features of Python?"
    ]

    print("Starting Pydantic AI agent with Phoenix tracing...")

    while True:
        for query in queries:
            print(f"\nQuery: {query}")
            result = agent.run_sync(query)
            print(f"Response: {result.data}")
            time.sleep(10)

if __name__ == "__main__":
    main()
```

## Network Configuration

### Docker Compose Service Discovery

Docker Compose automatically creates a default network where services communicate using service names as hostnames. ([Docker Compose Networking Documentation][7])

**Key Points**:

1. **Service Names as Hostnames**: Services reference each other by service name (e.g., `phoenix`, `db`, `pydantic-app`)
2. **DNS Resolution**: Docker's built-in DNS (127.0.0.11:53) resolves service names to container IP addresses
3. **Port Mapping**:
   - `phoenix:6006` - Internal access from other containers
   - `localhost:6006` - External access from host machine

### Endpoint Configuration

**Inside Docker Compose** (container-to-container):
```python
endpoint = "http://phoenix:6006/v1/traces"  # Use service name
```

**On Host Machine** (host-to-container):
```python
endpoint = "http://localhost:6006/v1/traces"  # Use localhost
```

## Authentication Configuration

### Enabling Phoenix Authentication

When authentication is enabled, API keys are required for trace ingestion. ([Phoenix Authentication Documentation][8])

```yaml
phoenix:
  environment:
    - PHOENIX_ENABLE_AUTH=true
    - PHOENIX_SECRET=your-secret-key-min-32-chars-long
    - PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD=admin
```

### Creating API Keys

1. Start Phoenix with authentication enabled
2. Login as admin: `admin@localhost` / `admin`
3. Navigate to Settings → API Keys
4. Create a System API Key

### Configuring Client with API Key

```bash
export PHOENIX_API_KEY=your-system-or-user-key
```

**In Python**:

```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(
    endpoint="http://phoenix:6006/v1/traces",
    headers={"authorization": "Bearer your-api-key"}  # lowercase for gRPC compatibility
)
```

**Important**: Use lowercase `authorization` for gRPC compatibility. ([Phoenix Authentication Documentation][8])

## Protocol Selection

### HTTP/Protobuf (Recommended)

**Endpoint**: `http://phoenix:6006/v1/traces`

**Configuration**:
```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(endpoint="http://phoenix:6006/v1/traces")
```

**Environment Variables**:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://phoenix:6006
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

### gRPC

**Endpoint**: `http://phoenix:4317`

**Configuration**:
```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter(endpoint="http://phoenix:4317")
```

**Environment Variables**:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://phoenix:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
```

([Phoenix OTEL Setup Guide][2])

## Advanced Configuration

### OpenInference Instrumentation

For advanced use cases, use the OpenInference instrumentation library designed for Phoenix integration. ([OpenInference PydanticAI GitHub][5])

**Installation**:
```bash
pip install openinference-instrumentation-pydantic-ai arize-phoenix
```

**Configuration**:
```python
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from openinference.instrumentation.pydantic_ai import OpenInferenceSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Set up tracer provider
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

# Configure Phoenix endpoint
endpoint = f"{os.environ['PHOENIX_COLLECTOR_ENDPOINT']}/v1/traces"
headers = {"Authorization": f"Bearer {os.environ.get('PHOENIX_API_KEY', '')}"}
exporter = OTLPSpanExporter(endpoint=endpoint, headers=headers)

# Add processors
tracer_provider.add_span_processor(OpenInferenceSpanProcessor())
tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))

# Create agent with instrumentation enabled
model = OpenAIModel("gpt-4", provider='openai')
agent = Agent(model, instrument=True)

result = agent.run_sync("The windy city in the US of A.")
```

([Phoenix Pydantic AI Tracing Documentation][6], [OpenInference PydanticAI GitHub][5])

### HTTPX Instrumentation

Capture HTTP requests made by Pydantic AI to model providers (OpenAI, Anthropic, etc.). ([SigNoz Pydantic AI Observability][4])

**Installation**:
```bash
pip install opentelemetry-instrumentation-httpx
```

**Configuration**:
```python
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# Instrument all HTTPX clients
HTTPXClientInstrumentor().instrument()

# Then enable Pydantic AI instrumentation
Agent.instrument_all()
```

## Testing the Integration

### Step 1: Start Phoenix

```bash
docker compose up phoenix db -d
```

**Verify Phoenix is running**:
- UI: http://localhost:6006
- Check logs: `docker compose logs phoenix`

### Step 2: Run Pydantic AI Application

**Option A: Inside Docker Compose**
```bash
docker compose up pydantic-app
```

**Option B: On Host Machine**
```bash
export OPENAI_API_KEY=your-key
export PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006
python app/main.py
```

### Step 3: Verify Traces in Phoenix

1. Open http://localhost:6006
2. Navigate to "Traces" tab
3. Verify traces appear with:
   - Agent interactions
   - LLM calls (span kind: LLM)
   - Tool calls (span kind: TOOL)
   - Input/output data

## Troubleshooting

### Traces Not Appearing

**Check Endpoint Configuration**:
```bash
# Inside container
curl http://phoenix:6006/v1/traces

# From host
curl http://localhost:6006/v1/traces
```

**Check Authentication**:
- Verify `PHOENIX_API_KEY` is set if auth enabled
- Confirm header format: `Bearer <token>`

**Check Network Connectivity**:
```bash
# Test from pydantic-app container
docker exec pydantic-app ping phoenix
docker exec pydantic-app curl http://phoenix:6006
```

### Database Connection Errors

**PostgreSQL Not Ready**:

Add health check and depends_on condition:
```yaml
pydantic-app:
  depends_on:
    phoenix:
      condition: service_started
    db:
      condition: service_healthy
```

**Connection String Format**:
```bash
# Correct
postgresql://user:password@host:5432/database

# Incorrect (missing 'ql')
postgres://user:password@host:5432/database
```

### High Memory Usage

**Optimize PostgreSQL**:
```yaml
db:
  command: |
    postgres
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
    -c max_connections=100
```

**Set Resource Limits**:
```yaml
phoenix:
  deploy:
    resources:
      limits:
        memory: 2G
        cpus: "2.0"
```

([Arize Phoenix Docker Documentation][1])

## Production Deployment Checklist

### Security
- [ ] Pin Docker image versions (not `latest`)
- [ ] Change default PostgreSQL password
- [ ] Enable Phoenix authentication
- [ ] Set strong `PHOENIX_SECRET` (min 32 chars)
- [ ] Use environment secrets management
- [ ] Enable SSL/TLS for PostgreSQL

### Data Persistence
- [ ] Use external PostgreSQL (not SQLite)
- [ ] Configure automated database backups
- [ ] Set retention policy (`PHOENIX_DEFAULT_RETENTION_POLICY_DAYS`)
- [ ] Monitor disk usage

### Monitoring
- [ ] Enable Prometheus metrics
- [ ] Set up alerting
- [ ] Configure log aggregation
- [ ] Monitor trace ingestion rates

### High Availability
- [ ] Use PostgreSQL cluster or managed service
- [ ] Run multiple Phoenix replicas behind load balancer
- [ ] Configure health checks
- [ ] Set resource limits and auto-scaling

([Arize Phoenix Docker Documentation][1])

## Configuration Summary

### Pydantic AI Configuration

**Environment Variables**:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://phoenix:6006
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_RESOURCE_ATTRIBUTES=service.name=my-app
OPENAI_API_KEY=sk-...
PHOENIX_API_KEY=optional-if-auth-enabled
```

**Code**:
```python
from pydantic_ai import Agent

Agent.instrument_all()
agent = Agent('openai:gpt-5-nano')
```

### Phoenix Configuration

**Ports**:
- 6006: UI + HTTP OTLP collector
- 4317: gRPC OTLP collector
- 9090: Prometheus (optional)

**Required Environment**:
```yaml
PHOENIX_SQL_DATABASE_URL=postgresql://user:pass@db:5432/phoenix
PHOENIX_ENABLE_PROMETHEUS=true
PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=30
```

## Related References

- [Pydantic AI Agents Reference](agents.md) - Core agent concepts and patterns
- [OpenAI Integration](openai-integration.md) - Model provider configuration
- [Arize Docker Compose Deployment](../arize/docker-compose-deployment.md) - Phoenix deployment patterns
- [Span Kinds Reference](../arize/span-kinds-reference.md) - OpenTelemetry span types

[1]: https://arize.com/docs/phoenix/self-hosting/deployment-options/docker "Arize Phoenix Docker Documentation"
[2]: https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/setup-using-phoenix-otel "Phoenix OTEL Setup Guide"
[3]: https://ai.pydantic.dev/logfire/ "Pydantic AI Logfire Documentation"
[4]: https://signoz.io/docs/pydantic-ai-observability/ "SigNoz Pydantic AI Observability"
[5]: https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-pydantic-ai "OpenInference PydanticAI GitHub"
[6]: https://arize.com/docs/phoenix/integrations/pydantic/pydantic-tracing "Phoenix Pydantic AI Tracing Documentation"
[7]: https://docs.docker.com/compose/networking/ "Docker Compose Networking Documentation"
[8]: https://docs.arize.com/phoenix/self-hosting/authentication "Phoenix Authentication Documentation"