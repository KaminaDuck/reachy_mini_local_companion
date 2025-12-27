---
title: "Prime Reference Links"
description: "Load context by analyzing a subject reference, fetching documentation and reviewing README"
type: "command"
tags: ["initialization", "context", "references", "documentation", "web"]
category: "documentation"
subcategory: "research"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
allowed-tools: Bash, Read, WebFetch, Glob, Grep
requires_args: true
argument_hint: "[reference-urls-or-topics]"
usage_examples:
  - "/prime-reference-links https://docs.example.com/guide"
  - "/prime-reference-links OpenTelemetry Tracing"
---

# Prime

Run the commands under the `Execute` section to gather information about the project, and then review the files listed under `Reference` to understand the subject the user wishes you to receive context for and functionality then `Report` your findings.

## Execute

- `git ls-files`

## Reference
$ARGUMENTS

## Report

- Provide a summary of your understanding of the topic
- Provide a report of the resources you used fetch on to retrieve the actual contents. 
