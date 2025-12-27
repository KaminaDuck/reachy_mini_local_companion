---
title: "A2A Protocol Overview"
description: "Conceptual introduction to the Agent2Agent (A2A) Protocol for multi-agent communication"
type: "concept-guide"
tags: ["protocol", "agent-communication", "multi-agent", "interoperability", "architecture", "design-principles", "agentic-ai"]
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
  - name: "Google Developer Blog - A2A Announcement"
    url: "https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/"
  - name: "A2A Roadmap"
    url: "https://a2a-protocol.org/latest/roadmap/"
  - name: "A2A Sample Implementations"
    url: "https://github.com/a2aproject/a2a-samples"
related: ["specification.md", "security-implementation.md"]
author: "unknown"
contributors: []
---

# A2A Protocol Overview

Conceptual introduction to the Agent2Agent (A2A) Protocol, an open standard for enabling AI agents to communicate and collaborate across different platforms and frameworks.

## What is A2A?

The Agent2Agent (A2A) Protocol is an open standard that enables AI agents built on diverse frameworks to discover each other, negotiate interaction modalities, securely collaborate on long-running tasks, and operate without exposing internal state, memory, or tools. ([A2A Protocol Site][1])

A2A aims to "maximize the benefits of agentic AI by enabling true multi-agent scenarios" where agents can work together regardless of their underlying implementation. ([A2A Announcement][4]) Originally developed by Google LLC, the protocol is now governed by the Linux Foundation and licensed under Apache License 2.0. ([A2A GitHub][3])

### Key Characteristics

**Open Standard:**
- Freely available specification
- Open source implementations
- Community-driven development
- Apache 2.0 license ([A2A GitHub][3])

**Platform Agnostic:**
- Works across different agent frameworks (LangGraph, CrewAI, Semantic Kernel, ADK)
- Transport flexibility (JSON-RPC, gRPC, REST)
- No vendor lock-in

**Enterprise Ready:**
- Built-in authentication and authorization
- Distributed tracing and audit logging
- Rate limiting and security features
- Production deployment patterns

## Core Concepts

### Opaque Agent Communication

A2A provides **opaque communication** where agents collaborate via declared capabilities and exchanged messages without exposing internal implementation details. ([A2A Specification][2])

**What Agents Share:**
- Declared capabilities (Agent Card)
- Message content and context
- Task status and artifacts
- Authentication requirements

**What Agents Keep Private:**
- Internal state and memory
- Tool implementations
- Prompts and reasoning processes
- Backend infrastructure

This opacity enables:
- Security and privacy preservation
- Implementation flexibility
- Framework independence
- Evolutionary upgrades without breaking changes

### Agent Cards

Every A2A agent publishes an **Agent Card** at `/.well-known/agent-card.json` describing its identity, capabilities, endpoints, and authentication requirements. ([A2A Specification][2])

Think of an Agent Card as an agent's "business card" that answers:
- Who am I? (name, description, version)
- How do you reach me? (URL, transport protocols)
- What can I do? (skills, input/output modes)
- How do you authenticate? (security schemes)

Agent Cards enable **capability discovery** - clients can programmatically discover what an agent offers before attempting interaction.

### Tasks

A **task** is a stateful unit of work with a unique ID and defined lifecycle. ([A2A Specification][2])

**Task Lifecycle:**
```
queued → running → streaming-response → completed
                ↓
          input-required → running
                ↓
          auth-required → running
```

Tasks support:
- **Long-running operations** (hours or days)
- **Multi-turn interactions** (back-and-forth with `input-required` state)
- **Asynchronous execution** (fire-and-forget with webhooks)
- **State tracking** (query task status at any time)

### Messages and Artifacts

**Messages** are communication turns containing role (user/agent) and content parts (text, files, structured data). ([A2A Specification][2])

**Artifacts** are agent-generated outputs composed of multiple parts. An agent might produce multiple artifacts during task execution.

**Example Flow:**
1. Client sends message: "Analyze this document" (with file attachment)
2. Agent creates task in `running` state
3. Agent generates artifact with analysis results
4. Task transitions to `completed` state
5. Client retrieves final artifacts

## Four Communication Phases

A2A structures agent interaction into four phases: ([A2A Specification][2])

### 1. Capability Discovery

Agents advertise capabilities via JSON-formatted Agent Cards:

```json
{
  "name": "Research Agent",
  "skills": [
    {"name": "web-search", "description": "Search web content"},
    {"name": "document-analysis", "description": "Analyze documents"}
  ],
  "defaultInputModes": ["text/plain", "application/pdf"],
  "defaultOutputModes": ["text/plain", "application/json"]
}
```

Clients discover what an agent can do before making requests.

### 2. Task Management

Communication is oriented toward task completion with defined lifecycles:
- Create task via `message/send` or `message/stream`
- Monitor progress via `tasks/get` or streaming events
- Cancel incomplete tasks via `tasks/cancel`
- Retrieve results from completed tasks

### 3. Collaboration

Agents exchange context, replies, artifacts, and user instructions:
- Multi-turn conversations (input-required state)
- File exchange (upload and download)
- Structured data transfer
- External authentication (auth-required state)

### 4. User Experience

Messages include content-type parts enabling format negotiation:
- Text (plain, markdown, HTML)
- Images (PNG, JPEG, WebP)
- Audio (MP3, WAV, Ogg)
- Video (MP4, WebM)
- Documents (PDF, Word)
- Structured data (JSON, XML, YAML)

Agents and clients negotiate supported formats via Agent Card declarations.

## Design Principles

### Built on Open Standards

A2A leverages existing protocols rather than inventing new ones: ([A2A Specification][2])
- **HTTP/HTTPS** - Universal transport layer
- **JSON-RPC 2.0** - Lightweight RPC protocol
- **gRPC** - High-performance binary protocol
- **REST** - Familiar HTTP+JSON patterns
- **Server-Sent Events** - Standard streaming mechanism
- **OpenAPI Security Schemes** - Industry-standard authentication
- **RFC 8615** - Well-known URIs (`.well-known/agent-card.json`)

This approach provides:
- Existing tooling and libraries
- Familiar developer experience
- Battle-tested security patterns
- Wide platform support

### Security by Default

Authentication is mandatory - every request must be authenticated per agent's declared security schemes. ([A2A Specification][2])

**Supported Authentication:**
- OAuth 2.0 and OpenID Connect
- API Keys
- HTTP Bearer tokens (JWT)
- Mutual TLS (mTLS)
- HTTP Basic Auth

**Security Features:**
- HTTPS mandatory in production
- Granular authorization (per-skill OAuth scopes)
- Audit logging (taskId, sessionId, correlation IDs)
- Distributed tracing (W3C Trace Context)
- Rate limiting and DDoS protection

### Multi-Modal Support

A2A handles diverse content types beyond just text: ([A2A Specification][2])
- Text in multiple formats (plain, markdown, HTML)
- Binary files (images, audio, video, documents)
- Structured data (JSON, XML, YAML)
- Custom MIME types via extensions

Agents declare supported input and output modes in their Agent Card, enabling automatic format negotiation.

### Long-Running Task Handling

Unlike synchronous APIs with tight timeouts, A2A supports tasks that take hours or days: ([A2A Specification][2])

**Asynchronous Execution:**
- Client submits task and receives task ID
- Client disconnects
- Agent processes in background
- Agent sends webhook notification on completion
- Client retrieves results later

**Streaming Execution:**
- Client opens streaming connection
- Agent sends incremental updates
- Client displays progress in real-time
- Connection can be resumed if interrupted (`tasks/resubscribe`)

## Relationship with MCP

A2A and MCP (Model Context Protocol) are complementary protocols that work together: ([A2A Announcement][4])

### MCP: Vertical Integration

**MCP** defines how a **single agent** connects to tools, APIs, data sources, and resources.

**Use Case:** An agent needs to access a database, call a REST API, or use a file system.

**Direction:** Agent → Tools/Resources (vertical)

### A2A: Horizontal Integration

**A2A** defines how **different agents** communicate and collaborate with each other.

**Use Case:** Multiple specialized agents coordinate on a complex task requiring diverse expertise.

**Direction:** Agent ↔ Agent (horizontal)

### Working Together

An agent in an A2A collaboration may use MCP connections to fetch data or execute tools needed for its assigned task:

```
┌─────────┐                    ┌─────────┐
│ Agent A │◄─────A2A──────────►│ Agent B │
└────┬────┘                    └────┬────┘
     │                              │
     │ MCP                          │ MCP
     ▼                              ▼
┌─────────┐                    ┌─────────┐
│ Tools/  │                    │ Tools/  │
│ Resources│                    │ Resources│
└─────────┘                    └─────────┘
```

**Example Scenario (Auto Repair Shop):**
- **MCP**: Connects agents to structured tools (inventory systems, diagnostic APIs, scheduling databases)
- **A2A**: Enables ongoing communication between service advisor agent, technician agent, and parts agent

Both protocols are open standards promoting interoperability in the agentic AI ecosystem.

## Common Use Cases

### Multi-Agent Task Delegation

A coordinator agent distributes subtasks to specialized agents:

**Scenario:** Research project requiring web search, document analysis, and data visualization
1. Coordinator agent receives user request
2. Coordinator discovers available specialist agents via Agent Cards
3. Coordinator delegates subtasks via A2A messages
4. Specialist agents execute tasks and return artifacts
5. Coordinator synthesizes results and returns to user

### Long-Running Research Operations

Complex research taking hours or days:

**Scenario:** Comprehensive market analysis
1. Client submits analysis request via `message/send`
2. Agent begins work, task enters `running` state
3. Client disconnects, sets up webhook for notifications
4. Agent works for several hours, generating intermediate artifacts
5. Agent completes analysis, sends webhook notification
6. Client retrieves final report

### Cross-Platform Agent Collaboration

Agents built with different frameworks working together:

**Scenario:** LangGraph agent coordinating with CrewAI agent
1. LangGraph agent publishes A2A Agent Card
2. CrewAI agent publishes A2A Agent Card
3. Both agents discover each other's capabilities
4. Agents exchange messages via A2A protocol
5. Internal implementations remain private and independent

### Human-in-the-Loop Workflows

Tasks requiring user approval or additional input:

**Scenario:** Expense approval workflow
1. Agent processes expense report
2. Agent transitions task to `input-required` state with approval request
3. Client notifies user and awaits decision
4. User provides approval or rejection
5. Client sends additional message to agent
6. Agent resumes processing based on user input

### Asynchronous Batch Processing

Large-scale operations with webhook notifications:

**Scenario:** Bulk document processing
1. Client configures webhook URL via `tasks/pushNotificationConfig/set`
2. Client submits 1000 documents for processing
3. Client disconnects after receiving task IDs
4. Agent processes documents in background
5. Agent sends webhook POST for each completed task
6. Client retrieves artifacts when notified

## Transport Options

A2A provides three transport protocols, allowing implementations to choose based on requirements: ([A2A Specification][2])

### JSON-RPC 2.0 (Primary)

**Best For:** General-purpose agent communication, web clients, straightforward integrations

**Characteristics:**
- Lightweight JSON format
- Simple request/response pattern
- Streaming via Server-Sent Events
- Widely supported tooling

**When to Use:**
- Building web-based agent interfaces
- Rapid prototyping
- Language-agnostic clients
- Human-readable debugging

### gRPC

**Best For:** High-performance scenarios, microservices architectures, strong typing

**Characteristics:**
- Protocol Buffers serialization (efficient binary format)
- HTTP/2 multiplexing
- Bidirectional streaming
- Strong schema validation

**When to Use:**
- High-throughput requirements
- Low-latency communication
- Polyglot microservices
- Strongly-typed contracts

### REST (HTTP+JSON)

**Best For:** Traditional web applications, curl/Postman testing, REST-centric architectures

**Characteristics:**
- Standard HTTP verbs (GET, POST, DELETE)
- Familiar URL patterns
- Stateless operations
- Easy manual testing

**When to Use:**
- Existing REST infrastructure
- Simple CRUD-style operations
- Manual API exploration
- Minimal client dependencies

**Transport Negotiation:**
Agents declare `preferredTransport` and `additionalInterfaces` in Agent Card. Clients choose compatible transport or fall back to alternatives.

## Implementation Options

### Official SDKs

**Python:**
```bash
pip install a2a-sdk
```

**JavaScript/TypeScript:**
```bash
npm install @a2a-js/sdk
```

**Java:** Maven distribution

**.NET:** NuGet package (`dotnet add package A2A`)

**Go:** In development

([A2A Samples][6])

### Framework Integration

A2A works with existing agent frameworks:
- **LangGraph** - LangChain's agent orchestration framework
- **CrewAI** - Multi-agent collaboration framework
- **Semantic Kernel** - Microsoft's agent framework
- **ADK (Agent Development Kit)** - Google's agent framework

Agents built with these frameworks can expose A2A endpoints to enable cross-framework collaboration.

### Sample Implementations

The A2A project provides sample code demonstrating:
- Basic client/server implementations
- Streaming execution patterns
- Multi-turn interactions
- Webhook configuration
- Authentication integration
- Framework-specific examples

Available at: https://github.com/a2aproject/a2a-samples ([A2A Samples][6])

## Protocol Versioning and Stability

**Current Version:** 0.3.0 (Released July 2025) ([A2A GitHub][3])

**Stability Commitment:**
Version 0.3.0 is the first **stable release** with backward compatibility guarantees: ([A2A Roadmap][5])
- **Patch versions** (0.3.x) - Bug fixes only, fully compatible
- **Minor versions** (0.x.0) - New features, backward compatible
- **Major versions** (x.0.0) - Breaking changes, migration required

**Version History:**
- 9 releases total
- 423 commits
- 120 contributors
- 20.5k GitHub stars, 2.1k forks

**Breaking Changes in v0.3.0:**
- Agent Card path changed: `/.well-known/agent.json` → `/.well-known/agent-card.json`
- Python SDK field naming: camelCase → snake_case

**New Features in v0.3.0:**
- Signed Agent Cards (JWS signatures for integrity verification)
- Extensions support with SDK implementation
- Enhanced client SDK capabilities
- gRPC transport finalization

## Community and Governance

### Linux Foundation Stewardship

A2A is governed by the Linux Foundation with a Technical Steering Committee (TSC) overseeing development. ([A2A GitHub][3])

**Governance Model:**
- Community-led development
- Transparent decision-making
- Standardized contribution processes
- Dedicated working groups

### Partner Ecosystem

50+ technology companies support A2A: ([A2A Announcement][4])
- **Collaboration:** Atlassian, Slack, Zoom
- **Enterprise:** Salesforce, ServiceNow, SAP, Workday, UKG
- **Development:** MongoDB, Cohere, Langchain
- **Financial:** Intuit, PayPal, Box

### Contributing

**Ways to Contribute:**
- Report bugs and request features (GitHub Issues)
- Submit pull requests (code, documentation, samples)
- Participate in discussions (GitHub Discussions)
- Propose protocol enhancements (via RFC process)

**Resources:**
- Contributing Guide: https://github.com/a2aproject/A2A/blob/main/CONTRIBUTING.md
- Governance: https://github.com/a2aproject/A2A/blob/main/GOVERNANCE.md

## Roadmap and Future Development

### Near-Term (v0.3 Focus)

Completed in v0.3.0: ([A2A Roadmap][5])
- ✅ Signed Agent Cards for content integrity
- ✅ Extensions solidification across SDKs
- ✅ Enhanced client-side SDK improvements
- ✅ gRPC transport support

### Medium-Term (3-6 Months)

**Agent Registry:**
- Centralized discovery mechanism
- Agent search and filtering
- Capability matching
- Version compatibility checking

**Tooling:**
- A2A Inspector (protocol debugging tool)
- TCK (Technology Compatibility Kit) for validation
- Performance benchmarking suite

**Documentation:**
- Community best practices
- Architecture patterns
- Security guidelines
- Migration guides

**SDK Expansion:**
- Complete Go SDK
- Additional language support
- Framework-specific helpers

### Longer-Term Plans

**Dynamic Skill Querying:**
- Runtime skill discovery
- Conditional capability advertising
- Context-aware skill availability

**Mid-Task UX Negotiation:**
- Dynamic format switching
- Adaptive content types
- Real-time preference updates

**Enhanced Authorization:**
- Credential provisioning in Agent Cards
- Token acquisition flows
- Federated identity integration

**Reliability Enhancements:**
- Circuit breakers
- Automatic retry policies
- Failover mechanisms
- Health checking

## Getting Started

### 1. Understand the Concepts

Read this overview and the technical specification to understand:
- Agent Cards and capability discovery
- Task lifecycle and state transitions
- Message and artifact structures
- Transport options and trade-offs

### 2. Choose Your Transport

Select transport based on requirements:
- **JSON-RPC** - General purpose, web-friendly
- **gRPC** - High performance, type-safe
- **REST** - Traditional, easy testing

### 3. Install SDK

```bash
# Python
pip install a2a-sdk

# JavaScript
npm install @a2a-js/sdk

# Java (Maven)
<dependency>
  <groupId>org.a2aproject</groupId>
  <artifactId>a2a-sdk</artifactId>
</dependency>

# .NET
dotnet add package A2A
```

### 4. Explore Samples

Clone and run sample implementations:
```bash
git clone https://github.com/a2aproject/a2a-samples
cd a2a-samples
# Follow language-specific README
```

### 5. Build Your Agent

1. Define capabilities in Agent Card
2. Implement authentication requirements
3. Handle `message/send` and `tasks/get` methods
4. Add streaming support (`message/stream`)
5. Test with A2A Inspector tool

### 6. Integrate with Existing Systems

- Wrap existing services with A2A endpoints
- Expose agent capabilities via Agent Card
- Implement authentication integration
- Add distributed tracing headers

## Comparison with Other Protocols

### A2A vs HTTP APIs

**Traditional HTTP API:**
- Custom per-service contracts
- Ad-hoc authentication patterns
- Limited standardization
- Tight coupling to implementation

**A2A:**
- Standardized message format
- Consistent authentication (OpenAPI schemes)
- Agent Card capability discovery
- Opaque implementation isolation

### A2A vs MCP

**MCP (Model Context Protocol):**
- Agent-to-resource communication
- Tool and data source integration
- Single agent scope
- Vertical integration

**A2A (Agent2Agent Protocol):**
- Agent-to-agent communication
- Multi-agent coordination
- Distributed agent ecosystems
- Horizontal integration

**Together:** MCP connects agents to resources; A2A connects agents to each other.

### A2A vs Custom Agent Protocols

**Custom Protocols:**
- Framework-specific (LangGraph, CrewAI, etc.)
- Vendor lock-in
- No cross-framework collaboration
- Limited tooling

**A2A:**
- Framework-agnostic
- Vendor-neutral
- Cross-platform collaboration
- Standardized tooling and SDKs

## Key Takeaways

1. **A2A enables multi-agent collaboration** across different platforms and frameworks through a standardized protocol

2. **Opaque communication** allows agents to work together without exposing internal implementation details

3. **Agent Cards provide capability discovery** - clients can programmatically determine what agents offer

4. **Tasks support long-running operations** with state management, multi-turn interactions, and asynchronous execution

5. **Three transport options** (JSON-RPC, gRPC, REST) provide flexibility for different use cases

6. **Security is mandatory** - every request must be authenticated using industry-standard schemes

7. **Complementary to MCP** - A2A handles agent-to-agent (horizontal) while MCP handles agent-to-resource (vertical)

8. **Enterprise-ready** with authentication, authorization, tracing, audit logging, and production deployment patterns

9. **Open source and community-driven** under Linux Foundation governance with 50+ partner organizations

10. **Version 0.3.0 is stable** with backward compatibility commitments and long-term support

## References

[1]: https://a2a-protocol.org/ "A2A Protocol Official Site"
[2]: https://a2a-protocol.org/latest/specification/ "A2A Protocol Specification"
[3]: https://github.com/a2aproject/A2A "A2A GitHub Repository"
[4]: https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ "Google Developer Blog - A2A Announcement"
[5]: https://a2a-protocol.org/latest/roadmap/ "A2A Roadmap"
[6]: https://github.com/a2aproject/a2a-samples "A2A Sample Implementations"
