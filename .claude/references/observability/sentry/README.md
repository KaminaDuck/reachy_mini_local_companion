---
author: unknown
category: observability
contributors: []
description: Reference documentation for self-hosted Sentry deployment and configuration
last_updated: '2025-08-16'
related:
- README.md
- opentelemetry-best-practices.md
sources:
- name: Sentry Self-Hosted GitHub
  url: https://github.com/getsentry/self-hosted
- name: Sentry Self-Hosted Documentation
  url: https://develop.sentry.dev/self-hosted/
status: stable
subcategory: sentry
tags:
- index
- sentry
- observability
- error-tracking
- self-hosted
title: Sentry Self-Hosted Reference Index
type: meta
version: '1.0'
---

# Sentry Self-Hosted Reference Index

Reference documentation for deploying and managing self-hosted Sentry error tracking and application monitoring platform.

## Overview

Sentry is an open-source error tracking and performance monitoring platform. The self-hosted version provides full Sentry functionality packaged for low-volume deployments and proof-of-concept environments, supporting approximately 1 million events per month ([Self-Hosted Documentation][1]).

## Documentation Files

### [Self-Hosted Deployment Guide](self-hosted-deployment.md)
Comprehensive deployment guide for self-hosted Sentry including Docker Compose setup, system requirements, configuration options, upgrade procedures, backup strategies, troubleshooting, and production best practices.

## Key Features

- **Error Tracking**: Capture and aggregate application errors across all platforms
- **Performance Monitoring**: Distributed tracing and performance insights
- **Release Tracking**: Monitor deployments and track issues by release
- **Alert Management**: Configurable alerting rules and notifications
- **Integrations**: GitHub, GitLab, Slack, and other third-party services
- **Multi-tenancy**: Organizations, teams, and projects structure

## Platform Support

Sentry SDKs available for:
- **Languages**: Python, JavaScript/TypeScript, Go, Java, PHP, Ruby, Rust, .NET, C/C++
- **Frameworks**: React, Next.js, Django, Flask, FastAPI, Express, Laravel
- **Mobile**: iOS, Android, React Native
- **Game Engines**: Unity, Unreal Engine, Godot

## License

Self-hosted Sentry is licensed under the Functional Source License (FSL) ([Self-Hosted Documentation][1]). Users may deploy widely but cannot resell commercially or compete directly with Sentry's offerings.

## External Resources

- [Sentry Documentation](https://docs.sentry.io/)
- [Self-Hosted GitHub Repository](https://github.com/getsentry/self-hosted)
- [Self-Hosted Documentation](https://develop.sentry.dev/self-hosted/)
- [Sentry Community Discord](https://discord.gg/sentry)
- [Release Notes](https://github.com/getsentry/self-hosted/releases)

## References

[1]: https://develop.sentry.dev/self-hosted/ "Sentry Self-Hosted Documentation"