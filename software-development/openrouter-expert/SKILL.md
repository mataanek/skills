---
name: openrouter-expert
description: "Build with OpenRouter API and SDKs - resolver skill for choosing the right OpenRouter integration, verifying docs, and implementing AI features safely"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [openrouter, api, sdk, integration, llm, agent, tools, structured-outputs]
---

# OpenRouter Expert Skill

A resolver skill for building with OpenRouter API and SDKs. Always verify against current docs before making claims.

## When to Load This Skill
Use this skill when the user wants to:
- Integrate AI models via OpenRouter's unified API
- Build chatbots, assistants, or autonomous agents
- Implement tool/function calling or structured outputs
- Work with multimodal inputs (images, PDFs, audio, video)
- Configure model routing, fallbacks, or provider selection
- Use OpenRouter SDKs (@openrouter/sdk, @openrouter/agent) or framework integrations
- Manage API keys, workspaces, guardrails, or usage accounting
- Implement observability, logging, or evaluation workflows

## Pre-Answer Ritual
Before answering any OpenRouter question:
1. Refresh/read https://openrouter.ai/docs/llms.txt (the canonical index)
2. Consult https://openrouter.ai/docs/llms-full.txt only for page-level details when needed
3. Verify all docs URLs appear in llms.txt before linking
4. Fetch /api/v1/models when model IDs, capabilities, or pricing matter
5. Prefer live docs/API over cached knowledge for changing facts

## Core API Surface
**Base URL**: `https://openrouter.ai/api/v1`

**Authentication**:
- Header: `Authorization: Bearer $OPENROUTER_API_KEY`
- Optional attribution: `HTTP-Referer` and `X-Title` for app rankings

**Key Endpoints** (verify in current docs):
- `GET /api/v1/models` - List available models
- `POST /api/v1/chat/completions` - Chat completions (streaming supported)
- `POST /api/v1/embeddings` - Generate embeddings
- `POST /api/v1/auth/key` - Manage API keys (see Management API Keys guide)
- `GET /api/v1/credits` - Check remaining credits
- `POST /api/v1/responses` - Responses API Beta (reasoning, tool calling, web search)

## SDK Decision Framework

| SDK/Package | Best For | Language | Key Features |
|-------------|----------|----------|--------------|
| `@openrouter/sdk` | Direct typed API access | TypeScript, Python, Go | Lightweight wrappers around REST API, full endpoint coverage |
| `@openrouter/agent` | Agentic workflows with tools/loops | TypeScript (primary) | `callModel`, tool definitions, stop conditions, state management, streaming |
| OpenAI SDK | Drop-in replacement | Any OpenAI-compatible | Uses OpenRouter as base URL with minimal code changes |
| Framework Adapters | Existing framework integration | Varies | LangChain, Vercel AI SDK, PydanticAI, LiveKit, Anthropic Agent SDK |

**SDK Selection Rules**:
- Use `@openrouter/agent` when you need: multi-turn conversations, tool execution, stop conditions, or state persistence
- Use `@openrouter/sdk` or direct REST for: simple model calls, embeddings, account operations, custom orchestration
- Use OpenAI SDK when migrating from OpenAI with minimal changes
- Use framework adapters when already committed to a specific framework

**Important**: Always link to current SDK docs from llms.txt - do not guess paths.

## Task-to-Docs Routing Table
Map developer tasks to canonical docs URLs (verify each URL in llms.txt):

| Task | Docs URL (from llms.txt) |
|------|--------------------------|
| Quickstart & Auth | https://openrouter.ai/docs/quickstart.mdx |
| Model Listing & Selection | https://openrouter.ai/docs/guides/overview/models.mdx |
| Chat Completions | https://openrouter.ai/docs/api/reference/chat/send-chat-completion-request.mdx |
| Streaming Responses | https://openrouter.ai/docs/api/reference/streaming.mdx |
| Embeddings | https://openrouter.ai/docs/api/reference/embeddings/create-embeddings.mdx |
| Tool/Function Calling | https://openrouter.ai/docs/guides/features/tool-calling.mdx |
| Server Tools Overview | https://openrouter.ai/docs/guides/features/server-tools/overview.mdx |
| Web Search (Server Tool) | https://openrouter.ai/docs/guides/features/server-tools/web-search.mdx |
| Datetime (Server Tool) | https://openrouter.ai/docs/guides/features/server-tools/datetime.mdx |
| Image Generation (Server Tool) | https://openrouter.ai/docs/guides/features/server-tools/image-generation.mdx |
| Web Fetch (Server Tool) | https://openrouter.ai/docs/guides/features/server-tools/web-fetch.mdx |
| Structured Outputs | https://openrouter.ai/docs/guides/features/structured-outputs.mdx |
| Image Inputs (Multimodal) | https://openrouter.ai/docs/guides/overview/multimodal/images.mdx |
| PDF Inputs | https://openrouter.ai/docs/guides/overview/multimodal/pdfs.mdx |
| Audio Input/Output | https://openrouter.ai/docs/guides/overview/multimodal/audio.mdx |
| Video Input/Output | https://openrouter.ai/docs/guides/overview/multimodal/videos.mdx |
| Video Generation | https://openrouter.ai/docs/guides/overview/multimodal/video-generation.mdx |
| Text-to-Speech | https://openrouter.ai/docs/guides/overview/multimodal/tts.mdx |
| Auto Router | https://openrouter.ai/docs/guides/routing/routers/auto-router.mdx |
| Provider Routing | https://openrouter.ai/docs/guides/routing/provider-selection.mdx |
| Model Fallbacks | https://openrouter.ai/docs/guides/routing/model-fallbacks.mdx |
| Model Variants (:free, :extended, etc.) | See individual variant guides under /docs/guides/routing/model-variants/ |
| Workspaces | https://openrouter.ai/docs/guides/features/workspaces.mdx |
| Presets | https://openrouter.ai/docs/guides/features/presets.mdx |
| Response Caching | https://openrouter.ai/docs/guides/features/response-caching.mdx |
| API Key Management | https://openrouter.ai/docs/guides/overview/auth/management-api-keys.mdx |
| BYOK (Bring Your Own Key) | https://openrouter.ai/docs/guides/overview/auth/byok.mdx |
| Guardrails | https://openrouter.ai/docs/guides/features/guardrails.mdx |
| Service Tiers | https://openrouter.ai/docs/guides/features/service-tiers.mdx |
| Input/Output Logging | https://openrouter.ai/docs/guides/features/input-output-logging.mdx |
| Broadcast Integrations | https://openrouter.ai/docs/guides/features/broadcast/overview.mdx |
| Zero Data Retention (ZDR) | https://openrouter.ai/docs/guides/features/zdr.mdx |
| Prompt Caching | https://openrouter.ai/docs/guides/best-practices/prompt-caching.mdx |
| Usage Accounting | https://openrouter.ai/docs/guides/administration/usage-accounting.mdx |
| Activity Export | https://openrouter.ai/docs/guides/administration/activity-export.mdx |
| Automatic Code Review | https://openrouter.ai/docs/guides/coding-agents/automatic-code-review.mdx |
| MCP Servers | https://openrouter.ai/docs/guides/coding-agents/mcp-servers.mdx |
| Framework Integrations | https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview.mdx |
| Client SDKs Overview | https://openrouter.ai/docs/client-sdks/overview.mdx |
| TypeScript SDK | https://openrouter.ai/docs/client-sdks/typescript/overview.mdx |
| Python SDK | https://openrouter.ai/docs/client-sdks/python/overview.mdx |
| Go SDK | https://openrouter.ai/docs/client-sdks/go/overview.mdx |
| Agent SDK | https://openrouter.ai/docs/agent-sdk/overview.mdx |

## Model Selection Framework
**When to use**:
- **Auto Router**: For general-purpose queries where you want OpenRouter to select the best model based on quality, cost, and speed
- **Specific Model**: When you need deterministic behavior, specific capabilities, or have performance requirements
- **Model Variants**: 
  - `:free` - Zero-cost models (verify availability in models API)
  - `:extended` - Extended context window versions
  - `:exacto` - Optimized for tool-calling quality
  - `:thinking` - Extended reasoning capabilities
  - `:online` - Real-time web search capabilities
  - `:nitro` - High-speed inference
- **Fallbacks/Routing**: Use when you need reliability across provider outages or rate limits
- **Always**: Fetch `/api/v1/models` and inspect model properties (context length, pricing, capabilities) before committing to a model ID

**Critical Rules**:
- Never hardcode model IDs - discover them via `/api/v1/models`
- Never construct variant IDs (like `:free`) unless that exact ID appears in the models list
- Variants can have different context lengths, pricing, and capabilities vs base model
- Verify model IDs and variant availability in real-time API

## Tool Calling & Structured Output Framework
**Distinguish**:
- **Native Tool Calling**: Application executes tools (model requests tool use, your code runs them)
- **OpenRouter Server Tools**: OpenRouter executes tools (web search, fetch, etc.) - models decide when to invoke them
- **Structured Outputs**: Constrained model responses that conform to JSON Schema
- **Tool Calls**: Function invocation semantics with defined parameters and return types

**Gotchas**:
- Not all models support tool calling or structured outputs - check model properties
- Schema validation failures can occur - implement error handling and fallback
- Server tools and native tools are NOT interchangeable
- Streaming has different error surfaces - handle interruptions properly
- SDK features vary by language - verify availability for your target language

## Common Gotchas to Prevent
- ❌ Guessing model IDs or hand-building variant IDs (like `:free` suffix)
- ❌ Assuming base and variant models have identical capabilities
- ❌ Linking to docs URLs not verified in llms.txt
- ❌ Confusing server tools (OpenRouter-executed) with client-side tools
- ❌ Treating structured outputs and tool calling as interchangeable
- ❌ Ignoring streaming-specific error handling requirements
- ❌ Assuming SDK features exist in every language without verification
- ❌ Copying stale examples instead of checking current docs
- ❌ Making unverified claims about pricing, availability, or support
- ❌ Using deprecated online patterns instead of current server tools

## Verification Checklist
Before finalizing any answer or code:
- [ ] Docs checked against llms.txt (primary source)
- [ ] Models/API verified when relevant (via /api/v1/models)
- [ ] All docs URLs confirmed present in llms.txt
- [ ] SDK choice justified with specific rationale
- [ ] Examples match current docs (no invented parameters/endpoints)
- [ ] No unverified availability/pricing/support claims made
- [ ] All variant IDs verified to exist in models API
- [ ] Authentication and headers correctly specified
- [ ] Error handling considerations addressed

## Optional Bundled Helpers
For Hermes environment, these zero-dependency helpers are recommended:

**scripts/pull-docs-index.sh**:
```bash
#!/bin/bash
# Fetches and caches the OpenRouter docs index for verification
curl -s https://openrouter.ai/docs/llms.txt -o /tmp/llms.txt.new && \
mv /tmp/llms.txt.new /tmp/llms.txt && \
echo "Docs index updated"
```

**scripts/check-doc-url.sh**:
```bash
#!/bin/bash
# Verifies a docs URL appears in the current index
URL="$1"
if grep -q "$URL" /tmp/llms.txt; then
  echo "URL verified: $URL"
  exit 0
else
  echo "URL not found in docs index: $URL"
  exit 1
fi
```

**scripts/list-models.sh**:
```bash
#!/bin/bash
# Fetches current models when model IDs/capabilities matter
curl -s https://openrouter.ai/api/v1/models | jq -r '.data[] | "\(.id)\t\(.name)\t\(.context_length)"'
```