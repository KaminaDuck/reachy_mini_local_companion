---
title: "AI Models Reference Index"
description: "Reference documentation for LLM and ML model specifications"
type: "meta"
tags: ["index", "models", "llm", "ai", "reference"]
category: "ai-models"
subcategory: "none"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources: []
related: []
author: "unknown"
contributors: []
---

# AI Models Reference Index

Comprehensive reference documentation for large language models and machine learning models used in development and production environments.

## Model Specifications

### [GPT-5 Nano](gpt-5-nano.md)
OpenAI's ultra-low-latency reasoning model optimized for speed and cost-efficiency. Ideal for high-volume applications, mobile apps, and latency-sensitive deployments. Features 400K token context window and pricing at $0.05/$0.40 per 1M tokens (input/output).

**Key Features:**
- Ultra-low latency architecture
- 400,000 token context window
- Multimodal input (text + image)
- Most affordable GPT-5 variant
- Released: August 7, 2025

### [GPT-OSS 120B](gpt_oss_120b.md)
OpenAI's open-weight 120B MoE reasoning LLM with Apache-2.0 license. Fits on a single 80GB GPU via MXFP4 quantization. Strong general reasoning capabilities positioned near o4-mini on core benchmarks.

**Key Features:**
- Mixture-of-Experts architecture (117B total, ~5.1B active)
- MXFP4 quantization for single GPU deployment
- 131,072 token context window
- Apache-2.0 licensed (open-weight)
- vLLM deployment support

## Model Comparison

| Model | Type | Context | License | Best For |
|-------|------|---------|---------|----------|
| **GPT-5 Nano** | Reasoning (API) | 400K | Proprietary | Ultra-low latency, cost-sensitive, high-volume |
| **GPT-OSS 120B** | MoE Reasoning (Open) | 131K | Apache-2.0 | Self-hosted reasoning, single-GPU deployment |

## Use Case Guide

### When to Use GPT-5 Nano
- **Chatbots & customer support:** Fast responses at low cost
- **Mobile applications:** Lightweight API integration
- **Developer tools:** Code completion, documentation lookup
- **High-volume deployments:** Budget-constrained with high throughput
- **Fine-tuning projects:** Fast iteration and experimentation

### When to Use GPT-OSS 120B
- **Self-hosted deployments:** On-premise or cloud infrastructure control
- **Privacy-sensitive applications:** Data stays in your environment
- **Custom modifications:** Open-weight allows model adaptation
- **Agentic workloads:** Long-form reasoning and step-by-step responses
- **Research & development:** Open access for experimentation

## External Resources

### OpenAI Platform
- [OpenAI Models Documentation](https://platform.openai.com/docs/models)
- [GPT-5 Nano API Reference](https://platform.openai.com/docs/models/gpt-5-nano)
- [GPT-OSS Announcement](https://openai.com/index/introducing-gpt-oss/)

### Deployment Resources
- [vLLM Documentation](https://blog.vllm.ai/)
- [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-foundry/)
- [OpenRouter API](https://openrouter.ai/)

### Community & Support
- [Hugging Face Model Hub](https://huggingface.co/openai)
- [OpenAI Developer Forum](https://community.openai.com/)
