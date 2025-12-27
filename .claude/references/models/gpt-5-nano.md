---
title: "GPT-5 Nano Model Reference"
description: "Ultra-low-latency reasoning model optimized for speed and cost-efficiency"
type: "model-spec"
tags: ["llm", "reasoning", "api", "openai", "low-latency", "multimodal", "gpt-5"]
category: "ai-models"
subcategory: "inference"
version: "1.0"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "OpenAI GPT-5 Announcement"
    url: "https://openai.com/index/introducing-gpt-5-for-developers/"
  - name: "Azure AI Foundry Reasoning Models"
    url: "https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning"
  - name: "OpenRouter GPT-5 Nano"
    url: "https://openrouter.ai/openai/gpt-5-nano"
  - name: "SWE-bench GPT-5 Analysis"
    url: "https://www.swebench.com/SWE-bench/blog/2025/08/08/gpt5/"
  - name: "Vellum GPT-5 Benchmarks"
    url: "https://www.vellum.ai/blog/gpt-5-benchmarks"
  - name: "Encord GPT-5 Technical Breakdown"
    url: "https://encord.com/blog/gpt-5-a-technical-breakdown/"
related: ["gpt_oss_120b.md"]
author: "unknown"
contributors: []
---

# Summary

GPT-5-Nano is the smallest and fastest variant in the GPT-5 reasoning model system, optimized for ultra-low-latency applications, developer tools, and high-volume deployments. ([OpenAI][1]) Released August 7, 2025, it offers rich Q&A capabilities with reduced reasoning depth compared to larger GPT-5 variants, making it ideal for mobile apps, edge devices, chatbots, and latency-sensitive applications. ([OpenRouter][2])

# Identity

* **Name:** gpt-5-nano
* **Alternative ID:** gpt-5-nano-2025-08-07
* **Publisher:** OpenAI
* **Release Date:** August 7, 2025 ([OpenAI][1])
* **License:** Proprietary (API access only)
* **Knowledge Cutoff:** May 30, 2024

# Architecture

* **Type:** Reasoning model optimized for speed and lightweight deployment. ([OpenAI][1])
* **Context Window:** Up to 400,000 tokens input. ([OpenRouter][2])
* **Max Output:** 128,000 tokens in a single response. ([OpenRouter][2])
* **Modality:** Text and image input; text-only output. ([Vellum][3])
* **Optimization:** Ultra-low-latency architecture for rapid, high-accuracy responses. ([Azure][4])

# Pricing

* **Input Tokens:** $0.05 per 1M tokens ([OpenRouter][2])
* **Output Tokens:** $0.40 per 1M tokens ([OpenRouter][2])
* **Position:** Most affordable model in GPT-5 family. ([Vellum][3])
* **SWE-bench Cost:** Maximum approximately $0.015 per instance. ([SWE-bench][5])

# API Parameters

## Unsupported Parameters

GPT-5-Nano as a reasoning model does **not support** the following parameters: ([Azure][4])
- `temperature`
- `top_p`
- `presence_penalty`
- `frequency_penalty`
- `logprobs`
- `top_logprobs`
- `logit_bias`
- `max_tokens` (deprecated for reasoning models)

**Note:** Passing unsupported parameters like `temperature` will result in a 400 Bad Request error. ([Azure][4])

## Supported Parameters

* **`max_completion_tokens`**: Maximum tokens for response when using Chat Completions API. ([Azure][4])
* **`max_output_tokens`**: Maximum tokens including visible output and reasoning tokens when using Responses API. Default: 512. ([Azure][4])
* **`reasoning_effort`**: Controls reasoning depth. Values: `minimal`, `low`, `medium`, `high`. GPT-5 reasoning models support the new `minimal` setting. ([Azure][4])
* **`prompt`**: Input text or messages.
* **`stop_sequences`**: Token sequences that stop generation.

## API Endpoints

* **Chat Completions API:** `/v1/chat/completions`
* **Responses API:** `/v1/responses`
* **Model Parameter:** `"gpt-5-nano"` or `"gpt-5-nano-2025-08-07"`

# Benchmarks

Performance benchmarks reflect trade-offs between model size, speed, and capability. ([Vellum][3])

## Academic & Coding Benchmarks

* **MMLU:** Solid performance, reduced from larger GPT-5 variants but competitive for nano tier. ([Vellum][3])
* **AIME '25:** Competent performance proportional to model size. ([Encord][6])
* **SWE-bench:** Half the performance of full GPT-5 at half the cost - strong cost-efficiency ratio. ([SWE-bench][5])
* **Multimodal Tasks:** Above 60% on MMMU and VideoMMU, maintaining competent multimodal understanding. ([Vellum][3])

## Reliability

* **Hallucination Rate:** Higher than larger GPT-5 variants, reflecting size/reliability trade-off. Users should implement validation for factual accuracy in production. ([Encord][6])

# Capabilities

* **Ultra-Low Latency:** Optimized for rapid responses in high-volume scenarios. ([Azure][4])
* **Reasoning:** Rich Q&A capabilities with reduced reasoning depth compared to GPT-5 standard/mini. ([OpenAI][1])
* **Multimodal Input:** Supports text and image inputs. ([Vellum][3])
* **Instruction Following:** Retains key instruction-following features from GPT-5 family.
* **Safety Features:** Maintains core safety features from GPT-5 family. ([OpenAI][1])
* **Fine-tuning Target:** Ideal model for fine-tuning due to low cost and fast iteration. ([Azure][4])

# Use Cases

## Ideal For

* **High-Volume Applications:** Chatbots, customer support, FAQ systems where speed and cost matter. ([OpenRouter][2])
* **Latency-Sensitive Applications:** Real-time interactions, live chat, interactive experiences. ([Azure][4])
* **Mobile Apps:** Lightweight deployment for mobile and edge devices. ([OpenAI][1])
* **Developer Tools:** Code completion, quick Q&A, documentation lookup. ([OpenAI][1])
* **Cost-Constrained Deployments:** High throughput with budget constraints. ([OpenRouter][2])
* **Fine-tuning Projects:** Fast iteration and experimentation at low cost. ([Azure][4])

## Consider Larger Variants If

* **Deep Reasoning Required:** Complex mathematical proofs, advanced code generation, multi-step problem solving. ([Encord][6])
* **Lower Hallucination Rate Needed:** Mission-critical factual accuracy requirements. ([Encord][6])
* **Maximum Benchmark Performance:** Top-tier academic or coding benchmarks are required. ([Vellum][3])

# Deployment Options

* **OpenAI API:** Direct access via OpenAI Platform. ([OpenAI][1])
* **Azure AI Foundry:** Available through Azure OpenAI service with enterprise features. ([Azure][4])
* **OpenRouter:** Third-party API aggregator with unified interface. ([OpenRouter][2])

# Usage Example

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ],
    max_completion_tokens=500,
    reasoning_effort="low"  # Options: minimal, low, medium, high
)

print(response.choices[0].message.content)
```

# Configuration Recommendations

## For Maximum Speed

* Set `reasoning_effort="minimal"` or `"low"`
* Use shorter `max_completion_tokens` (e.g., 256-512)
* Deploy in low-latency regions
* Optimize prompt length and structure

## For Cost Optimization

* Minimize input tokens through efficient prompting
* Set appropriate `max_completion_tokens` limits
* Batch similar requests when possible
* Use `reasoning_effort="minimal"` for simple queries
* Implement caching for common responses

## For Quality Balance

* Use `reasoning_effort="medium"` for standard queries
* Set `reasoning_effort="high"` only for complex questions requiring deeper analysis
* Monitor hallucination rates in production
* Implement output validation for critical applications

# Limitations

* **Reduced Reasoning Depth:** Less capable than GPT-5 standard or mini for complex reasoning tasks. ([OpenAI][1])
* **Higher Hallucination Rate:** Trade-off between model size and reliability - validation recommended. ([Encord][6])
* **No Temperature Control:** Cannot adjust sampling randomness via temperature parameter. ([Azure][4])
* **Text-Only Output:** No image or multimodal output generation. ([Vellum][3])
* **API-Only Access:** No local deployment or open weights available. ([OpenRouter][2])

# Comparison with GPT-5 Family

| Feature | GPT-5 Nano | GPT-5 Mini | GPT-5 Standard |
|---------|-----------|-----------|----------------|
| **Input Price** | $0.05/1M | Higher | Highest |
| **Output Price** | $0.40/1M | Higher | Highest |
| **Latency** | Ultra-low | Low | Standard |
| **Reasoning Depth** | Limited | Moderate | Deep |
| **Context Window** | 400K tokens | Similar | Similar |
| **Best For** | Speed/Cost | Balance | Quality |

([OpenRouter][2], [Vellum][3])

# Production Considerations

* **Monitor Costs:** Track token usage carefully in high-volume applications.
* **Validate Outputs:** Implement verification for factual accuracy due to size/reliability trade-offs.
* **Reasoning Effort Tuning:** Start with `minimal` or `low`, increase only when needed for complex queries.
* **Fallback Strategy:** Consider fallback to GPT-5 mini for queries requiring deeper reasoning.
* **Rate Limiting:** Implement appropriate rate limits for API calls to control costs.
* **Error Handling:** Handle 400 errors from unsupported parameters gracefully.
* **Caching Strategy:** Cache common responses to reduce API calls and costs.
* **Performance Monitoring:** Track latency, quality metrics, and cost per request.

# References

[1]: https://openai.com/index/introducing-gpt-5-for-developers/ "Introducing GPT-5 for developers - OpenAI"
[2]: https://openrouter.ai/openai/gpt-5-nano "GPT-5 Nano - OpenRouter"
[3]: https://www.vellum.ai/blog/gpt-5-benchmarks "GPT-5 Benchmarks - Vellum"
[4]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning "Azure OpenAI reasoning models - Microsoft Learn"
[5]: https://www.swebench.com/SWE-bench/blog/2025/08/08/gpt5/ "GPT-5 on SWE-bench - SWE-bench"
[6]: https://encord.com/blog/gpt-5-a-technical-breakdown/ "GPT-5 Technical Breakdown - Encord"
