---
title: "Prime Context"
description: "Load context for a new agent session by analyzing codebase structure and documentation"
type: "command"
tags: ["initialization", "context", "codebase", "documentation", "onboarding"]
category: "development"
subcategory: "setup"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed-tools: Bash, Read, Glob, Grep
requires_args: false
usage_examples:
  - "/prime"
---

# Prime

Run the commands under the `Execute` section to gather information about the project, and then review the files listed under `Read` to understand the project's purpose and functionality then `Report` your findings.

## Execute

- `git ls-files`

## Read

- README.md

## Report

- Provide a summary of your understanding of the project
