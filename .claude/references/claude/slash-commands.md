---
title: "Claude Code Slash Commands Reference"
description: "Comprehensive guide to creating and using custom slash commands in Claude Code"
type: "tool-reference"
tags: ["claude-code", "slash-commands", "automation", "workflows", "productivity", "customization"]
category: "claude"
subcategory: "customization"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Claude Code Slash Commands Documentation"
    url: "https://anthropic.mintlify.app/en/docs/claude-code/slash-commands"
  - name: "Claude Code Tips - Custom Slash Commands"
    url: "https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/"
  - name: "Claude Code Slash Commands Productivity Guide"
    url: "https://alexop.dev/tils/claude-code-slash-commands-boost-productivity/"
  - name: "Awesome Claude Code Repository"
    url: "https://github.com/hesreallyhim/awesome-claude-code"
  - name: "Claude Code Best Practices"
    url: "https://www.anthropic.com/engineering/claude-code-best-practices"
related: []
author: "unknown"
contributors: []
---

# Claude Code Slash Commands Reference

Slash commands are reusable prompt templates that control Claude's behavior during interactive sessions. They enable you to encode workflows once and invoke them with simple `/command-name` syntax, reducing token usage and standardizing team workflows. ([Slash Commands Docs][1])

## Overview

Slash commands fall into four categories: ([Slash Commands Docs][1])

1. **Built-in commands** - Core Claude Code operations (24+ commands)
2. **Custom commands** - User-defined Markdown prompts
3. **Plugin commands** - Commands provided by Claude Code plugins
4. **MCP commands** - Commands exposed by MCP (Model Context Protocol) servers

## Built-in Commands

Claude Code includes 24+ built-in slash commands for essential operations: ([Slash Commands Docs][1])

**Navigation & Session**
- `/clear` - Clear the conversation history
- `/rewind` - Rewind to a previous state
- `/status` - Show current session status
- `/help` - Display available commands

**Configuration**
- `/config` - Configure settings
- `/model` - Select AI model
- `/permissions` - Manage tool permissions
- `/login` - Authenticate
- `/logout` - Sign out

**Development**
- `/review` - Code review workflows
- `/bug` - Bug investigation
- `/sandbox` - Isolated testing environment
- `/terminal-setup` - Terminal configuration

**Project Management**
- `/init` - Initialize new project
- `/memory` - Manage conversation memory
- `/cost` - View usage costs
- `/usage` - Track usage metrics

**Integration**
- `/mcp` - MCP server management
- `/agents` - Agent control
- `/add-dir` - Add directories to context

## Custom Slash Commands

### Creating Commands

Custom slash commands are Markdown files stored in two locations: ([Slash Commands Docs][1], [Cloud Artisan Tips][2])

**Project-level** (`.claude/commands/`): Shared with your team via version control
**User-level** (`~/.claude/commands/`): Available across all your projects

Example creation:

```bash
# Project-level command
mkdir -p .claude/commands
echo "Analyze this code for performance issues:" > .claude/commands/optimize.md

# User-level command
mkdir -p ~/.claude/commands
echo "Review my git changes and suggest a commit message" > ~/.claude/commands/commit.md
```

Commands become available immediately when saved. Type `/` to see them in the autocomplete menu. ([Slash Commands Docs][1])

### Command Syntax

```
/<command-name> [arguments]
```

Examples:
```
/optimize
/commit fix authentication bug
/review-pr 123
```

### Arguments and Interpolation

Commands support dynamic values through placeholder variables: ([Slash Commands Docs][1], [Alexop Productivity][3])

**`$ARGUMENTS`**: Captures all passed arguments as a single string

```markdown
Review the following code for $ARGUMENTS issues:
```

Usage: `/review security` → "Review the following code for security issues:"

**Positional arguments** (`$1`, `$2`, etc.): Individual argument access

```markdown
Review PR #$1 with priority $2 and assign to $3
```

Usage: `/review-pr 123 high alice` → "Review PR #123 with priority high and assign to alice"

**Design tip**: Commands should function sensibly whether `$ARGUMENTS` is provided or omitted, increasing flexibility. ([Cloud Artisan Tips][2])

### Frontmatter Configuration

Commands support YAML frontmatter for metadata and behavior control: ([Slash Commands Docs][1])

```yaml
---
description: Create a conventional commit message
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [message]
model: sonnet
disable-model-invocation: false
---
```

#### Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `description` | Brief command description shown in `/help` | `"Create a git commit"` |
| `allowed-tools` | Whitelist of tools the command can access | `Bash(git:*)` |
| `argument-hint` | Expected arguments for autocomplete | `[pr-number]` |
| `model` | Specific AI model to use | `sonnet`, `opus`, `haiku` |
| `disable-model-invocation` | Prevent programmatic execution by Claude | `true` or `false` |

**Security**: Use `allowed-tools` to restrict command capabilities and prevent unintended operations. ([Slash Commands Docs][1])

### Advanced Features

#### Bash Execution

Use `!` prefix to run shell commands and inject their output into the prompt: ([Slash Commands Docs][1])

```markdown
---
description: Commit changes with context
---

Current git status:
!`git status`

Recent commits for reference:
!`git log --oneline -10`

Create a conventional commit message based on the changes above.
```

**Note**: Bash execution happens *before* the command is sent to Claude, injecting the output directly into the prompt.

#### File References

Use `@` prefix to include file contents in the prompt: ([Slash Commands Docs][1])

```markdown
---
description: Review implementation
---

Review the implementation in @src/utils/helpers.js and suggest improvements.
```

#### Namespacing

Organize commands in subdirectories for better organization. ([Slash Commands Docs][1], [Cloud Artisan Tips][2])

**Example directory structure**:
```
.claude/commands/
├── git/
│   ├── commit.md
│   └── pr.md
├── posts/
│   ├── create.md
│   └── publish.md
└── help.md
```

Commands appear with namespace prefixes:
- `.claude/commands/git/commit.md` → `/commit` (shows "project:git" in `/help`)
- `.claude/commands/posts/create.md` → `/create` (shows "project:posts" in `/help`)

**Organizational tip**: Structure commands hierarchically by function for intuitive discovery as your library grows. ([Cloud Artisan Tips][2])

### SlashCommand Tool

The `SlashCommand` tool enables Claude to programmatically execute custom slash commands during conversations. ([Slash Commands Docs][1])

**Requirements**:
- Command must be user-defined (not built-in)
- Must include `description` in frontmatter
- Must not have `disable-model-invocation: true`

**Permission control**:
```
SlashCommand:/commit                 # Exact match
SlashCommand:/review-pr:*            # With any arguments
SlashCommand:*                       # All custom commands
```

**Trigger tip**: To encourage Claude to invoke commands automatically, reference them by name (with `/` prefix) in your `CLAUDE.md` instructions. ([Awesome Claude Code][4])

## Plugin Commands

Plugins can provide custom slash commands following the pattern `/plugin-name:command-name`. ([Slash Commands Docs][1])

Plugin commands:
- Support all standard command features (arguments, frontmatter, bash execution)
- Reside in the plugin's `commands/` directory
- Appear automatically in `/help` when the plugin is installed

Example: A git plugin might provide `/git:squash`, `/git:rebase`, etc.

## MCP Slash Commands

MCP (Model Context Protocol) servers expose prompts as slash commands using the pattern: ([Slash Commands Docs][1])

```
/mcp__<server-name>__<prompt-name> [arguments]
```

MCP commands are automatically discovered when servers connect successfully and appear in `/help`.

Example: `/mcp__github__create-issue "Fix login bug"`

## Best Practices

### Command Design

**Use descriptive names** that reflect the command's purpose clearly. ([Slash Commands Docs][1])
- Good: `/review-security`, `/create-component`, `/deploy-staging`
- Bad: `/r`, `/do`, `/x`

**Include clear descriptions** in frontmatter for discoverability in `/help`. ([Slash Commands Docs][1])

**Specify allowed-tools** to restrict command capabilities and prevent accidents. ([Slash Commands Docs][1])

```yaml
---
description: Deploy to production
allowed-tools: Bash(git:*), Bash(docker:*)
---
```

**Provide argument hints** for better user experience and autocomplete. ([Slash Commands Docs][1])

```yaml
---
argument-hint: [environment] [version]
---
```

### Organization

**Namespace by category** using subdirectories for teams and large projects. ([Cloud Artisan Tips][2])

**Version control project commands** by committing `.claude/commands/` to git, making them available to your entire team. ([Cloud Artisan Tips][2], [Alexop Productivity][3])

**Document your commands** with a `/help` or `/view-commands` reference guide listing all available operations by category. ([Cloud Artisan Tips][2])

Example help command structure:

```markdown
---
description: Show all available custom commands
---

# Available Commands

## Git Workflows
- `/commit` - Create conventional commit
- `/pr` - Create pull request

## Content Management
- `/create-post` - Generate new blog post
- `/publish` - Publish to production

## Quality Assurance
- `/lint` - Run linters and formatters
- `/test` - Execute test suite
```

### Productivity Optimization

**Extract fixed workflows** from `CLAUDE.md` into slash commands to reduce token consumption. ([Alexop Productivity][3])

Instead of loading repetitive instructions every session, encode them once:

**Before (in `CLAUDE.md`)**:
```markdown
When I ask you to commit changes:
1. Run git status
2. Review changes
3. Create conventional commit message
4. Use imperative mood
5. Keep subject under 50 characters
...
```

**After (in `.claude/commands/commit.md`)**:
```markdown
---
description: Create conventional commit
---
!`git status`

Review the changes above and create a conventional commit message.
Use imperative mood and keep subject under 50 characters.
```

**Result**: Token usage reduced by ~20% for repeated workflows. ([Alexop Productivity][3])

**Design for reusability**: Make commands flexible enough to handle variations through `$ARGUMENTS`. ([Cloud Artisan Tips][2])

**Chain commands together** for complex workflows, reducing dozens of manual steps to a few command invocations. ([Awesome Claude Code][4])

### Common Use Cases

Based on community implementations, effective slash command categories include: ([Awesome Claude Code][4], [Cloud Artisan Tips][2])

**Version Control & Git**
- Commit message generation
- PR creation and review
- Branch management
- Changelog updates

**Code Analysis & Testing**
- Code review workflows
- Security audits
- Performance analysis
- Test generation and execution

**Context Loading & Priming**
- Project setup and initialization
- Codebase exploration
- Architecture documentation
- Dependency analysis

**Documentation**
- README generation
- API documentation
- Changelog creation
- Comment generation

**CI/CD & Deployment**
- Release workflows
- Deployment automation
- Environment management
- Build verification

**Project & Task Management**
- Task tracking
- Progress reporting
- Sprint planning
- Issue management

## Skills vs. Slash Commands

Choose between skills and slash commands based on complexity: ([Slash Commands Docs][1])

**Use Slash Commands when:**
- Prompt fits comfortably in a single Markdown file
- Workflow is relatively simple and linear
- You need frequent, quick invocation
- Team standardization is the primary goal

**Use Agent Skills when:**
- Capabilities require multiple files and complex logic
- Need automatic discovery and structured workflows
- Building reusable components for multiple projects
- Require sophisticated state management

## Troubleshooting

### Commands Not Appearing

**Check file location**: Ensure files are in `.claude/commands/` (project) or `~/.claude/commands/` (user). ([Slash Commands Docs][1])

**Verify filename**: Commands use the filename (without `.md`) as the command name.

**Restart if needed**: Claude Code typically detects new commands immediately, but restart if they don't appear.

### Arguments Not Working

**Clarify formatting requirements** within the command markdown when using `$ARGUMENTS` for complex inputs. ([Cloud Artisan Tips][2])

Example:
```markdown
---
description: Create component
argument-hint: [ComponentName] [variant]
---

Create a React component with the following arguments:
- Component name: $1 (PascalCase)
- Variant: $2 (default|minimal|full)
```

### SlashCommand Tool Not Triggering

**Add description**: The `SlashCommand` tool requires commands to have a `description` field in frontmatter. ([Slash Commands Docs][1])

**Check permissions**: Verify SlashCommand tool is allowed in your permissions settings.

**Reference explicitly**: Include command names (with `/` prefix) in your `CLAUDE.md` instructions to encourage automatic invocation. ([Awesome Claude Code][4])

Example in `CLAUDE.md`:
```markdown
For git operations, you can use:
- `/commit` - Create conventional commits
- `/pr` - Generate pull requests
```

### False Positives in Validation Commands

When creating validation commands (orphan file detection, link checking, etc.), be aware that variant files may create false positives. ([Cloud Artisan Tips][2])

Example: Checking for orphaned images might flag `-150x150.png` thumbnails that are actually referenced dynamically.

**Solution**: Build exclusion patterns into your validation logic or document known false positives.

## Examples

### Basic Commit Command

```markdown
---
description: Create conventional commit message
allowed-tools: Bash(git:*)
argument-hint: [type] [message]
---

!`git status`
!`git diff --staged`

Create a conventional commit message for the changes above.
Type: $1
Message: $ARGUMENTS
```

### Content Creation Workflow

```markdown
---
description: Create new blog post
allowed-tools: Write, Bash(git:*)
argument-hint: [title]
---

Create a new blog post with:
- Title: $ARGUMENTS
- Filename: Kebab-case from title
- Front matter: date, author, tags
- Basic structure: intro, body, conclusion
- Save in `content/posts/`
```

### Code Review Command

```markdown
---
description: Review code for common issues
allowed-tools: Read, Grep
model: sonnet
---

Review the codebase for:
- Security vulnerabilities (XSS, SQL injection, command injection)
- Performance issues (N+1 queries, memory leaks)
- Code quality (complexity, duplication, naming)
- Best practice violations

Focus areas: $ARGUMENTS

Provide actionable recommendations with line numbers.
```

### Multi-Step Deployment

```markdown
---
description: Deploy to staging environment
allowed-tools: Bash(git:*), Bash(docker:*)
disable-model-invocation: true
---

!`git status`

Deploy to staging:
1. Verify clean working directory
2. Run tests
3. Build Docker image
4. Tag with commit hash
5. Push to staging registry
6. Update staging deployment
7. Verify health checks

Environment: staging
Version: $1
```

## References

[1]: https://anthropic.mintlify.app/en/docs/claude-code/slash-commands "Claude Code Slash Commands Documentation"
[2]: https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/ "Claude Code Tips - Custom Slash Commands"
[3]: https://alexop.dev/tils/claude-code-slash-commands-boost-productivity/ "Claude Code Slash Commands Productivity Guide"
[4]: https://github.com/hesreallyhim/awesome-claude-code "Awesome Claude Code Repository"
[5]: https://www.anthropic.com/engineering/claude-code-best-practices "Claude Code Best Practices"
