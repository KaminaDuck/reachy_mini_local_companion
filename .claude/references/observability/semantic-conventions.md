---
title: "OpenTelemetry Semantic Conventions Reference"
description: "Comprehensive guide to OpenTelemetry semantic attribute definitions, requirements, and standardized patterns"
type: "standard-spec"
tags: ["opentelemetry", "semantic-conventions", "attributes", "telemetry", "standards", "otel", "semconv"]
category: "observability"
subcategory: "telemetry-standards"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "OpenTelemetry Semantic Conventions Overview"
    url: "https://opentelemetry.io/docs/specs/semconv/"
  - name: "General Trace Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/general/trace/"
  - name: "Attribute Naming Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/"
  - name: "Attribute Type Mapping"
    url: "https://opentelemetry.io/docs/specs/otel/common/attribute-type-mapping/"
  - name: "Attribute Requirement Levels"
    url: "https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/"
  - name: "Resource Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/resource/"
  - name: "HTTP Semantic Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/http/"
  - name: "Database Semantic Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/database/"
  - name: "Exception Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/exceptions/"
  - name: "RPC Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/rpc/"
  - name: "Messaging Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/messaging/"
  - name: "System Metrics Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/system/"
  - name: "GenAI Conventions"
    url: "https://opentelemetry.io/docs/specs/semconv/gen-ai/"
  - name: "Kubernetes Resource Attributes"
    url: "https://opentelemetry.io/docs/specs/semconv/resource/k8s/"
  - name: "Cloud Provider Attributes"
    url: "https://opentelemetry.io/docs/specs/semconv/resource/cloud/"
related: ["opentelemetry-best-practices.md", "genai-semantic-conventions.md", "../python/pydantic-ai/phoenix-integration.md", "arize/span-kinds-reference.md"]
author: "unknown"
contributors: []
---

# OpenTelemetry Semantic Conventions Reference

Comprehensive reference for OpenTelemetry semantic conventions defining standardized attributes, metrics, and naming patterns that provide consistent meaning to observability data across distributed systems.

## Overview

OpenTelemetry semantic conventions define standardized attributes, metrics, and naming patterns that provide consistent meaning to observability data across distributed systems. ([OpenTelemetry Semantic Conventions Overview][1])

These conventions enable correlation of telemetry data from polyglot microservice environments, ensuring operators can analyze traces, metrics, and logs consistently regardless of programming language or platform. ([General Trace Conventions][2])

**Organization**:
- **Signal-based categories**: Traces, Metrics, Logs, Events
- **Domain-specific categories**: HTTP, Database, Messaging, RPC, Cloud Providers, Generative AI
- **Resource definitions**: Service, Host, Container, Kubernetes, Cloud infrastructure
- **Attribute registry**: 100+ standardized attribute namespaces

## General Conventions

### Attribute Naming Rules

OpenTelemetry enforces strict naming standards to ensure consistency and predictability. ([Attribute Naming Conventions][3])

#### Case and Structure

- **Lowercase requirement**: Names should be lowercase ([Attribute Naming Conventions][3])
- **Dot notation**: Use dots for namespacing (e.g., `service.version`, `http.request.method`)
- **Snake case**: Multi-word components within segments use underscores (e.g., `http.response.status_code`)
- **Nested namespaces**: Hierarchies can nest multiple levels (e.g., `telemetry.sdk.name`)

#### Character Restrictions

Valid attribute names: ([Attribute Naming Conventions][3])
- Must be valid Unicode sequences
- Limited to printable Basic Latin characters (U+0021 .. U+007E)
- Restricted to: Latin letters, numbers, underscores, dots
- Must start with a letter
- Must end with alphanumeric character
- Cannot contain consecutive delimiters (underscores or dots)

#### Precision and Clarity

- **Be descriptive**: Attribute, event, metric, and other names should be descriptive and unambiguous ([Attribute Naming Conventions][3])
- **Include property names**: Use `file.owner.name` rather than `file.owner` ([Attribute Naming Conventions][3])
- **Avoid ambiguity**: Don't use terms with different meanings across conventions

#### Uniqueness Requirements

Two attributes, two metrics, or two events must not share the same name. ([Attribute Naming Conventions][3])

Different entity types may share names (attribute vs. metric is acceptable).

#### Pluralization Guidelines

**For Attributes** ([Attribute Naming Conventions][3]):
- Singular: Single entities (`host.name`, `container.id`)
- Plural: Multiple values as arrays (`process.command_args`)

**For Metrics** ([Attribute Naming Conventions][3]):
- Counter/UpDownCounter names should not be pluralized unless representing discrete countable quantities
- Use "non-unit" convention: pluralize only when unit is countable (e.g., `{fault}`, `{operation}`)
- Avoid `_total` suffix in counter names

#### Reserved Namespace

Attribute names that start with `otel.` are reserved to be defined by OpenTelemetry specification. ([Attribute Naming Conventions][3])

### Namespace Organization

Attributes follow an object-property pattern using dot-delimited hierarchies: ([Attribute Naming Conventions][3])
- `{object}.{property}` structure (e.g., `file.owner.name`)
- Multiple nesting levels allowed (e.g., `telemetry.sdk.name`)
- Prefer dots over underscores for hierarchy

**System-Specific Pattern**: `{system_name}.*.{property}` ([Attribute Naming Conventions][3])

Examples:
- `cassandra.consistency.level`
- `aws.s3.key`
- `signalr.connection.status`

**Application-Specific Extensions**: ([Attribute Naming Conventions][3])
- Reverse domain naming: `com.acme.shopname`
- Application-specific prefixes
- Avoid collision with existing semantic convention namespaces

### Attribute Data Types

OpenTelemetry supports multiple data types mapped to OTLP's AnyValue format. ([Attribute Type Mapping][4])

#### Primitive Types

| Type | Range/Format | AnyValue Field |
|------|--------------|----------------|
| **Integer** | -2^63 to 2^63-1 | `int_value` |
| **Integer (overflow)** | Outside 64-bit range | `string_value` (decimal) |
| **Float** | IEEE 754 64-bit | `double_value` |
| **Float (high-precision)** | Beyond 64-bit | `string_value` (decimal) |
| **String** | Valid UTF-8 | `string_value` |
| **Bytes** | Raw byte data | `bytes_value` |
| **Boolean** | true/false | `bool_value` |
| **Enum** | Symbolic names preferred | `string_value` or `int_value` |

#### Composite Types

**Arrays/Sequences** ([Attribute Type Mapping][4]):
- Ordered sequences → `array_value`
- Rules apply recursively to elements

**Maps/Dictionaries**:
- Unique-key associative arrays → `kvlist_value`
- Non-string keys convert to strings maintaining uniqueness

**Special Cases**:
- **Empty Values**: Null/nil/absent → empty AnyValue with all fields unset ([Attribute Type Mapping][4])

### Requirement Levels

OpenTelemetry defines four requirement levels for attributes. ([Attribute Requirement Levels][5])

#### Required

**Definition**: All instrumentations must populate the attribute. ([Attribute Requirement Levels][5])

**Characteristics**:
- Included by default; cannot be excluded via configuration
- Expected to be efficiently retrievable
- Meets cardinality, security, and signal-specific requirements

**Example**: `http.request.method`

#### Conditionally Required

**Definition**: All instrumentations must populate the attribute when the given condition is satisfied. ([Attribute Requirement Levels][5])

**Characteristics**:
- Included by default when conditions exist; cannot be excluded
- Semantic convention explicitly defines triggering conditions
- May become Opt-In if conditions aren't met

**Example**: `http.route` (only when HTTP framework provides routing information)

#### Recommended

**Definition**: Instrumentations should add the attribute by default if it's readily available. ([Attribute Requirement Levels][5])

**Characteristics**:
- Included by default unless excluded for performance/security/privacy
- Instrumentation may offer configuration to disable
- Users can opt-in if initially excluded

#### Opt-In

**Definition**: Instrumentations should populate the attribute if and only if the user configures the instrumentation to do so. ([Attribute Requirement Levels][5])

**Characteristics**:
- Not included by default
- Reserved for expensive or sensitive operations
- Requires informed user decisions

**Examples**: DNS lookups for `server.address`, reading response streams for `http.response.body.size`

### Stability Levels

#### Stable
- Production-ready with backward compatibility guarantees
- Breaking changes follow deprecation process
- Examples: `http.request.method`, `server.address`, `url.full`

#### Development (Experimental)
- Under active development
- May change without notice
- Not recommended for production use
- Examples: `url.template`, `http.server.active_requests`

#### Deprecated
- Marked for removal in future versions
- Migration path should be documented
- Example: `exception.escaped`

## Resource Semantic Conventions

Resources describe the entity producing telemetry.

### Service Attributes

Core service identification attributes: ([Resource Conventions][6])

| Attribute | Requirement | Stability | Type | Description | Example |
|-----------|-------------|-----------|------|-------------|---------|
| `service.name` | **Required** | Stable | string | Logical name of the service | `shoppingcart` |
| `service.namespace` | Recommended | Development | string | Groups services (e.g., team ownership) | `shop` |
| `service.instance.id` | Recommended | Development | string | Unique identifier per service instance | `627cc493-f310-47de-96bd-71410b7dec09` |
| `service.version` | Recommended | Stable | string | Version string of the service | `2.0.0` |

### Telemetry SDK Attributes

Identifies the OpenTelemetry SDK: ([Resource Conventions][6])

| Attribute | Requirement | Stability | Type | Description | Example |
|-----------|-------------|-----------|------|-------------|---------|
| `telemetry.sdk.name` | **Required** | Stable | string | Must be `opentelemetry` for official SDKs | `opentelemetry` |
| `telemetry.sdk.language` | **Required** | Stable | string | Language identifier | `python`, `java`, `go` |
| `telemetry.sdk.version` | **Required** | Stable | string | SDK version string | `1.2.3` |

### Host Attributes

Describes computing instances like physical servers, VMs, switches: ([Resource Conventions][6])

| Attribute | Requirement | Stability | Type | Description | Example |
|-----------|-------------|-----------|------|-------------|---------|
| `host.id` | Recommended | Development | string | Unique host identifier | `/etc/machine-id` value |
| `host.name` | Recommended | Development | string | Hostname or FQDN | `opentelemetry-test` |
| `host.type` | Recommended | Development | string | Machine type | `n1-standard-1` |
| `host.arch` | Recommended | Development | string | CPU architecture | `amd64`, `arm64`, `x86` |
| `host.ip` | Opt-In | Development | string[] | Available IP addresses (excluding loopback) | `["10.0.0.1"]` |
| `host.mac` | Opt-In | Development | string[] | MAC addresses in IEEE RA format | `["AC-DE-48-23-45-67"]` |

### Container Attributes

All Development stability: ([Resource Conventions][6])

| Attribute | Requirement | Type | Description | Example |
|-----------|-------------|------|-------------|---------|
| `container.id` | Recommended | string | Container ID, usually a UUID | `a3bf90e006b2` |
| `container.name` | Recommended | string | Used by container runtime | `opentelemetry-autoconf` |
| `container.label.<key>` | Recommended | string | Container label key-value pairs | - |
| `oci.manifest.digest` | Recommended | string | OCI image manifest digest | `sha256:e4ca62c0d62f...` |
| `container.command` | Opt-In | string | Executable name | `otelcontribcol` |
| `container.command_args` | Opt-In | string[] | Complete command arguments | `["otelcontribcol", "--config"]` |

**Security Note**: Sensitive data like embedded credentials should be removed from command attributes. ([Resource Conventions][6])

### Cloud Provider Attributes

All Development stability, Recommended requirement: ([Cloud Provider Attributes][15])

| Attribute | Description | Examples |
|-----------|-------------|----------|
| `cloud.provider` | Name of cloud provider | `aws`, `azure`, `gcp`, `alibaba_cloud` |
| `cloud.platform` | Specific cloud platform | `aws_ec2`, `aws_lambda`, `azure.vm`, `gcp_kubernetes_engine` |
| `cloud.region` | Geographical region | `us-central1`, `us-east-1` |
| `cloud.availability_zone` | Isolated location within region | `us-east-1c` |
| `cloud.account.id` | Cloud account ID | `111111111111` |
| `cloud.resource_id` | Provider-specific native identifier | AWS Lambda ARN, GCP URI |

### Kubernetes Attributes

Comprehensive Kubernetes resource identification: ([Kubernetes Resource Attributes][14])

#### Cluster

| Attribute | Requirement | Stability | Description |
|-----------|-------------|-----------|-------------|
| `k8s.cluster.name` | Recommended | Development | The name of the cluster |
| `k8s.cluster.uid` | Recommended | Development | UID of `kube-system` namespace as proxy |

#### Pod

| Attribute | Requirement | Description |
|-----------|-------------|-------------|
| `k8s.pod.name` | Recommended | Pod name |
| `k8s.pod.uid` | Recommended | Pod UID |
| `k8s.pod.annotation.<key>` | Opt-In | Pod annotations |
| `k8s.pod.label.<key>` | Opt-In | Pod labels |

#### Workload Controllers

Standard attributes (name, uid) with optional annotations/labels for: ([Kubernetes Resource Attributes][14])
- Deployment
- StatefulSet
- DaemonSet
- Job
- CronJob
- ReplicaSet

### Deployment Environment

| Attribute | Requirement | Stability | Type | Description | Example |
|-----------|-------------|-----------|------|-------------|---------|
| `deployment.environment.name` | Recommended | Development | string | Deployment tier/environment | `staging`, `production` |

### Process Attributes

All Development stability: ([Resource Conventions][6])

| Attribute | Requirement | Type | Description | Example |
|-----------|-------------|------|-------------|---------|
| `process.pid` | Recommended | int | Process identifier (PID) | `1234` |
| `process.parent_pid` | Recommended | int | Parent process ID | `111` |
| `process.executable.name` | Recommended | string | Base name of executable | `otelcol` |
| `process.executable.path` | Recommended | string | Full path to executable | `/usr/bin/cmd/otelcol` |
| `process.command_line` | Recommended | string | Complete command as single string | `cmd/otelcol --config config.yaml` |
| `process.runtime.name` | Recommended | string | Runtime identifier | `OpenJDK Runtime Environment` |
| `process.runtime.version` | Recommended | string | Runtime version number | `14.0.2` |

## Trace Semantic Conventions

Spans represent specific operations in and between systems and ensure consistent analysis across polyglot (multi-language) micro-service environments. ([General Trace Conventions][2])

### HTTP Spans

HTTP conventions support HTTP/1.1, 2, 3, and SPDY protocols. ([HTTP Semantic Conventions][7])

#### Span Naming

Format: `{method} {target}` where: ([HTTP Semantic Conventions][7])
- `{method}` = `http.request.method` (or `HTTP` if method is `_OTHER`)
- `{target}` = `http.route` (servers) or `url.template` (clients, when available)

**Critical**: Instrumentation must not default to using URI path as a `{target}`. ([HTTP Semantic Conventions][7])

#### HTTP Client Spans

**Span Kind**: `CLIENT` ([HTTP Semantic Conventions][7])

**Required Attributes**:

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `http.request.method` | string | Known HTTP method or `_OTHER` | `GET`, `POST` |
| `server.address` | string | Domain name or IP address | `example.com` |
| `server.port` | int | Server port number | `443` |
| `url.full` | string | Complete absolute URL (sensitive data redacted) | `https://example.com/search?q=term` |

**Conditionally Required**:

| Attribute | Condition | Description |
|-----------|-----------|-------------|
| `error.type` | If request failed | Error classification |
| `http.response.status_code` | If received | HTTP status code |
| `http.request.method_original` | If different from normalized | Original method string |

**Recommended**:
- `network.peer.address` / `.port` - Directly connected peer
- `network.protocol.version` - HTTP version (e.g., `1.1`, `2`)
- `http.request.resend_count` - For retries/redirects

#### HTTP Server Spans

**Span Kind**: `SERVER` ([HTTP Semantic Conventions][7])

**Required Attributes**:

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `http.request.method` | string | HTTP method | `GET` |
| `url.path` | string | URI path component | `/search` |
| `url.scheme` | string | Protocol identifier | `http`, `https` |

**Conditionally Required**:

| Attribute | Condition | Description |
|-----------|-----------|-------------|
| `http.response.status_code` | If sent/received | HTTP status code |
| `http.route` | If available | Matched route template (low-cardinality) |

**Recommended**:
- `client.address` - Client domain/IP
- `network.peer.address` / `.port` - Directly connected peer
- `user_agent.original` - User-Agent header value

#### Span Status Rules

From ([HTTP Semantic Conventions][7]):
- **1xx, 2xx, 3xx**: Status unset (unless another error occurred)
- **4xx (client)**: Status unset for servers; should be `Error` for clients
- **5xx**: Status should be `Error`

### Database Spans

Database conventions cover SQL, NoSQL, and distributed systems. ([Database Semantic Conventions][8])

#### Span Naming Hierarchy

Priority order: ([Database Semantic Conventions][8])

1. **Preferred**: `{db.query.summary}` when available
2. **Fallback**: `{db.operation.name} {target}` if operation name exists
3. **Alternative**: `{target}` (collection name, stored procedure, namespace, or server address)
4. **Last resort**: `{db.system.name}` alone

#### Required Attributes

| Attribute | Requirement | Description | Example |
|-----------|-------------|-------------|---------|
| `db.system` | **Required** | DBMS product identifier | `postgresql`, `mysql`, `mongodb` |

#### Conditionally Required

| Attribute | Condition | Description |
|-----------|-----------|-------------|
| `db.collection.name` | Operating on specific table/container | Collection/table name |
| `db.operation.name` | Single operation describes call | Operation name |
| `db.response.status_code` | If operation failed | Response status |

#### Query Text Sanitization

Non-parameterized query text should not be collected by default unless there is sanitization that excludes sensitive information. ([Database Semantic Conventions][8])

Sanitization replaces literals with `?` placeholders to protect credentials and sensitive data.

### Exception Spans

Exception events follow standardized conventions. ([Exception Conventions][9])

#### Event Name

Must be named `exception`. ([Exception Conventions][9])

#### Core Attributes

| Attribute | Requirement | Stability | Type | Description | Example |
|-----------|-------------|-----------|------|-------------|---------|
| `exception.type` | Conditionally Required* | Stable | string | The type of the exception (fully-qualified class name) | `java.net.ConnectException`, `OSError` |
| `exception.message` | Conditionally Required* | Stable | string | The exception message | `Division by zero` |
| `exception.stacktrace` | Recommended | Stable | string | A stacktrace as a string in natural representation | - |

*At least one of `exception.type` or `exception.message` required. ([Exception Conventions][9])

### RPC Spans

Remote procedure call conventions covering gRPC, JSON-RPC, and others. ([RPC Conventions][10])

#### Span Naming

Format: `$package.$service/$method` ([RPC Conventions][10])

Package portion optional if unknown/absent.

Examples:
- `grpc.test.EchoService/Echo`
- `com.example.ExampleRmiService/exampleMethod`

#### Client Spans (CLIENT)

**Required Attributes**: ([RPC Conventions][10])

| Attribute | Description |
|-----------|-------------|
| `rpc.system` | Remoting system (e.g., `grpc`, `java_rmi`) |
| `server.address` | RPC server hostname or IP |

**Recommended**:
- `rpc.method`
- `rpc.service`
- Network details: `network.peer.address`, `network.peer.port`

#### Supported RPC Systems

Well-known `rpc.system` values: ([RPC Conventions][10])
- `grpc`
- `java_rmi`
- `dotnet_wcf`
- `jsonrpc`
- `apache_dubbo`
- `connect_rpc`

### Messaging Spans

Conventions for message queuing systems. ([Messaging Conventions][11])

#### Core Operation Types

Five messaging operations: ([Messaging Conventions][11])

1. **Create**: Single message preparation for sending
2. **Send**: Delivery of one or more messages to intermediary
3. **Receive**: Pull-based message consumption
4. **Process**: Push-based message handling by consumers
5. **Settle**: Acknowledgment of message processing

#### Span Naming

Span name should be `{messaging.operation.name} {destination}`. ([Messaging Conventions][11])

Use destination template, name, or server address as appropriate.

#### Required Attributes

| Attribute | Description | Examples |
|-----------|-------------|----------|
| `messaging.operation.name` | Operation type | `send`, `poll`, `process` |
| `messaging.system` | Messaging system | `kafka`, `rabbitmq`, `aws_sqs` |

#### Span Kind Mapping

| Operation | Span Kind |
|-----------|-----------|
| Create | PRODUCER |
| Send | PRODUCER or CLIENT |
| Receive | CLIENT |
| Process | CONSUMER |
| Settle | CLIENT |

([Messaging Conventions][11])

## Metric Semantic Conventions

### HTTP Metrics

#### HTTP Server Duration (Required, Stable)

**`http.server.request.duration`** ([HTTP Semantic Conventions][7])
- **Instrument**: Histogram
- **Unit**: seconds (`s`)
- **Purpose**: Measures duration of HTTP server requests

**Required Attributes**:
- `http.request.method`
- `url.scheme`

**Conditionally Required**:
- `http.response.status_code` (if available)
- `error.type` (if error occurred)
- `http.route` (if available)

**Bucket Boundaries**: `[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10]` ([HTTP Semantic Conventions][7])

#### HTTP Client Duration (Required, Stable)

**`http.client.request.duration`** ([HTTP Semantic Conventions][7])
- **Instrument**: Histogram
- **Unit**: seconds (`s`)
- **Purpose**: Measures duration of HTTP client requests

**Required Attributes**:
- `http.request.method`
- `server.address`
- `server.port`

### Database Metrics

#### Database Operation Duration (Required, Stable)

**`db.client.operation.duration`** ([Database Semantic Conventions][8])
- **Instrument**: Histogram
- **Unit**: seconds (`s`)
- **Purpose**: Duration of database client operations
- **Bucket boundaries**: `[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]`

**Required Attributes**:
- Database system name
- Collection name (when applicable)
- Namespace
- Operation name
- Response status code

### System Metrics

Comprehensive system-level monitoring conventions. All metrics use `system.*` namespace and are in Development status. ([System Metrics Conventions][12])

#### CPU Metrics

| Metric | Type | Unit | Purpose |
|--------|------|------|---------|
| `system.cpu.physical.count` | UpDownCounter | `{cpu}` | Reports the number of actual physical processor cores |
| `system.cpu.logical.count` | UpDownCounter | `{cpu}` | Logical (virtual) processor cores |
| `system.cpu.time` | Counter | `s` | Seconds spent per CPU mode |
| `system.cpu.utilization` | Gauge | `1` | CPU usage calculated from cumulative time changes |

#### Memory Metrics

| Metric | Type | Unit | Purpose |
|--------|------|------|---------|
| `system.memory.usage` | UpDownCounter | `By` | Reports memory in use by state |
| `system.memory.utilization` | Gauge | `1` | Percentage of memory bytes in use |
| `system.memory.limit` | UpDownCounter | `By` | Total virtual memory available |

#### Network Metrics

| Metric | Type | Unit | Purpose |
|--------|------|------|---------|
| `system.network.io` | Counter | `By` | Bytes transmitted and received |
| `system.network.packet.count` | Counter | `{packet}` | Packets transferred count |
| `system.network.packet.dropped` | Counter | `{packet}` | Packets dropped or discarded without error |
| `system.network.errors` | Counter | `{error}` | Network errors detected |

## Generative AI Semantic Conventions

OpenTelemetry defines comprehensive conventions for instrumenting generative AI systems. All conventions are in Development status. ([GenAI Conventions][13])

### GenAI Inference Spans

**Purpose**: Represents client calls to GenAI models that generate responses or request tool execution.

**Span Naming**: `{gen_ai.operation.name} {gen_ai.request.model}` ([GenAI Conventions][13])

**Span Kind**: `CLIENT` (or `INTERNAL` for same-process execution)

#### Essential Attributes (Required)

| Attribute | Description | Example |
|-----------|-------------|---------|
| `gen_ai.operation.name` | Operation type | `chat`, `generate_content`, `text_completion` |
| `gen_ai.provider.name` | Provider identifier | `openai`, `anthropic`, `aws.bedrock` |

#### Conditionally Required

| Attribute | Condition | Description |
|-----------|-----------|-------------|
| `gen_ai.request.model` | If available | Model name being invoked |
| `error.type` | On errors | Error classification |

#### Token Usage (Recommended)

| Attribute | Description |
|-----------|-------------|
| `gen_ai.usage.input_tokens` | Tokens consumed in prompt |
| `gen_ai.usage.output_tokens` | Tokens generated in response |

#### Model Parameters (Recommended)

| Attribute | Description | Typical Range |
|-----------|-------------|---------------|
| `gen_ai.request.temperature` | Creativity control | 0.0-2.0 |
| `gen_ai.request.top_p` | Sampling control | 0.0-1.0 |
| `gen_ai.request.max_tokens` | Generation limit | Integer |
| `gen_ai.request.frequency_penalty` | Repetition control | -2.0 to 2.0 |
| `gen_ai.request.presence_penalty` | Repetition control | -2.0 to 2.0 |

#### Content Capture (Opt-In)

| Attribute | Description | Format |
|-----------|-------------|--------|
| `gen_ai.input.messages` | Chat history | Structured JSON array |
| `gen_ai.output.messages` | Model responses | Structured JSON array |
| `gen_ai.system_instructions` | System prompts | Structured format |
| `gen_ai.tool.definitions` | Available tool specifications | Structured format |

### GenAI Metrics

#### Token Usage (Recommended)

**Metric**: `gen_ai.client.token.usage` ([GenAI Conventions][13])
- **Instrument**: Histogram
- **Unit**: `{token}`
- **Purpose**: Number of input and output tokens used

**Required Attributes**:
- `gen_ai.operation.name`
- `gen_ai.provider.name`
- `gen_ai.token.type` (input or output)

#### Operation Duration (Required)

**Metric**: `gen_ai.client.operation.duration` ([GenAI Conventions][13])
- **Instrument**: Histogram
- **Unit**: `s` (seconds)
- **Purpose**: GenAI operation duration

## Common Attributes

### Network Attributes

Describes network-level characteristics:

| Attribute | Stability | Type | Description | Values |
|-----------|-----------|------|-------------|--------|
| `network.transport` | Stable | string | OSI transport layer or inter-process communication method | `tcp`, `udp`, `quic`, `unix`, `pipe` |
| `network.type` | Stable | string | OSI network layer or non-OSI equivalent | `ipv4`, `ipv6` |
| `network.protocol.name` | Stable | string | OSI application layer or non-OSI equivalent | `amqp`, `http`, `mqtt` |
| `network.protocol.version` | Stable | string | Actual version used for network communication | `1.1`, `2` |

### Server and Client Attributes

Both Stable status:

| Attribute | Type | Description | Examples |
|-----------|------|-------------|----------|
| `server.address` | string | Server domain name if available without reverse DNS lookup | `example.com`, `10.1.2.80` |
| `server.port` | int | Server port number | `80`, `8080`, `443` |
| `client.address` | string | Client address - domain name if available | `client.example.com`, `10.1.2.80` |
| `client.port` | int | Client port number | `65123` |

### URL Attributes

Core URL attributes (Stable):

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `url.scheme` | string | The URI scheme component | `https`, `ftp` |
| `url.full` | string | Absolute URL describing network resource | `https://www.foo.bar/search?q=OpenTelemetry` |
| `url.path` | string | The URI path component | `/search` |
| `url.query` | string | The URI query component | `q=OpenTelemetry` |

**Development**:

| Attribute | Description | Examples |
|-----------|-------------|----------|
| `url.template` | Low-cardinality template of an absolute path reference | `/users/{id}`, `/users/:id` |

**Security**: User and password information, when they are provided in User Information subcomponent, must not be recorded.

### User Agent Attributes

| Attribute | Stability | Type | Description | Examples |
|-----------|-----------|------|-------------|----------|
| `user_agent.original` | Stable | string | Value of the HTTP User-Agent header | Browser strings, `YourApp/1.0.0` |
| `user_agent.name` | Development | string | Extracted browser/application name | `Safari`, `YourApp` |
| `user_agent.version` | Development | string | Extracted browser/application version | `14.1.2`, `1.0.0` |

### Error Attributes

**`error.type`** (Stable)
- **Type**: string
- **Purpose**: Describes a class of error the operation ended with
- **Examples**: `timeout`, `java.net.UnknownHostException`, `500`

**Key Requirements**:
- Should be predictable with low cardinality
- Use canonical class names when representing exception types
- Should not be set if operation completed successfully

## Examples

### HTTP Server Span Example

```python
span = tracer.start_span(
    name="GET /api/users/{id}",
    kind=SpanKind.SERVER,
    attributes={
        # Required
        "http.request.method": "GET",
        "url.path": "/api/users/123",
        "url.scheme": "https",

        # Conditionally Required
        "http.route": "/api/users/{id}",
        "http.response.status_code": 200,

        # Recommended
        "client.address": "192.168.1.100",
        "user_agent.original": "Mozilla/5.0 ...",
    }
)
```

### Database Span Example

```python
span = tracer.start_span(
    name="SELECT users",
    kind=SpanKind.CLIENT,
    attributes={
        # Required
        "db.system": "postgresql",

        # Conditionally Required
        "db.collection.name": "users",
        "db.operation.name": "SELECT",

        # Recommended
        "server.address": "db.example.com",
        "server.port": 5432,
        "db.query.text": "SELECT * FROM users WHERE id = ?",
    }
)
```

### GenAI Inference Span Example

```python
span = tracer.start_span(
    name="chat gpt-4",
    kind=SpanKind.CLIENT,
    attributes={
        # Required
        "gen_ai.operation.name": "chat",
        "gen_ai.provider.name": "openai",
        "gen_ai.request.model": "gpt-4",

        # Token usage (Recommended)
        "gen_ai.usage.input_tokens": 150,
        "gen_ai.usage.output_tokens": 75,

        # Model parameters (Recommended)
        "gen_ai.request.temperature": 0.7,
        "gen_ai.request.max_tokens": 500,
    }
)
```

### Resource Definition Example

```python
resource = Resource.create({
    # Service identification (Required)
    "service.name": "checkout-service",
    "service.version": "2.1.0",

    # Telemetry SDK (Required)
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.language": "python",
    "telemetry.sdk.version": "1.21.0",

    # Cloud (Recommended)
    "cloud.provider": "aws",
    "cloud.platform": "aws_ec2",
    "cloud.region": "us-east-1",

    # Kubernetes (Recommended)
    "k8s.cluster.name": "production-cluster",
    "k8s.namespace.name": "ecommerce",
    "k8s.pod.name": "checkout-service-abc123-xyz",
})
```

## Related References

- [OpenTelemetry Best Practices](opentelemetry-best-practices.md) - Implementation patterns and configuration
- [Pydantic AI Phoenix Integration](../pydantic-ai/phoenix-integration.md) - Practical integration example
- [Arize Span Kinds Reference](../arize/span-kinds-reference.md) - OpenInference span types

[1]: https://opentelemetry.io/docs/specs/semconv/ "OpenTelemetry Semantic Conventions Overview"
[2]: https://opentelemetry.io/docs/specs/semconv/general/trace/ "General Trace Conventions"
[3]: https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/ "Attribute Naming Conventions"
[4]: https://opentelemetry.io/docs/specs/otel/common/attribute-type-mapping/ "Attribute Type Mapping"
[5]: https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/ "Attribute Requirement Levels"
[6]: https://opentelemetry.io/docs/specs/semconv/resource/ "Resource Conventions"
[7]: https://opentelemetry.io/docs/specs/semconv/http/ "HTTP Semantic Conventions"
[8]: https://opentelemetry.io/docs/specs/semconv/database/ "Database Semantic Conventions"
[9]: https://opentelemetry.io/docs/specs/semconv/exceptions/ "Exception Conventions"
[10]: https://opentelemetry.io/docs/specs/semconv/rpc/ "RPC Conventions"
[11]: https://opentelemetry.io/docs/specs/semconv/messaging/ "Messaging Conventions"
[12]: https://opentelemetry.io/docs/specs/semconv/system/ "System Metrics Conventions"
[13]: https://opentelemetry.io/docs/specs/semconv/gen-ai/ "GenAI Conventions"
[14]: https://opentelemetry.io/docs/specs/semconv/resource/k8s/ "Kubernetes Resource Attributes"
[15]: https://opentelemetry.io/docs/specs/semconv/resource/cloud/ "Cloud Provider Attributes"
