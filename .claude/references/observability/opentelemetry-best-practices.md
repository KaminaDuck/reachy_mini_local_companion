---
author: unknown
category: observability
contributors: []
description: Comprehensive guide to OpenTelemetry instrumentation, configuration,
  and production deployment patterns
last_updated: '2025-11-01'
related:
- semantic-conventions.md
- ../python/pydantic-ai/phoenix-integration.md
- arize/docker-compose-deployment.md
sources:
- name: OpenTelemetry Core Concepts
  url: https://opentelemetry.io/docs/concepts/
- name: OpenTelemetry Trace SDK Specification
  url: https://opentelemetry.io/docs/specs/otel/trace/sdk/
- name: OpenTelemetry Attribute Naming Conventions
  url: https://opentelemetry.io/docs/specs/otel/common/attribute-naming/
- name: OpenTelemetry Context API Specification
  url: https://opentelemetry.io/docs/specs/otel/context/
- name: OpenTelemetry Collector Deployment
  url: https://opentelemetry.io/docs/collector/deployment/
- name: OpenTelemetry Python Instrumentation
  url: https://opentelemetry.io/docs/languages/python/instrumentation/
- name: OpenTelemetry Performance Specification
  url: https://opentelemetry.io/docs/specs/otel/performance/
- name: OpenTelemetry Resource SDK Specification
  url: https://opentelemetry.io/docs/specs/otel/resource/sdk/
- name: OpenTelemetry SDK Environment Variables
  url: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/
- name: OpenTelemetry Trace API Specification
  url: https://opentelemetry.io/docs/specs/otel/trace/api/
- name: OpenTelemetry Resource Semantic Conventions
  url: https://opentelemetry.io/docs/specs/semconv/resource/
- name: OpenTelemetry Baggage API Specification
  url: https://opentelemetry.io/docs/specs/otel/baggage/api/
- name: OpenTelemetry Collector Configuration
  url: https://opentelemetry.io/docs/collector/configuration/
- name: OpenTelemetry OTLP Exporter Specification
  url: https://opentelemetry.io/docs/specs/otel/protocol/exporter/
- name: OpenTelemetry Collector Scaling
  url: https://opentelemetry.io/docs/collector/scaling/
status: stable
subcategory: telemetry-standards
tags:
- opentelemetry
- observability
- tracing
- metrics
- instrumentation
- otel
- telemetry
- collector
title: OpenTelemetry Best Practices
type: pattern-reference
version: '1.0'
---

# OpenTelemetry Best Practices

Comprehensive guide to implementing OpenTelemetry instrumentation, configuration, and production deployment patterns based on official specifications.

## Overview

OpenTelemetry provides a vendor-neutral standard for generating, collecting, and exporting telemetry data including traces, metrics, and logs. ([OpenTelemetry Core Concepts][1])

This reference covers best practices for:
- Core concepts and architecture
- Instrumentation patterns
- Performance optimization
- Production deployment
- SDK configuration
- Common patterns and anti-patterns

## Core Concepts & Architecture

### Telemetry Signals

OpenTelemetry supports four primary telemetry signals: ([OpenTelemetry Core Concepts][1])

- **Traces**: Distributed request tracking across services
- **Metrics**: Quantitative measurements and performance indicators
- **Logs**: Textual event records from applications
- **Baggage**: Context data propagated across service boundaries

### Context Propagation

Context propagation enables distributed tracing by allowing trace identifiers and contextual information to flow between services. ([OpenTelemetry Core Concepts][1])

**Key Implementation Requirements** ([OpenTelemetry Context API Specification][4]):

- Keys must be unique across library boundaries
- Context values are immutable—write operations create new Context instances
- Multiple calls to `CreateKey` with the same name should not return the same value unless language constraints dictate otherwise
- In languages with implicit Context management, three additional operations are required: Get Current Context, Attach Context, and Detach Context

**Best Practice**: Avoid direct Context API manipulation in languages with implicit handling. Instead, use higher-level APIs from cross-cutting concerns like tracing and baggage. ([OpenTelemetry Context API Specification][4])

### Sampling Strategies

Sampling reduces data volume while maintaining statistical relevance. The SDK defines two critical decision flags: ([OpenTelemetry Trace SDK Specification][2])

- **IsRecording**: Controls data collection (attributes, events, status)
- **Sampled**: Propagates via SpanContext to descendants

The combination `Sampled=false` with `IsRecording=true` is valid for downstream sampling, but the reverse is forbidden. ([OpenTelemetry Trace SDK Specification][2])

#### Built-in Samplers

**AlwaysOn/AlwaysOff** ([OpenTelemetry Trace SDK Specification][2]): Deterministic samplers returning constant decisions.

**TraceIdRatioBased** ([OpenTelemetry Trace SDK Specification][2]): Uses deterministic hash of the TraceId when computing the sampling decision to ensure child spans inherit parent sampling decisions consistently.

**ProbabilitySampler** ([OpenTelemetry Trace SDK Specification][2]): Implements W3C Trace Context Level 2 standards using 56 bits of randomness with the formula `R >= T` where R is randomness and T is threshold.

**ParentBased** ([OpenTelemetry Trace SDK Specification][2]): Decorator distinguishing between root spans, remote parents with sampled/unsampled flags, and local parents with sampled/unsampled flags. Delegates to configurable child samplers for each case.

**CompositeSampler** ([OpenTelemetry Trace SDK Specification][2]): Enables composition through `ComposableSampler` interface supporting ComposableAlwaysOn/Off, ComposableProbability, ComposableParentThreshold, ComposableRuleBased, and ComposableAnnotating.

**Randomness Requirements**: SDKs should implement the TraceID randomness requirements of the W3C Trace Context Level 2 for root spans. SDKs must not overwrite user-provided explicit randomness. ([OpenTelemetry Trace SDK Specification][2])

### Resource Semantic Conventions

Resources identify the entity producing telemetry through immutable attributes. A Resource is an immutable representation of the entity producing telemetry as Attributes. ([OpenTelemetry Resource SDK Specification][8])

#### Core Service Attributes

**`service.name`** (Required, Stable) ([OpenTelemetry Resource Semantic Conventions][11]): Logical name of the service. Example: `shoppingcart`. SDKs must default to `unknown_service:` prefixed with the process executable name if unspecified.

**`service.instance.id`** (Recommended) ([OpenTelemetry Resource Semantic Conventions][11]): Globally unique identifier for each service instance.

**`service.namespace`** (Recommended) ([OpenTelemetry Resource Semantic Conventions][11]): Groups services by logical boundaries (e.g., team ownership).

**`service.version`** (Recommended, Stable) ([OpenTelemetry Resource Semantic Conventions][11]): Service version string without format restrictions.

#### Telemetry SDK Attributes

Required attributes for SDK identification: ([OpenTelemetry Resource Semantic Conventions][11])

- **`telemetry.sdk.name`**: Must be `opentelemetry` for standard SDK implementations
- **`telemetry.sdk.language`**: Language identifier (cpp, dotnet, go, java, nodejs, python, ruby, rust, webjs)
- **`telemetry.sdk.version`**: SDK version string

#### Resource Merging

If a key exists on both the old and updating resource, the value of the updating resource must be picked (even if the updated value is empty). Schema URL merging has strict rules—different non-empty URLs constitute errors. ([OpenTelemetry Resource SDK Specification][8])

**Best Practice**: Maintain consistent `service.name` across horizontally scaled instances and use stable, opaque identifiers for `service.instance.id` rather than exposing sensitive metadata. ([OpenTelemetry Resource Semantic Conventions][11])

## Instrumentation Best Practices

### Auto vs Manual Instrumentation

OpenTelemetry provides three instrumentation methods: ([OpenTelemetry Core Concepts][1])

- **Zero-code instrumentation**: Automatic telemetry without code modifications
- **Code-based instrumentation**: Direct API usage within application logic
- **Library instrumentation**: Pre-built integrations for popular frameworks

#### Python-Specific Guidance

**Manual Instrumentation** ([OpenTelemetry Python Instrumentation][6]): When instrumenting an application, install both API and SDK packages (`opentelemetry-api` and `opentelemetry-sdk`).

**Library Instrumentation** ([OpenTelemetry Python Instrumentation][6]): When creating a library, install only the API package—the library won't emit telemetry independently.

**Common Pitfall**: Using both zero-code and manual instrumentation simultaneously can cause duplicate instrumentation. ([OpenTelemetry Python Instrumentation][6])

### Span Naming Conventions

Span names should identify the operation class broadly rather than specific instances. Example: `get_account` is preferable to `get_account/42` to maintain reasonable cardinality. ([OpenTelemetry Trace API Specification][10])

**Critical Timing**: Adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation. ([OpenTelemetry Trace API Specification][10])

#### Required Parameters

Span creation requires: ([OpenTelemetry Trace API Specification][10])

- **Span name** (required)
- **Parent Context**: May implicitly use current context or explicitly specify a root span
- **SpanKind** (optional): Defaults to `Internal`
- **Attributes** (optional): Empty collection assumed if unspecified
- **Links**: Ordered sequence of related spans
- **Start timestamp** (optional): Defaults to current time

### Span Creation Patterns

#### Context Manager Approach (Recommended)

```python
with tracer.start_as_current_span("operation-name") as span:
    # Work is tracked here
    # Span automatically closes when exiting block
```

This pattern guarantees span closure even if exceptions occur, eliminating manual cleanup overhead. ([OpenTelemetry Python Instrumentation][6])

#### Decorator Pattern for Functions

```python
@tracer.start_as_current_span("do_work")
def do_work():
    print("doing some work...")
```

**Caveat**: Requires `tracer` availability in the function's scope. ([OpenTelemetry Python Instrumentation][6])

#### Concurrent Operations

Use `start_span()` without making it current for tracking parallel operations that shouldn't establish parent-child relationships with the calling context. ([OpenTelemetry Python Instrumentation][6])

### Attribute Best Practices

#### Naming Conventions

Attribute naming rules: ([OpenTelemetry Attribute Naming Conventions][3])

- Use lowercase characters
- Follow namespacing with dot delimiters (e.g., `service.version`)
- Multi-word components within a namespace use snake_case (e.g., `http.response.status_code`)
- Use namespacing (and dot separator) whenever it makes sense. For example when introducing an attribute representing a property of some object, follow `{object}.{property}` pattern.

**Precision Requirements**: Be precise. Attribute, event, metric, and other names should be descriptive and unambiguous. Include specific property names—use `file.owner.name` instead of `file.owner`. ([OpenTelemetry Attribute Naming Conventions][3])

#### Pluralization Rules

([OpenTelemetry Attribute Naming Conventions][3])

- Singular form for single entities: `host.name`, `container.id`
- Plural form when representing multiple entities with array values: `process.command_args`
- For metrics: Pluralize names only when recording discrete, countable quantities

**Reserved Namespaces**: Attribute names that start with `otel.` are reserved to be defined by OpenTelemetry specification. ([OpenTelemetry Attribute Naming Conventions][3])

#### Semantic Attributes (Recommended)

```python
from opentelemetry.semconv.trace import SpanAttributes

span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
span.set_attribute(SpanAttributes.HTTP_URL, "https://example.com")
```

Semantic attributes enable normalized data collection and better cross-system correlation. ([OpenTelemetry Python Instrumentation][6])

#### Anti-Patterns to Avoid

([OpenTelemetry Attribute Naming Conventions][3])

- **Name reuse**: Two attributes, metrics, or events cannot share identical names
- **Unclear scope**: Avoid generic names like `rule` when `security_rule` provides clarity
- **Unnecessary nesting**: Don't use `vcs.repository.change.id` when `vcs.change.id` is equally precise
- **Non-Latin characters**: Limit to printable Basic Latin characters (U+0021 through U+007E)

### Error Handling and Status Codes

#### Exception Recording Pattern

```python
from opentelemetry.trace import Status, StatusCode

try:
    risky_operation()
except Exception as ex:
    current_span.set_status(Status(StatusCode.ERROR))
    current_span.record_exception(ex)
```

([OpenTelemetry Python Instrumentation][6])

#### Status Values

([OpenTelemetry Python Instrumentation][6], [OpenTelemetry Trace API Specification][10])

- `ERROR`: Operation failed
- `OK`: Explicitly successful (overrides default)
- `Unset`: Default—operation completed without error

**Key Guidelines**: ([OpenTelemetry Trace API Specification][10])

- Status consists of StatusCode (Unset, Ok, or Error) and Description (only valid with Error)
- Status ordering (Ok > Error > Unset) means Ok status overrides prior Error attempts
- Instrumentation Libraries should not set the status code to Ok, unless explicitly configured to do so

### SpanKind Classification

Five kinds clarify span relationships: ([OpenTelemetry Trace API Specification][10])

| Kind | Direction | Style |
|------|-----------|-------|
| SERVER | Incoming | Request/Response |
| CLIENT | Outgoing | Request/Response |
| PRODUCER | Outgoing | Deferred |
| CONSUMER | Incoming | Deferred |
| INTERNAL | Local | Any |

## Performance & Resource Management

### Core Performance Principles

The specification establishes two fundamental guidelines: ([OpenTelemetry Performance Specification][7])

1. Library should not block end-user application by default.
2. Library should not consume unbounded memory resource.

### Batching Strategies

#### Batch Span Processor Configuration

Accumulates spans and exports on conditions: ([OpenTelemetry Trace SDK Specification][2])

- `scheduledDelayMillis` interval (default: 5000ms)
- Queue reaches `maxExportBatchSize` (default: 512)
- ForceFlush called

#### Default Parameters

([OpenTelemetry SDK Environment Variables][9])

| Variable | Default |
|----------|---------|
| `OTEL_BSP_SCHEDULE_DELAY` | 5000 ms |
| `OTEL_BSP_EXPORT_TIMEOUT` | 30000 ms |
| `OTEL_BSP_MAX_QUEUE_SIZE` | 2048 |
| `OTEL_BSP_MAX_EXPORT_BATCH_SIZE` | 512 |

#### Simple Processor

Immediately exports finished spans. Must synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. ([OpenTelemetry Trace SDK Specification][2])

**Best Practice**: Use batch processors in production for efficiency; use simple processors only in development or low-throughput scenarios.

### Sampling Configurations

#### Environment Variables

([OpenTelemetry SDK Environment Variables][9])

| Variable | Purpose | Default |
|----------|---------|---------|
| `OTEL_TRACES_SAMPLER` | Sampler type for traces | "parentbased_always_on" |
| `OTEL_TRACES_SAMPLER_ARG` | Sampler configuration argument | - |

**Sampler types**: always_on, always_off, traceidratio, parentbased_always_on, parentbased_always_off, parentbased_traceidratio, jaeger_remote, parentbased_jaeger_remote, xray

### Memory Management

#### Span Limits Configuration

Default limits control span bloat: ([OpenTelemetry Trace SDK Specification][2])

- **AttributeCountLimit**: 128 attributes per span
- **EventCountLimit**: 128 events
- **LinkCountLimit**: 128 links
- **AttributePerEventCountLimit**: 128 attributes per event
- **AttributePerLinkCountLimit**: 128 attributes per link

The specification requires a message printed in the SDK's log to indicate that an attribute, event, or link was discarded, printed at most once per span. ([OpenTelemetry Trace SDK Specification][2])

#### Environment Variables

([OpenTelemetry SDK Environment Variables][9])

| Variable | Default |
|----------|---------|
| `OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT` | no limit |
| `OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` | 128 |
| `OTEL_SPAN_EVENT_COUNT_LIMIT` | 128 |
| `OTEL_SPAN_LINK_COUNT_LIMIT` | 128 |
| `OTEL_EVENT_ATTRIBUTE_COUNT_LIMIT` | 128 |
| `OTEL_LINK_ATTRIBUTE_COUNT_LIMIT` | 128 |

#### Log Volume Management

([OpenTelemetry Performance Specification][7])

- Implement log filtering capabilities so applications can selectively send data to exporters
- High-volume logging requires intentional resource management
- Guide users on filtering strategies to bound resource consumption

### Performance Overhead Considerations

#### Non-Blocking vs. Memory Consumption Trade-off

The specification acknowledges an inherent tension: background tasks may accumulate state and consume memory. OpenTelemetry clients should offer configurable options: ([OpenTelemetry Performance Specification][7])

- **Information Preservation Mode**: Retain all telemetry data (potentially higher resource usage)
- **Blocking Prevention Mode**: Drop information under excessive load with configurable thresholds and warning notifications

#### Shutdown and Flushing Operations

([OpenTelemetry Performance Specification][7])

- These operations may necessarily block to prevent data loss
- Implementations should support user-configurable timeout values during shutdown
- Allow explicit flush operations with adjustable timeout parameters

#### Span Lifecycle Best Practices

([OpenTelemetry Trace API Specification][10])

- **End()** must complete quickly—no blocking I/O
- Subsequent calls to End() should be ignored
- End must not inactivate the Span in any Context it is active in

## Production Deployment

### Collector Architecture Patterns

OpenTelemetry Collector supports three primary deployment patterns: ([OpenTelemetry Collector Deployment][5])

**1. No Collector Pattern**: Direct signal transmission from applications to backend systems, bypassing intermediary processing.

**2. Agent Pattern**: Send signals to collectors and from there to backends—applications forward telemetry to local or nearby Collector instances, which then route to observability backends.

**3. Gateway Pattern**: Send signals to a single OTLP endpoint and from there to backends—centralized collection point receiving telemetry from multiple sources before backend distribution.

### High Availability Setups

#### Horizontal Scaling Strategies

**Stateless Components** ([OpenTelemetry Collector Scaling][15]): Most Collector components scale easily through replication. Adding new replicas and distributing traffic among them using a load balancer enables straightforward horizontal expansion for receivers and processors without state concerns.

#### Load Balancing Requirements

([OpenTelemetry Collector Scaling][15])

- Use Layer 7 (gRPC-aware) load balancers for OTLP traffic to avoid persistent connections to single instances
- Kubernetes environments should leverage service mesh solutions (Istio, Linkerd) or cloud provider load balancers for mature traffic management

#### Deployment Patterns

([OpenTelemetry Collector Scaling][15])

- **Sidecar Pattern**: Deploy collectors alongside application pods for local processing and improved gRPC load distribution
- **DaemonSet Pattern**: Place collectors on each node for node-level telemetry with central processing layers

#### Stateful Component Handling

Components maintaining in-memory state (tail-sampling processor, span-to-metrics processor) require special consideration: ([OpenTelemetry Collector Scaling][15])

- Place a load-balancing exporter layer in front using trace ID or service name hashing
- Ensures consistent routing of related spans to the same backend instance, preventing incomplete traces

### Security Best Practices

#### OTLP Exporter TLS Configuration

([OpenTelemetry OTLP Exporter Specification][14])

| Variable | Purpose |
|----------|---------|
| `OTEL_EXPORTER_OTLP_CERTIFICATE` | Certificate file |
| `OTEL_EXPORTER_OTLP_CLIENT_KEY` | Client key file |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` | Client certificate |
| `OTEL_EXPORTER_OTLP_INSECURE` | Insecure mode (default: false; gRPC only) |

#### Collector Authentication

([OpenTelemetry Collector Configuration][13])

```yaml
extensions:
  oidc:
    issuer_url: http://localhost:8080/auth/realms/opentelemetry
    audience: collector

receivers:
  otlp/auth:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        auth:
          authenticator: oidc
```

#### Best Practices for Production

([OpenTelemetry OTLP Exporter Specification][14])

1. Use signal-specific endpoints for multi-collector architectures
2. Configure appropriate timeouts for your network latency
3. Enable compression (gzip) for high-volume deployments
4. Implement mutual TLS in secure environments
5. Set custom User-Agent headers to identify your distribution

### Configuration Management

#### Collector Configuration Structure

The Collector's configuration consists of four pipeline components: ([OpenTelemetry Collector Configuration][13])

- **Receivers**: Collect telemetry from sources (push or pull-based)
- **Processors**: Modify/transform data before export
- **Exporters**: Send data to backends or destinations
- **Connectors**: Join pipelines acting as both exporter and receiver

#### Key Configuration Practices

([OpenTelemetry Collector Configuration][13])

- Configuring a receiver does not enable it. Receivers are enabled by adding them to appropriate pipelines within the service section
- The order of the processors in a pipeline determines the order of processing operations
- Configuring an exporter does not enable it—activation occurs in service pipelines

#### Multiple Configuration Files

Merge configurations using `--config` flag multiple times: ([OpenTelemetry Collector Configuration][13])

```bash
otelcol --config=file:/path/to/first --config=file:/path/to/second
```

#### Environment Variable Support

([OpenTelemetry Collector Configuration][13])

- Expand variables: `${env:DB_KEY}`
- Include defaults: `${env:DB_KEY:-default-value}`
- Escape literal `$`: Use `$$`

#### Configuration Validation

```bash
otelcol validate --config=customconfig.yaml
```

([OpenTelemetry Collector Configuration][13])

## SDK Configuration

### Exporter Configuration

#### OTLP Protocol Options

The OTLP exporter supports three transport protocols: ([OpenTelemetry OTLP Exporter Specification][14])

- **gRPC**: protobuf-encoded data using gRPC wire format over HTTP/2
- **HTTP/Protobuf**: protobuf over standard HTTP connections
- **HTTP/JSON**: JSON-encoded data via HTTP

The specification recommends `http/protobuf` as the default unless backward compatibility requires otherwise. ([OpenTelemetry OTLP Exporter Specification][14])

#### Default Endpoints

([OpenTelemetry OTLP Exporter Specification][14])

- **OTLP/HTTP**: `http://localhost:4318`
- **OTLP/gRPC**: `http://localhost:4317`

#### Environment Variables

Per-signal endpoints take precedence: ([OpenTelemetry OTLP Exporter Specification][14], [OpenTelemetry SDK Environment Variables][9])

- `OTEL_EXPORTER_OTLP_ENDPOINT` (base URL)
- `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`
- `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`
- `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`

#### Exporter Selection

([OpenTelemetry SDK Environment Variables][9])

| Variable | Default |
|----------|---------|
| `OTEL_TRACES_EXPORTER` | "otlp" |
| `OTEL_METRICS_EXPORTER` | "otlp" |
| `OTEL_LOGS_EXPORTER` | "otlp" |

Values: otlp, zipkin (traces), prometheus (metrics), console, logging (deprecated), none, otlp/stdout (development)

### Processor Pipelines

#### Recommended Processors

([OpenTelemetry Collector Configuration][13])

- `memory_limiter`: Resource management
- `attributes`: Add/modify/delete attributes
- `filter`: Conditional data filtering
- `resource`: Modify resource attributes

#### Pipeline Definition

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter]
      exporters: [otlp]
    metrics:
      receivers: [otlp]
      exporters: [otlp]
```

([OpenTelemetry Collector Configuration][13])

#### Span Processor Interface

Processors implement hooks at span lifecycle events, processing only spans where `IsRecording` is true. ([OpenTelemetry Trace SDK Specification][2])

**Interface Methods** ([OpenTelemetry Trace SDK Specification][2]):

- **OnStart**: Synchronous callback when span begins—can maintain references but must not block
- **OnEnding**: Called during `End()` operation—span still mutable for final modifications
- **OnEnd**: Called after span termination—receives readable span (immutable)
- **Shutdown**: Cleanup operation called once per processor instance
- **ForceFlush**: Export hint that triggers export of pending spans

### Resource Detectors

**Custom Detectors** ([OpenTelemetry Resource SDK Specification][8]): For platforms (Docker, Kubernetes) and vendor environments (EKS, AKS, GKE), implemented as separate packages.

**Reserved detector names for built-in detectors** ([OpenTelemetry Resource SDK Specification][8]):
- `container`, `host`, `process`, `service`

Detector names should use snake_case with lowercase alphanumeric characters and underscores, reflecting the root namespace of attributes they populate.

#### Environment Variable Configuration

The SDK extracts resource information from `OTEL_RESOURCE_ATTRIBUTES` in W3C Baggage format: `key1=value1,key2=value2`. User-provided resources take priority over environment variable attributes when merging. ([OpenTelemetry Resource SDK Specification][8])

### Environment Variables

#### General SDK Configuration

([OpenTelemetry SDK Environment Variables][9])

| Variable | Purpose | Default | Type |
|----------|---------|---------|------|
| `OTEL_SDK_DISABLED` | Disables SDK for all signals | false | Boolean |
| `OTEL_SERVICE_NAME` | Sets service name resource attribute | - | String |
| `OTEL_RESOURCE_ATTRIBUTES` | Key-value pairs for resource attributes | - | String |
| `OTEL_LOG_LEVEL` | Internal SDK logger level | "info" | Enum |
| `OTEL_PROPAGATORS` | Propagators to be used as a comma-separated list | "tracecontext,baggage" | Enum |

**Propagator values** ([OpenTelemetry SDK Environment Variables][9]): tracecontext, baggage, b3, b3multi, jaeger, xray, ottrace, none

#### Configuration Type Guidelines

([OpenTelemetry SDK Environment Variables][9])

- **Boolean**: Case-insensitive "true" only; all other values = false
- **Integer**: Non-negative values 0 to 2³¹ − 1
- **Duration**: Non-negative milliseconds
- **Timeout**: Milliseconds (zero = infinite/no limit)
- **Enum**: Case-insensitive values; unrecognized values trigger warning and are ignored

## Common Patterns

### Service Naming

**Best Practices** ([OpenTelemetry Resource Semantic Conventions][11]):

- Maintain consistent `service.name` across horizontally scaled instances
- Use `service.namespace` to distinguish organizational groupings
- SDKs must default to `unknown_service:` prefixed with the process executable name if `service.name` is unspecified

#### Python Provider Initialization

```python
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("module.name")
```

([OpenTelemetry Python Instrumentation][6])

#### Tracer Naming

Use module-level tracer names (`__name__`) for easier trace filtering: ([OpenTelemetry Python Instrumentation][6])

```python
tracer = trace.get_tracer(__name__)
```

### Version Tracking

**Service Version Attribute** ([OpenTelemetry Resource Semantic Conventions][11]):

- **`service.version`** (Recommended, Stable): Service version string without format restrictions
- Include version attributes for artifact identification and lifecycle tracking

### Error and Exception Handling

#### Complete Error Recording Pattern

```python
from opentelemetry.trace import Status, StatusCode

try:
    risky_operation()
except Exception as ex:
    current_span.set_status(Status(StatusCode.ERROR))
    current_span.record_exception(ex)
```

([OpenTelemetry Python Instrumentation][6])

#### Events and Logging

Record discrete occurrences without exceptions: ([OpenTelemetry Python Instrumentation][6])

```python
current_span.add_event("Starting operation")
# ... work ...
current_span.add_event("Operation completed")
```

Events function as primitive logs marking significant moments during span lifetime.

### Custom Attributes and Events

#### Custom Attribute Prefixing

Application developers should prefix company or application-specific attributes with reverse domain names (`com.acme.shopname`) or reasonably unique application names to prevent clashes in distributed systems. ([OpenTelemetry Attribute Naming Conventions][3])

#### Retrieving Current Span

Access the active span for enrichment without creating a new one: ([OpenTelemetry Python Instrumentation][6])

```python
current_span = trace.get_current_span()
current_span.set_attribute("key", "value")
```

### Baggage Handling

**Baggage Overview** ([OpenTelemetry Baggage API Specification][12]): Baggage is a set of application-defined properties contextually associated with a distributed request or workflow execution. Each name maps to exactly one value.

#### Core Operations

([OpenTelemetry Baggage API Specification][12])

- **Get Value**: Retrieves a value by name, returning null if absent
- **Get All Values**: Returns all name/value pairs as an immutable collection or iterator
- **Set Value**: Creates a new Baggage instance with updated entries. Accepts optional metadata as an opaque wrapper for a string with no semantic meaning
- **Remove Value**: Produces a new Baggage instance excluding specified names

**Security Consideration**: Clear all baggage entries to prevent propagation to untrusted processes. ([OpenTelemetry Baggage API Specification][12])

#### Propagation

A TextMapPropagator implementing the W3C Baggage Specification is mandatory. The propagator stores metadata on extract and appends it per W3C format on inject. ([OpenTelemetry Baggage API Specification][12])

### Span Links

**Use Case**: Connect causally-related spans without parent-child hierarchy: ([OpenTelemetry Python Instrumentation][6])

```python
ctx = trace.get_current_span().get_span_context()
link = trace.Link(ctx)

with tracer.start_as_current_span("span-2", links=[link]):
    pass  # linked to span-1 but not a child
```

Useful for tracking requests that spawn independent operations.

### Context Propagation Format

#### Override Default Format

Default W3C formats (Trace Context + Baggage) can be overridden via environment variable: ([OpenTelemetry Python Instrumentation][6])

```bash
OTEL_PROPAGATORS="b3,baggage"
```

Or programmatically:

```python
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format

set_global_textmap(B3Format())
```

## Capacity Planning & Monitoring

### Scale-Up Indicators

**Key Metrics to Monitor** ([OpenTelemetry Collector Scaling][15]):

- `otelcol_processor_refused_spans`: Data being blocked suggests memory pressure
- Watch exporter queue metrics: scale at 60-70% of `otelcol_exporter_queue_capacity`
- For scrapers: scale when scrape completion approaches the scrape interval

### Scale-Down Indicators

**Resource Underutilization**: Consistently low queue sizes and memory consumption below limits indicate scaling down opportunities. ([OpenTelemetry Collector Scaling][15])

### When NOT to Scale

**External Bottlenecks** ([OpenTelemetry Collector Scaling][15]):

Scaling won't help when bottlenecks exist outside the collector:
- Backend systems unable to process incoming data
- Network saturation between collector and backend
- Rising `otelcol_exporter_send_failed_spans` indicates downstream problems, not collector capacity issues

### Resource Allocation

**Memory Limiter Implementation**: Implement memory limits via the `memory_limiter` processor to prevent resource exhaustion and enable informed scaling decisions based on observed refusal metrics. ([OpenTelemetry Collector Scaling][15])

## Common Anti-Patterns to Avoid

### Instrumentation Anti-Patterns

([OpenTelemetry Python Instrumentation][6])

1. **Forgetting Context**: Not using context managers leads to resource leaks
2. **Global Tracer Assumptions**: Decorators fail if `tracer` isn't globally available
3. **Ignoring Timeouts in Async Callbacks**: Asynchronous instruments must respect provided timeout values to prevent blocking
4. **Mixing Manual and Zero-Code**: Using both simultaneously can cause duplicate instrumentation
5. **Skipping Semantic Conventions**: Custom attribute names prevent cross-system analysis

### API Usage Anti-Patterns

([OpenTelemetry Trace API Specification][10])

- Creating spans outside Tracer instances (prohibited by specification)
- Setting span as active in current context by default during creation
- Performing blocking I/O in End() method
- Calling End() multiple times with side effects
- Not ending created spans (resource leak)

### Configuration Anti-Patterns

([OpenTelemetry Attribute Naming Conventions][3])

- **Name reuse**: Two attributes, metrics, or events cannot share identical names
- **Unclear scope**: Avoid generic names like `rule` when `security_rule` provides clarity
- **Unnecessary nesting**: Don't use `vcs.repository.change.id` when `vcs.change.id` is equally precise
- **Inconsistent conventions**: Don't prefix company-specific attributes with existing OpenTelemetry namespaces

## Related References

- [Pydantic AI Phoenix Integration](../pydantic-ai/phoenix-integration.md) - Integration with Phoenix observability platform
- [Arize Docker Compose Deployment](../arize/docker-compose-deployment.md) - Phoenix deployment patterns

[1]: https://opentelemetry.io/docs/concepts/ "OpenTelemetry Core Concepts"
[2]: https://opentelemetry.io/docs/specs/otel/trace/sdk/ "OpenTelemetry Trace SDK Specification"
[3]: https://opentelemetry.io/docs/specs/otel/common/attribute-naming/ "OpenTelemetry Attribute Naming Conventions"
[4]: https://opentelemetry.io/docs/specs/otel/context/ "OpenTelemetry Context API Specification"
[5]: https://opentelemetry.io/docs/collector/deployment/ "OpenTelemetry Collector Deployment"
[6]: https://opentelemetry.io/docs/languages/python/instrumentation/ "OpenTelemetry Python Instrumentation"
[7]: https://opentelemetry.io/docs/specs/otel/performance/ "OpenTelemetry Performance Specification"
[8]: https://opentelemetry.io/docs/specs/otel/resource/sdk/ "OpenTelemetry Resource SDK Specification"
[9]: https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/ "OpenTelemetry SDK Environment Variables"
[10]: https://opentelemetry.io/docs/specs/otel/trace/api/ "OpenTelemetry Trace API Specification"
[11]: https://opentelemetry.io/docs/specs/semconv/resource/ "OpenTelemetry Resource Semantic Conventions"
[12]: https://opentelemetry.io/docs/specs/otel/baggage/api/ "OpenTelemetry Baggage API Specification"
[13]: https://opentelemetry.io/docs/collector/configuration/ "OpenTelemetry Collector Configuration"
[14]: https://opentelemetry.io/docs/specs/otel/protocol/exporter/ "OpenTelemetry OTLP Exporter Specification"
[15]: https://opentelemetry.io/docs/collector/scaling/ "OpenTelemetry Collector Scaling"