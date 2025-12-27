---
title: "AI and Agent References"
description: "Reference documentation for AI models, agent protocols, and agentic AI systems"
type: "meta"
tags: ["ai", "agents", "protocols", "reference-index"]
category: "ai"
subcategory: "none"
version: "1.0"
last_updated: "2025-08-16"
status: "stable"
sources: []
related: []
author: "unknown"
contributors: []
---

# AI and Agent References

Reference documentation covering AI models, agent communication protocols, multi-agent systems, and agentic AI implementations.

## Agent Protocols

### A2A (Agent2Agent Protocol)

The A2A Protocol enables AI agents to communicate and collaborate across different platforms and frameworks.

**Documentation:**
- [**A2A Protocol Overview**](a2a/overview.md) - Conceptual introduction, core concepts, design principles, and use cases
- [**A2A Protocol Specification**](a2a/specification.md) - Complete technical specification including transport protocols, Agent Card schema, task lifecycle, and message formats
- [**A2A Security and Implementation Guide**](a2a/security-implementation.md) - Security best practices, authentication patterns, implementation workflows, and enterprise deployment

**Key Topics:**
- Multi-agent communication and collaboration
- Opaque agent communication (no internal state exposure)
- Agent Cards for capability discovery
- Task lifecycle management (long-running, multi-turn, asynchronous)
- Three transport options: JSON-RPC, gRPC, REST
- Enterprise security: OAuth2, OIDC, mTLS authentication
- Streaming execution with Server-Sent Events
- Webhook notifications for asynchronous workflows

**Version:** 0.3.0 (stable)
**Status:** Production-ready, maintained by Linux Foundation
**License:** Apache 2.0

**Quick Links:**
- Official Site: https://a2a-protocol.org/
- GitHub: https://github.com/a2aproject/A2A
- Samples: https://github.com/a2aproject/a2a-samples

---

## Related Topics

### MCP (Model Context Protocol)

While A2A handles agent-to-agent communication (horizontal integration), MCP handles agent-to-resource communication (vertical integration):
- **MCP**: How a single agent connects to tools, APIs, and data sources
- **A2A**: How different agents communicate and collaborate

Both protocols work together to enable comprehensive agent ecosystems.

---

## Contributing

To add new AI/agent reference documentation:

1. Create appropriate subdirectory under `ai/` (e.g., `ai/protocol-name/`)
2. Follow the [Reference Template](../REFERENCE-TEMPLATE.md)
3. Include all required metadata fields per [Metadata Spec](../METADATA-SPEC.md)
4. Use inline citations heavily for human verification
5. Update this README with links to new documentation

---

## Tags

Common tags for AI/agent references:
- `protocol` - Communication protocols
- `agent-communication` - Agent interaction patterns
- `multi-agent` - Multi-agent systems
- `interoperability` - Cross-platform compatibility
- `authentication` - Security and auth patterns
- `streaming` - Real-time data streaming
- `task-management` - Task lifecycle and orchestration
- `agentic-ai` - Agentic AI systems
- `llm` - Large language models
- `model-spec` - Model specifications
