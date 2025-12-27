---
title: "Claude Code MCP Integration Reference"
description: "Comprehensive guide to Model Context Protocol integration with Claude Code"
type: "integration-guide"
tags: ["claude-code", "mcp", "model-context-protocol", "integration", "tools", "servers", "configuration"]
category: "claude"
subcategory: "integration"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Claude Code MCP Documentation"
    url: "https://anthropic.mintlify.app/en/docs/claude-code/mcp"
  - name: "Model Context Protocol Specification"
    url: "https://modelcontextprotocol.io/specification/2025-06-18"
  - name: "Anthropic MCP Announcement"
    url: "https://www.anthropic.com/news/model-context-protocol"
  - name: "Claude Code Tips - MCP Servers"
    url: "https://cloudartisan.com/posts/2025-04-12-adding-mcp-servers-claude-code/"
  - name: "Top 10 MCP Servers for Claude Code"
    url: "https://apidog.com/blog/top-10-mcp-servers-for-claude-code/"
related: ["slash-commands.md"]
author: "unknown"
contributors: []
---

# Claude Code MCP Integration Reference

The Model Context Protocol (MCP) is an open-source standard enabling AI tools to connect with external services. Claude Code integrates hundreds of tools and data sources through MCP servers, granting access to databases, APIs, and specialized services. ([Claude Code MCP Docs][1], [MCP Announcement][3])

## Overview

### What is MCP?

MCP is an open protocol that enables seamless integration between LLM applications and external data sources and tools. ([MCP Specification][2]) It was introduced by Anthropic in November 2024 to standardize how AI systems like large language models integrate and share data with external tools, systems, and data sources. ([MCP Announcement][3])

**Core Problem**: Advanced AI models often remain isolated from crucial business data trapped in information silos and legacy systems. MCP addresses this by providing a unified protocol approach, replacing fragmented custom integrations. ([MCP Announcement][3])

### Architecture

MCP operates as a **JSON-RPC 2.0 message-based protocol** establishing stateful connections between three primary components: ([MCP Specification][2])

- **Hosts**: LLM applications (like Claude Code) initiating connections
- **Clients**: Connectors within host applications
- **Servers**: Services delivering context and capabilities

The protocol draws design inspiration from the Language Server Protocol (LSP), applying similar standardization principles to AI application integrations. ([MCP Specification][2])

## Core Capabilities

With MCP servers connected, Claude Code can: ([Claude Code MCP Docs][1])

**Implement features from tracking systems**: Extract requirements from issue trackers and create pull requests directly.

**Analyze operational data**: Query monitoring platforms for error patterns and performance metrics.

**Database operations**: Execute natural language queries against connected data sources.

**Design integration**: Incorporate external design files into development workflows.

**Workflow automation**: Generate communications and manage cross-platform tasks.

## Server Capabilities

MCP servers can expose three primary feature categories: ([MCP Specification][2])

### Resources
Contextual information and data accessible to users or AI models. Resources are referenced using `@` mentions:

```
@github:issue://123
@docs:file://api/authentication
```

### Prompts
Pre-templated messages and workflow structures that become available as slash commands:

```
/mcp__github__list_prs
/mcp__jira__create_issue "Bug description" priority
```

### Tools
Executable functions for AI model invocation. MCP servers are designed for natural language queries rather than explicit tool calls - you describe what you need rather than calling specific functions. ([Cloud Artisan MCP Tips][4])

## Client Capabilities

Clients (like Claude Code) may offer servers: ([MCP Specification][2])

**Sampling**: Server-initiated agentic behaviors enabling recursive LLM interactions.

**Roots**: Server-initiated exploration of URI or filesystem boundaries.

**Elicitation**: Server-initiated requests for user-provided information.

## Installation and Configuration

### Transport Protocols

Claude Code supports three transport protocols: ([Claude Code MCP Docs][1])

#### HTTP Servers (Recommended)
Cloud-based services use HTTP transport for remote connections. This is the most widely supported transport for cloud-based services. ([Claude Code MCP Docs][1])

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

#### SSE Servers (Deprecated)
Legacy server-sent events option:

```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

#### Stdio Servers (Local)
Local processes requiring system access. Python servers use `uvx`, while Node.js servers use `npx`. ([Cloud Artisan MCP Tips][4])

```bash
# Python server example
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY -- npx -y airtable-mcp-server

# With timezone configuration
claude mcp add-json server-time --scope user '{
  "command": "uvx",
  "args": ["mcp-server-time", "--local-timezone", "Australia/Sydney"]
}'
```

**Important**: The `--` separator distinguishes Claude CLI flags from server command arguments. ([Claude Code MCP Docs][1])

### Configuration Scopes

MCP servers operate at three levels: ([Claude Code MCP Docs][1], [Cloud Artisan MCP Tips][4])

| Scope | Storage | Use Case |
|-------|---------|----------|
| **Local** | User settings (temporary) | Single session, testing |
| **Project** | `.mcp.json` file | Team collaboration, version control |
| **User** | User settings (default) | Cross-project utilities, personal tools |

**Project scope** enables team sharing through version control. For example, you can add Puppeteer and Sentry servers to your `.mcp.json`, so that every engineer working on your repo can use these out of the box. ([Top 10 MCP Servers][5])

**User scope** is recommended for tools you'll reuse regularly across projects, as it reduces duplication and ensures consistent availability. ([Cloud Artisan MCP Tips][4])

### Prerequisites

Install required package managers: ([Cloud Artisan MCP Tips][4])

```bash
brew install uv      # Python package manager
brew install node    # Node.js runtime
```

### Example Configuration

Create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${POSTGRES_CONNECTION_STRING}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    }
  }
}
```

## Popular MCP Servers

### Project Management
- **Asana** - Task and project management
- **Jira** - Issue tracking and agile workflows
- **Linear** - Modern issue tracking
- **Monday** - Work operating system
- **Notion** - Collaborative workspace

### Development Tools
- **GitHub** - Repository management, issues, PRs, CI/CD workflows ([Top 10 MCP Servers][5])
- **Sentry** - Error monitoring and debugging
- **Socket** - Dependency security scanning

### Databases
- **PostgreSQL** - Relational database queries
- **HubSpot** - CRM and customer data
- **Airtable** - Collaborative database platform
- **Daloopa** - Financial data platform

### Infrastructure & Deployment
- **Vercel** - Serverless deployment platform
- **Netlify** - Web application hosting
- **Cloudflare** - CDN and security services
- **AWS** - Comprehensive access to Amazon Web Services (CDK, CloudFormation, Bedrock, Rekognition) ([Top 10 MCP Servers][5])

### Design & Creative
- **Figma** - Design collaboration
- **Canva** - Graphic design platform

### Payments
- **Stripe** - Payment processing
- **PayPal** - Payment gateway
- **Square** - Point-of-sale and payments

### Browser Automation
- **Puppeteer** - Browser screenshots and web automation ([Top 10 MCP Servers][5])

## Authentication

### OAuth 2.0

OAuth 2.0 authentication is supported for cloud services. Within Claude Code, use `/mcp` to authenticate and manage tokens. Authentication tokens are stored securely and refreshed automatically. ([Claude Code MCP Docs][1])

### API Keys

For servers requiring API keys, use environment variables:

```bash
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

**Security best practice**: Use tokens with the minimum necessary permissions and set expiration dates. Never commit credentials to repositories or share them publicly. ([Cloud Artisan MCP Tips][4])

## Management Commands

### CLI Commands

```bash
# List all configured servers
claude mcp list

# Get details for specific server
claude mcp get <name>

# Remove server configuration
claude mcp remove <name>

# Reset approval decisions
claude mcp reset-project-choices
```

### In-Session Commands

Within Claude Code, use `/mcp` to:
- Check server status
- Manage authentication
- Verify connections

## Verification and Debugging

### Verify Installation

Three approaches to verify MCP server setup: ([Cloud Artisan MCP Tips][4])

1. **List all servers**:
   ```bash
   claude mcp list
   ```

2. **Check connection status**:
   ```bash
   claude --mcp-debug
   # Then run /mcp command
   ```

3. **Test naturally**: Ask Claude questions requiring specific server functionality

### Debug Mode

Launch Claude with debugging enabled to identify configuration issues: ([Top 10 MCP Servers][5])

```bash
claude --mcp-debug
```

### Common Issues

**Language mismatch**: Python servers require `uvx`, Node.js servers require `npx`. Mixing these up causes failures. ([Cloud Artisan MCP Tips][4])

**Scope confusion**: Ensure you understand the difference between local (temporary), user (persistent), and project (shareable) scopes.

**Permission errors**: When setting up filesystem access, explicitly define allowed directories rather than granting blanket access. ([Cloud Artisan MCP Tips][4])

## Security Considerations

### Risk Awareness

**Important warning**: "Use third party MCP servers at your own risk - Anthropic has not verified the correctness or security of all these servers." ([Claude Code MCP Docs][1], [Top 10 MCP Servers][5])

### Security Best Practices

**Verify server trustworthiness** before installation. Review server source code and maintainer reputation.

**Be cautious with servers fetching untrusted content**, as these can expose you to prompt injection risk. ([Claude Code MCP Docs][1], [Top 10 MCP Servers][5])

**Store sensitive credentials** using environment variables, never hardcode them in configuration files.

**Review `.mcp.json`** before committing to version control to ensure no secrets are included.

**User consent**: Users must explicitly consent to and understand all data access and operations. ([MCP Specification][2])

**Minimum permissions**: Grant only the minimum necessary permissions to MCP servers.

## Advanced Features

### Output Management

Configure MCP output limits with environment variables: ([Claude Code MCP Docs][1])

```bash
export MAX_MCP_OUTPUT_TOKENS=50000
```

- Default warning threshold: 10,000 tokens
- Default maximum: 25,000 tokens

### Resource References

MCP servers expose resources accessible via `@` mentions: ([Claude Code MCP Docs][1])

```
@github:issue://123
@docs:file://api/authentication
@notion:page://product-roadmap
```

### Slash Commands from Prompts

MCP prompts become available as slash commands using the pattern: ([Claude Code MCP Docs][1])

```
/mcp__<server-name>__<prompt-name> [arguments]
```

Examples:
```
/mcp__github__list_prs
/mcp__jira__create_issue "Fix authentication bug" high
/mcp__notion__search "Q1 roadmap"
```

### Context Window Optimization

**Important consideration**: Each enabled MCP server adds tool definitions to Claude's system prompt, consuming part of your context window even when not actively used. ([Top 10 MCP Servers][5])

**Best practice**: Only enable MCP servers you actively need to maximize available context for your code and conversation.

## Enterprise Configuration

Organizations can deploy centralized MCP configurations through administrator-controlled files. ([Claude Code MCP Docs][1])

### Enterprise Features

**Server allowlists**: Specify permitted MCP servers organization-wide.

**Server denylists**: Block specific servers for security or compliance.

**Enterprise-managed servers**: Pre-configured organization servers with standardized credentials.

### Configuration Locations

Platform-specific directories for enterprise configuration: ([Claude Code MCP Docs][1])

- **macOS**: `/Library/Application Support/ClaudeCode/`
- **Windows**: `C:\ProgramData\ClaudeCode\`
- **Linux**: `/etc/claude-code/`

## Best Practices

### Team Collaboration

**Share project configurations**: Add commonly-used servers to `.mcp.json` and commit to version control, making them available to all team members. ([Top 10 MCP Servers][5])

**Document server purposes**: Include comments or a README explaining why each server is configured and what it's used for.

**Standardize credentials management**: Use consistent environment variable naming across the team.

### Development Workflow

**Combine with slash commands**: Create custom slash commands that leverage MCP servers for repeated workflows. ([Top 10 MCP Servers][5])

Example in `.claude/commands/create-issue.md`:
```markdown
---
description: Create GitHub issue from current context
---

Use the GitHub MCP server to create an issue with:
- Title: $ARGUMENTS
- Body: Current file context and error details
- Labels: bug, needs-triage
```

**Natural language queries**: Remember that MCP servers work best with natural language rather than explicit function calls. Describe what you need instead of trying to invoke specific tools. ([Cloud Artisan MCP Tips][4])

### Performance Optimization

**Selective enablement**: Only enable servers you need to reduce context window consumption and improve response times.

**Scope appropriately**: Use project scope for team tools, user scope for personal utilities, local scope for temporary experiments.

**Monitor token usage**: Be aware that MCP server tool definitions consume tokens from your context window.

### Security Hygiene

**Regular audits**: Periodically review configured servers and remove unused ones.

**Credential rotation**: Rotate API keys and tokens regularly, especially for production systems.

**Least privilege**: Grant minimum necessary permissions to each MCP server.

**Environment isolation**: Use different credentials for development, staging, and production environments.

## Use Cases

### GitHub Integration Example

Connect Claude Code to GitHub to enable: ([Top 10 MCP Servers][5])

- Reading and analyzing issues
- Managing pull requests
- Triggering CI/CD workflows
- Analyzing commits and repository history
- Creating issues directly from conversation

**Setup**:
```bash
claude mcp add --transport stdio github \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxx \
  -- npx -y @modelcontextprotocol/server-github
```

**Usage**: Ask natural language questions like "What are the open high-priority bugs?" or "Create a PR for this feature."

### Database Query Example

Connect to PostgreSQL for natural language database queries:

**Setup**:
```bash
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost/db \
  -- npx -y @modelcontextprotocol/server-postgres
```

**Usage**: Ask questions like "Show me users who signed up last week" or "What's the average order value by region?"

### Error Monitoring Example

Integrate Sentry for production error analysis: ([Top 10 MCP Servers][5])

**Setup**:
```bash
claude mcp add --transport stdio sentry \
  --env SENTRY_AUTH_TOKEN=your_token \
  --env SENTRY_ORG=your_org \
  -- npx -y @modelcontextprotocol/server-sentry
```

**Usage**: "What are the most frequent errors this week?" or "Show me the stack trace for issue #12345."

### Filesystem Operations Example

Enable local file system access with explicit directory boundaries:

**Setup**:
```bash
claude mcp add --transport stdio filesystem \
  -- npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

**Usage**: "Search for all TODO comments in the source files" or "Analyze the structure of configuration files."

## Troubleshooting

### Server Not Connecting

**Check installation**: Verify the server is listed:
```bash
claude mcp list
```

**Verify credentials**: Ensure environment variables are set correctly and accessible.

**Debug mode**: Launch with `claude --mcp-debug` to see detailed connection logs.

**Check transport**: Verify you're using the correct transport (http/sse/stdio) for your server type.

### Authentication Failures

**Token expiration**: Check if your API token or OAuth token has expired.

**Permissions**: Verify the token has necessary scopes and permissions.

**Re-authenticate**: Use `/mcp` command in Claude Code to re-authenticate.

**Environment variables**: Confirm environment variables are correctly interpolated in `.mcp.json`.

### Performance Issues

**Too many servers**: Disable unused MCP servers to free up context window.

**Output limits**: Adjust `MAX_MCP_OUTPUT_TOKENS` if hitting limits.

**Server responsiveness**: Some servers may be slow; consider timeout implications.

### Configuration Errors

**Scope mismatch**: Ensure you're using the right scope (local/user/project) for your use case.

**JSON syntax**: Validate `.mcp.json` syntax using a JSON validator.

**Path issues**: Use absolute paths for filesystem servers to avoid ambiguity.

**Command arguments**: Ensure the `--` separator is used correctly for stdio servers.

## Future Considerations

### Growing Ecosystem

The MCP ecosystem is rapidly expanding with new servers being released regularly. Development platforms like Zed and Replit are enhancing their tools through MCP integration. ([MCP Announcement][3])

### Standardization Benefits

As the ecosystem matures, MCP provides a more sustainable architecture than fragmented custom integrations. Rather than maintaining separate connectors for each data source, developers build against one standard. ([MCP Announcement][3])

### AI Agent Evolution

MCP enables AI agents to better retrieve relevant information and maintain context across different tools and datasets, supporting more sophisticated agentic workflows. ([MCP Announcement][3])

## References

[1]: https://anthropic.mintlify.app/en/docs/claude-code/mcp "Claude Code MCP Documentation"
[2]: https://modelcontextprotocol.io/specification/2025-06-18 "Model Context Protocol Specification"
[3]: https://www.anthropic.com/news/model-context-protocol "Anthropic MCP Announcement"
[4]: https://cloudartisan.com/posts/2025-04-12-adding-mcp-servers-claude-code/ "Claude Code Tips - MCP Servers"
[5]: https://apidog.com/blog/top-10-mcp-servers-for-claude-code/ "Top 10 MCP Servers for Claude Code"
