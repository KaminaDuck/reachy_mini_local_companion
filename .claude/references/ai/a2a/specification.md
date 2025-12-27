---
title: "A2A Protocol Technical Specification"
description: "Complete technical specification for the Agent2Agent (A2A) Protocol v0.3.0"
type: "standard-spec"
tags: ["protocol", "agent-communication", "multi-agent", "interoperability", "api-standard", "json-rpc", "grpc", "rest", "http", "streaming", "sse", "task-management"]
category: "ai"
subcategory: "protocols"
version: "0.3.0"
last_updated: "2025-07-01"
status: "stable"
sources:
  - name: "A2A Protocol Official Site"
    url: "https://a2a-protocol.org/"
  - name: "A2A Protocol Specification"
    url: "https://a2a-protocol.org/latest/specification/"
  - name: "A2A GitHub Repository"
    url: "https://github.com/a2aproject/A2A"
  - name: "A2A Protocol Specification Files"
    url: "https://github.com/a2aproject/A2A/tree/main/specification"
  - name: "A2A Roadmap"
    url: "https://a2a-protocol.org/latest/roadmap/"
  - name: "A2A Release Notes"
    url: "https://github.com/a2aproject/A2A/releases"
related: ["overview.md", "security-implementation.md"]
author: "unknown"
contributors: []
---

# A2A Protocol Technical Specification

Complete technical specification for the Agent2Agent (A2A) Protocol version 0.3.0, enabling AI agents to communicate and collaborate across different platforms and frameworks.

## Protocol Overview

The Agent2Agent (A2A) Protocol is an open standard that enables AI agents to communicate and collaborate across different platforms and frameworks. ([A2A Protocol Site][1]) Originally developed by Google LLC and now governed by the Linux Foundation, A2A is licensed under Apache License 2.0. ([A2A GitHub][3])

Version 0.3.0, released in July 2025, is the first stable release with backward compatibility commitments. ([A2A Releases][6]) The protocol provides opaque agent communication where agents collaborate via declared capabilities and exchanged messages without exposing internal state, memory, or tools. ([A2A Specification][2])

## Transport Protocols

A2A supports three transport mechanisms. Implementations MUST support at least one transport and SHOULD support multiple transports for interoperability. ([A2A Specification][2])

### JSON-RPC 2.0 Transport

The primary transport mechanism uses JSON-RPC 2.0 over HTTP. ([A2A Specification][2])

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "method": "category/action",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "result": {
    "field1": "value1"
  }
}
```

**Error Format:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": {"detail": "Additional context"}
  }
}
```

**Characteristics:**
- Content-Type: `application/json`
- Method naming convention: `{category}/{action}` (e.g., `message/send`, `tasks/get`)
- Streaming via Server-Sent Events (SSE) with JSON-RPC responses
- HTTP POST requests to agent endpoint URL

### gRPC Transport

Protocol Buffers-based transport for high-performance scenarios. ([A2A Specification][2])

**Service Definition:**
- Protocol Buffers v3 serialization
- Normative definition: `specification/grpc/a2a.proto` ([A2A Spec Files][4])
- Service name: `A2AService`
- HTTP/2 with TLS encryption required
- Bidirectional streaming support

**Message Types:**
- Request messages map to protocol buffer messages
- Response messages use standard gRPC response patterns
- Streaming responses use server streaming RPC

### HTTP+JSON/REST Transport

RESTful HTTP transport with standard verbs. ([A2A Specification][2])

**URL Patterns:**
```
/v1/{resource}[/{id}][:{action}]
```

**HTTP Verb Mapping:**
- `GET /v1/tasks/{taskId}` - Retrieve task status
- `POST /v1/message` - Send message
- `DELETE /v1/tasks/{taskId}` - Cancel task
- `POST /v1/tasks/{taskId}:resubscribe` - Resume streaming

**Characteristics:**
- Standard HTTP status codes
- JSON request/response bodies
- SSE for streaming responses
- Content-Type: `application/json`

## Agent Card Schema

Every A2A agent MUST publish an Agent Card at the well-known URI `/.well-known/agent-card.json` (RFC 8615 compliant). ([A2A Specification][2])

### Required Fields

```yaml
protocolVersion: "0.3.0"  # REQUIRED: Protocol version
name: "Agent Name"         # REQUIRED: Human-readable name
description: "Agent description"  # REQUIRED: Purpose and capabilities
version: "1.0.0"           # REQUIRED: Agent version
url: "https://agent.example.com"  # REQUIRED: Primary HTTPS endpoint
preferredTransport: "JSONRPC"  # REQUIRED: TransportProtocol enum
```

### Transport Protocol Enum

Valid values for `preferredTransport` and `additionalInterfaces[].transport`:
- `JSONRPC` - JSON-RPC 2.0 over HTTP
- `GRPC` - gRPC with Protocol Buffers
- `REST` - HTTP+JSON RESTful transport

### Optional Fields

```yaml
additionalInterfaces:  # Alternative transports and endpoints
  - transport: "GRPC"
    url: "https://agent.example.com:443"
  - transport: "REST"
    url: "https://agent.example.com/api"

capabilities:  # Supported features
  streaming: true                    # Supports message/stream
  pushNotifications: true            # Supports webhook notifications
  stateTransitionHistory: true       # Provides task history
  extensions: ["custom-ext"]         # Custom extensions

defaultInputModes:   # Accepted content types
  - "text/plain"
  - "application/json"
  - "image/png"

defaultOutputModes:  # Generated content types
  - "text/plain"
  - "application/json"

skills:  # Agent capabilities array
  - name: "skill-name"
    description: "Skill description"
    inputModes: ["text/plain"]
    outputModes: ["text/plain"]
```

### Security Schemes

Agent Cards declare authentication requirements using OpenAPI-compatible security scheme objects. ([A2A Specification][2])

**API Key Authentication:**
```yaml
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key

security:
  - apiKey: []
```

**OAuth 2.0 Authentication:**
```yaml
securitySchemes:
  oauth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://auth.example.com/oauth/authorize
        tokenUrl: https://auth.example.com/oauth/token
        scopes:
          read: "Read access"
          write: "Write access"

security:
  - oauth2: ["read", "write"]
```

**HTTP Bearer Authentication:**
```yaml
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT

security:
  - bearerAuth: []
```

**OpenID Connect:**
```yaml
securitySchemes:
  openIdConnect:
    type: openIdConnect
    openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration

security:
  - openIdConnect: []
```

**Mutual TLS:**
```yaml
securitySchemes:
  mutualTLS:
    type: mutualTLS

security:
  - mutualTLS: []
```

### Signed Agent Cards (v0.3.0)

Agent Cards MAY include JWS (JSON Web Signature) signatures for integrity verification. ([A2A Releases][6])

```yaml
signatures:
  - keyId: "key-identifier"
    signature: "base64-encoded-jws-signature"
    algorithm: "RS256"
```

**Signature Verification:**
1. Extract public key using `keyId`
2. Verify JWS signature over canonical JSON representation
3. Validate signature algorithm matches expected algorithm
4. Check key expiration and revocation status

### Complete Agent Card Example

```json
{
  "protocolVersion": "0.3.0",
  "name": "Research Assistant Agent",
  "description": "Multi-modal research agent with web search and document analysis",
  "version": "2.1.0",
  "url": "https://research.example.com",
  "preferredTransport": "JSONRPC",
  "additionalInterfaces": [
    {
      "transport": "GRPC",
      "url": "https://research.example.com:443"
    }
  ],
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true,
    "extensions": []
  },
  "defaultInputModes": [
    "text/plain",
    "application/json",
    "image/png",
    "application/pdf"
  ],
  "defaultOutputModes": [
    "text/plain",
    "application/json"
  ],
  "skills": [
    {
      "name": "web-research",
      "description": "Search and analyze web content",
      "inputModes": ["text/plain"],
      "outputModes": ["text/plain", "application/json"]
    },
    {
      "name": "document-analysis",
      "description": "Extract and analyze document content",
      "inputModes": ["application/pdf", "text/plain"],
      "outputModes": ["application/json"]
    }
  ],
  "securitySchemes": {
    "oauth2": {
      "type": "oauth2",
      "flows": {
        "authorizationCode": {
          "authorizationUrl": "https://auth.example.com/oauth/authorize",
          "tokenUrl": "https://auth.example.com/oauth/token",
          "scopes": {
            "agent:read": "Read agent capabilities",
            "agent:execute": "Execute agent tasks"
          }
        }
      }
    }
  },
  "security": [
    {"oauth2": ["agent:read", "agent:execute"]}
  ]
}
```

## Task Lifecycle

Tasks are stateful units of work with unique IDs and defined lifecycle progression. ([A2A Specification][2])

### Task States

**Non-Terminal States:**
- `queued` - Task accepted, waiting to start
- `running` - Task actively executing
- `streaming-response` - Streaming partial results
- `input-required` - Awaiting additional input from client
- `auth-required` - Requires authentication for external system
- `waiting` - Paused, waiting for external event

**Terminal States:**
- `completed` - Task finished successfully
- `canceled` - Task canceled by client request
- `rejected` - Task rejected by agent (invalid, unauthorized, etc.)
- `failed` - Task failed due to error

### State Transitions

```
          ┌─────────┐
          │ queued  │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │ running │◄────────┐
          └────┬────┘         │
               │              │
     ┌─────────┼──────────────┤
     │         │              │
     ▼         ▼              │
┌─────────┐ ┌──────────────┐ │
│streaming│ │input-required├─┘
└────┬────┘ └──────┬───────┘
     │             │
     │             ▼
     │      ┌─────────────┐
     │      │auth-required│
     │      └──────┬──────┘
     │             │
     ▼             ▼
┌─────────┐  ┌─────────┐
│completed│  │ waiting │
└─────────┘  └────┬────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌────────┐
│canceled │  │rejected │  │ failed │
└─────────┘  └─────────┘  └────────┘
```

**Valid Transitions:**
- `queued` → `running`, `canceled`, `rejected`
- `running` → `streaming-response`, `input-required`, `auth-required`, `waiting`, `completed`, `failed`, `canceled`
- `streaming-response` → `completed`, `failed`, `canceled`
- `input-required` → `running`, `canceled`, `rejected`
- `auth-required` → `running`, `canceled`, `rejected`
- `waiting` → `running`, `canceled`, `failed`

### Task Object Schema

```typescript
interface Task {
  taskId: string;              // Unique task identifier
  state: TaskState;            // Current state
  createdAt: number;           // Unix timestamp (ms)
  updatedAt: number;           // Unix timestamp (ms)
  artifacts?: Artifact[];      // Generated outputs
  error?: ErrorObject;         // Error details (if failed/rejected)
  metadata?: Record<string, any>;  // Optional metadata
}
```

## Message Format

Messages are the primary communication mechanism between clients and agents. ([A2A Specification][2])

### Message Structure

```typescript
interface Message {
  role: "user" | "agent";      // Message originator
  parts: Part[];                // Content parts array
  timestamp?: number;           // Unix timestamp (ms)
  metadata?: Record<string, any>;  // Optional metadata
}
```

### Part Types

**Text Part:**
```typescript
interface TextPart {
  type: "text";
  text: string;                 // Plain text content
  mimeType?: string;            // Default: "text/plain"
}
```

**File Part:**
```typescript
interface FilePart {
  type: "file";
  file: FileWithBytes | FileWithUri;
  mimeType: string;             // MIME type of file
  filename?: string;            // Original filename
}

interface FileWithBytes {
  bytes: string;                // Base64-encoded file content
}

interface FileWithUri {
  uri: string;                  // Downloadable URL
  headers?: Record<string, string>;  // Optional HTTP headers
}
```

**Data Part:**
```typescript
interface DataPart {
  type: "data";
  data: any;                    // Structured JSON data
  schema?: string;              // JSON Schema URI (optional)
}
```

### Artifact Structure

Artifacts are agent-generated outputs composed of multiple parts. ([A2A Specification][2])

```typescript
interface Artifact {
  artifactId: string;           // Unique artifact identifier
  parts: Part[];                // Content parts
  createdAt: number;            // Unix timestamp (ms)
  metadata?: Record<string, any>;  // Optional metadata
}
```

## Protocol Methods

All methods are available across all three transports (JSON-RPC, gRPC, REST). ([A2A Specification][2])

### message/send

Synchronous message sending with task creation.

**Request:**
```typescript
interface MessageSendRequest {
  messages: Message[];          // Message history
  sessionId?: string;           // Optional session grouping
  context?: Record<string, any>;  // Optional context
}
```

**Response:**
```typescript
interface MessageSendResponse {
  task: Task;                   // Created task with status
}
```

**Behavior:**
- Creates new task in `queued` or `running` state
- Returns immediately with task object
- Client polls using `tasks/get` for updates
- Terminal state indicates completion

### message/stream

Streaming message execution with real-time updates.

**Request:**
```typescript
interface MessageStreamRequest {
  messages: Message[];          // Message history
  sessionId?: string;           // Optional session grouping
  context?: Record<string, any>;  // Optional context
}
```

**Response Stream:**

Server sends Server-Sent Events (SSE) with JSON-RPC responses:

```
event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskStatusUpdate","task":{...}}}

event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskArtifactUpdate","taskId":"...","artifact":{...}}}

event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskStatusUpdate","task":{"state":"completed",...}}}
```

**Event Types:**
- `taskStatusUpdate` - Task state changed
- `taskArtifactUpdate` - New artifact or artifact update
- `taskError` - Error occurred

**Characteristics:**
- Keeps connection open until terminal state
- Client can disconnect and reconnect using `tasks/resubscribe`
- Server SHOULD send heartbeats every 15-30 seconds

### tasks/get

Retrieve current task status and artifacts.

**Request:**
```typescript
interface TasksGetRequest {
  taskId: string;               // Task identifier
}
```

**Response:**
```typescript
interface TasksGetResponse {
  task: Task;                   // Current task state and artifacts
}
```

**Usage:**
- Poll for task updates after `message/send`
- Retrieve final results after terminal state
- Check task status at any time

### tasks/list

Enumerate tasks with optional filtering.

**Request:**
```typescript
interface TasksListRequest {
  sessionId?: string;           // Filter by session
  state?: TaskState;            // Filter by state
  limit?: number;               // Max results (default: 100)
  offset?: number;              // Pagination offset
}
```

**Response:**
```typescript
interface TasksListResponse {
  tasks: Task[];                // Task array
  total: number;                // Total matching tasks
}
```

### tasks/cancel

Request task cancellation.

**Request:**
```typescript
interface TasksCancelRequest {
  taskId: string;               // Task to cancel
}
```

**Response:**
```typescript
interface TasksCancelResponse {
  task: Task;                   // Updated task (state: canceled)
}
```

**Behavior:**
- Agent attempts graceful cancellation
- Task transitions to `canceled` state if successful
- May transition to `completed` if already finishing
- Idempotent - multiple cancels safe

### tasks/resubscribe

Resume streaming subscription after disconnection.

**Request:**
```typescript
interface TasksResubscribeRequest {
  taskId: string;               // Task to resubscribe
}
```

**Response Stream:**

Same as `message/stream` - SSE stream with task updates.

**Usage:**
- Reconnect after network interruption
- Resume streaming from current task state
- Server sends current state immediately, then updates

### tasks/pushNotificationConfig/*

Manage webhook configurations for asynchronous notifications.

**tasks/pushNotificationConfig/set:**
```typescript
interface PushNotificationConfigSetRequest {
  url: string;                  // Webhook URL
  events: string[];             // Event types to send
  headers?: Record<string, string>;  // Optional HTTP headers
}
```

**tasks/pushNotificationConfig/get:**
```typescript
interface PushNotificationConfigGetRequest {
  // No parameters
}

interface PushNotificationConfigGetResponse {
  url: string;
  events: string[];
  headers?: Record<string, string>;
}
```

**tasks/pushNotificationConfig/delete:**
```typescript
interface PushNotificationConfigDeleteRequest {
  // No parameters
}
```

**Webhook Payload:**
```typescript
interface WebhookPayload {
  type: "taskStatusUpdate" | "taskArtifactUpdate" | "taskError";
  task?: Task;
  taskId?: string;
  artifact?: Artifact;
  error?: ErrorObject;
  timestamp: number;
}
```

### agent/getAuthenticatedExtendedCard

Retrieve extended Agent Card information requiring authentication.

**Request:**
```typescript
interface GetAuthenticatedExtendedCardRequest {
  // No parameters (uses authentication headers)
}
```

**Response:**
```typescript
interface GetAuthenticatedExtendedCardResponse {
  card: AgentCard;              // Extended card with authenticated data
}
```

**Usage:**
- Retrieve agent information specific to authenticated user
- Access private skills or capabilities
- Get user-specific configuration

## Error Handling

### JSON-RPC Error Codes

**Standard Errors (JSON-RPC 2.0):**
- `-32700` - Parse error (invalid JSON)
- `-32600` - Invalid request (missing required fields)
- `-32601` - Method not found
- `-32602` - Invalid params
- `-32603` - Internal error

**A2A-Specific Errors:**
- `1000` - Task not found
- `1001` - Task already canceled
- `1002` - Task already completed
- `1003` - Invalid task state transition
- `2000` - Authentication required
- `2001` - Authentication failed
- `2002` - Insufficient permissions
- `2003` - Rate limit exceeded
- `3000` - Invalid message format
- `3001` - Unsupported content type
- `3002` - File too large
- `3003` - Skill not available

### HTTP Status Code Mapping (REST Transport)

- `200 OK` - Successful request
- `201 Created` - Task created
- `400 Bad Request` - Invalid request (maps to -32600, 3000-3003)
- `401 Unauthorized` - Authentication required (maps to 2000, 2001)
- `403 Forbidden` - Insufficient permissions (maps to 2002)
- `404 Not Found` - Task/resource not found (maps to 1000, -32601)
- `409 Conflict` - Invalid state transition (maps to 1001-1003)
- `429 Too Many Requests` - Rate limit exceeded (maps to 2003)
- `500 Internal Server Error` - Internal error (maps to -32603)

### Error Object Structure

```typescript
interface ErrorObject {
  code: number;                 // Error code
  message: string;              // Human-readable message
  data?: {
    detail?: string;            // Additional context
    taskId?: string;            // Related task ID
    state?: TaskState;          // Current task state
    [key: string]: any;         // Additional fields
  };
}
```

## Content Negotiation

Agents and clients negotiate content types using MIME types. ([A2A Specification][2])

### Supported MIME Types

**Text Formats:**
- `text/plain` - Plain text
- `text/markdown` - Markdown
- `text/html` - HTML
- `text/csv` - CSV data

**Structured Data:**
- `application/json` - JSON data
- `application/xml` - XML data
- `application/yaml` - YAML data

**Images:**
- `image/png` - PNG images
- `image/jpeg` - JPEG images
- `image/gif` - GIF images
- `image/webp` - WebP images

**Audio:**
- `audio/mpeg` - MP3 audio
- `audio/wav` - WAV audio
- `audio/ogg` - Ogg Vorbis

**Video:**
- `video/mp4` - MP4 video
- `video/webm` - WebM video

**Documents:**
- `application/pdf` - PDF documents
- `application/msword` - Word documents
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` - DOCX

### Content Type Declaration

**In Agent Card:**
```yaml
defaultInputModes: ["text/plain", "application/json", "image/png"]
defaultOutputModes: ["text/plain", "application/json"]
```

**In Message Parts:**
```typescript
{
  type: "text",
  text: "content",
  mimeType: "text/markdown"  // Explicit MIME type
}
```

**Content Type Fallback:**
If agent cannot handle requested input type:
1. Agent MAY attempt conversion to supported type
2. Agent MAY reject task with error code 3001
3. Agent SHOULD indicate supported types in error data

## Extensions

A2A v0.3.0 introduces formal extension support for custom functionality. ([A2A Releases][6])

### Extension Declaration

**In Agent Card:**
```yaml
capabilities:
  extensions: ["com.example.custom-auth", "com.example.advanced-streaming"]
```

### Extension Namespacing

Extensions MUST use reverse domain notation:
- `com.example.feature-name` - Vendor-specific
- `org.a2aproject.experimental-feature` - Official experimental

### Extension Discovery

Clients discover extensions via Agent Card `capabilities.extensions` array. Clients SHOULD ignore unknown extensions.

## Protocol Versioning

### Version Format

`MAJOR.MINOR.PATCH` (Semantic Versioning)

**Current Version:** 0.3.0 ([A2A Releases][6])

### Compatibility Guarantees

Starting with v0.3.0, the protocol maintains backward compatibility: ([A2A Roadmap][5])
- **PATCH** - Bug fixes, no breaking changes
- **MINOR** - New features, backward compatible
- **MAJOR** - Breaking changes, migration required

### Version Negotiation

1. Client reads `protocolVersion` from Agent Card
2. Client verifies version compatibility
3. Client uses highest compatible version
4. Client MUST support version from Agent Card or fail

**Version String Comparison:**
- `0.3.0` and `0.3.1` - Compatible (patch)
- `0.3.0` and `0.4.0` - Compatible (minor)
- `0.3.0` and `1.0.0` - Incompatible (major)

## Transport-Specific Requirements

### HTTPS Requirements

All transports MUST use HTTPS in production with the following requirements: ([A2A Specification][2])
- TLS 1.3 or higher RECOMMENDED
- TLS 1.2 acceptable with strong cipher suites
- Certificate validation against trusted CA
- Hostname verification required
- HTTP connections ONLY for local development

### Server-Sent Events (SSE)

For streaming (`message/stream`, `tasks/resubscribe`):
- Content-Type: `text/event-stream`
- Event format: `event: message\ndata: {json}\n\n`
- Heartbeat: Server SHOULD send comment every 15-30 seconds
- Reconnection: Client uses `Last-Event-ID` header (optional)

**Example SSE Stream:**
```
: heartbeat

event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskStatusUpdate","task":{"taskId":"abc","state":"running"}}}

: heartbeat

event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskArtifactUpdate","taskId":"abc","artifact":{"artifactId":"art1","parts":[{"type":"text","text":"Result"}]}}}

event: message
data: {"jsonrpc":"2.0","id":"1","result":{"type":"taskStatusUpdate","task":{"taskId":"abc","state":"completed"}}}
```

### gRPC-Specific

- HTTP/2 transport required
- Protobuf message serialization
- Standard gRPC status codes
- Metadata for authentication headers
- Bidirectional streaming for `message/stream`

## Implementation Requirements

### Minimum Agent Compliance

An A2A-compliant agent MUST:
1. Implement at least ONE transport (JSON-RPC, gRPC, or REST)
2. Support `message/send` and `tasks/get` methods
3. Publish valid Agent Card at `/.well-known/agent-card.json`
4. Enforce HTTPS in production
5. Authenticate all requests per declared security schemes
6. Return valid task objects with required fields
7. Implement at least one terminal state (`completed`, `failed`, `rejected`)

### Minimum Client Compliance

An A2A-compliant client MUST:
1. Support at least ONE transport
2. Fetch and parse Agent Card from well-known URI
3. Discover and implement authentication requirements
4. Handle task lifecycle states correctly
5. Parse message and artifact structures
6. Implement error handling for all error codes

### Recommended Features

Implementations SHOULD:
- Support multiple transports with fallback
- Implement streaming (`message/stream`)
- Support webhook notifications for async workflows
- Provide state transition history
- Implement connection retry with exponential backoff
- Include distributed tracing headers (W3C Trace Context)
- Log all requests for audit purposes

## References

[1]: https://a2a-protocol.org/ "A2A Protocol Official Site"
[2]: https://a2a-protocol.org/latest/specification/ "A2A Protocol Specification"
[3]: https://github.com/a2aproject/A2A "A2A GitHub Repository"
[4]: https://github.com/a2aproject/A2A/tree/main/specification "A2A Protocol Specification Files"
[5]: https://a2a-protocol.org/latest/roadmap/ "A2A Roadmap"
[6]: https://github.com/a2aproject/A2A/releases "A2A Release Notes"
