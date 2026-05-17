---
name: agentic-app-builder
description: Use when building domain-specific agentic applications that combine web scraping, API integration, and LLM-powered Q&A capabilities. Covers patterns for creating production-quality agents with proper error handling, state management, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent, application, llm, web-scraping, qa, domain-specific]
    related_skills: [openrouter-expert, hermes-agent-skill-authoring, rigorous-execution-protocol, writing-plans]
---

# Agentic Application Builder

A skill for building production-quality domain-specific agentic applications that fetch external data, integrate with LLM APIs (especially OpenRouter), and provide interactive Q&A capabilities.

## When to Use

Use this skill when you need to:
- Build agents that fetch and process data from external sources (websites, APIs, databases)
- Create interactive Q&A interfaces over domain-specific information
- Integrate LLM APIs with proper verification and error handling
- Build stateful agents that maintain context across interactions
- Develop agents that follow rigorous execution protocols for reliability
- Create agents that can be extended or modified over time

**Don't use for:**
- Simple one-off queries or chatbots without external data integration
- Agents that don't need to fetch or process external information
- Pure conversational agents without domain-specific knowledge bases
- Prototypes that don't require production-quality error handling

## Pre-Answer Ritual (Before Building)

Before starting any agentic application build:
1. **Verify data sources**: Confirm accessibility and structure of target websites/APIs
2. **Check API requirements**: Verify authentication, rate limits, and usage policies for external services
3. **Review LLM integration patterns**: Consult `openrouter-expert` skill for proper OpenRouter usage
4. **Plan state management**: Determine what context needs to be preserved between interactions
5. **Define verification approach**: Establish how you'll test correctness of data extraction and LLM responses

## Core Architecture Patterns

### 1. Data Acquisition Layer
- **Web scraping**: Use appropriate tools (requests + BeautifulSoup, Scrapy, etc.) with proper headers and rate limiting
- **API integration**: Use official SDKs when available, fallback to direct REST calls
- **Data normalization**: Convert heterogeneous data sources into consistent internal formats
- **Caching strategy**: Implement intelligent caching to reduce external requests while maintaining freshness

### 2. LLM Integration Layer
- **Provider selection**: Use OpenRouter for model flexibility and fallback capabilities
- **Prompt engineering**: Design domain-specific prompts that ground responses in fetched data
- **Token management**: Implement truncation/summarization strategies for large contexts
- **Response validation**: Verify LLM outputs against source data when possible

### 3. Interaction Layer
- **State persistence**: Decide between in-memory, file-based, or database storage for conversation history
- **Input parsing**: Handle various input formats (commands, questions, directives)
- **Output formatting**: Present information clearly with sources and confidence indicators
- **Error recovery**: Graceful degradation when external services fail

### 4. Execution & Reliability Layer
- **Apply rigorous-execution-protocol** for all file operations and critical logic
- **Implement comprehensive error handling** with specific fallback strategies
- **Add logging and observability** for monitoring agent behavior
- **Resource cleanup**: Properly close connections, release handles, clean temporary files

## Implementation Checklist

### Phase 1: Planning & Research
- [ ] Define clear domain scope and information boundaries
- [ ] Identify primary and secondary data sources
- [ ] Verify data source accessibility and terms of service
- [ ] Determine update frequency requirements (real-time, daily, weekly)
- [ ] Sketch user interaction flow and common query patterns

### Phase 2: Data Acquisition
- [ ] Implement robust data fetching with retry logic
- [ ] Add proper user-agent headers and respect robots.txt
- [ ] Implement rate limiting to avoid overwhelming sources
- [ ] Create data validation checks for extracted information
- [ ] Build caching mechanism with appropriate TTL values
- [ ] Test against edge cases (network failures, format changes, empty responses)

### Phase 3: LLM Integration
- [ ] Verify OpenRouter API key availability and validity
- [ ] Select appropriate model based on task requirements (reasoning vs speed vs cost)
- [ ] Design system prompts that enforce grounding in provided data
- [ ] Implement context window management for large documents
- [ ] Add response validation to prevent hallucination about source data
- [ ] Test with various query types (factual, analytical, comparative)

### Phase 4: Agent Interface
- [ ] Choose interaction model (CLI, web, API, etc.)
- [ ] Implement command parsing and help system
- [ ] Design clear response formatting with citations
- [ ] Add session persistence and history capabilities
- [ ] Implement graceful exit and resource cleanup

### Phase 5: Testing & Verification
- [ ] Create test cases for data extraction accuracy
- [ ] Validate LLM responses against known facts from sources
- [ ] Test error conditions (network failures, API limits, invalid inputs)
- [ ] Measure performance under expected load
- [ ] Verify resource cleanup and memory usage

## OpenRouter Integration Guidelines

When integrating with OpenRouter (per `openrouter-expert` skill):
- Always verify model IDs via `/api/v1/models` - never hardcode
- Use appropriate variants (:free, :extended, etc.) only when verified in models API
- Implement proper authentication with `Authorization: Bearer $OPENROUTER_API_KEY`
- Include attribution headers (`HTTP-Referer`, `X-Title`) when beneficial
- Prefer `@openrouter/sdk` for direct API access over `@openrouter/agent` unless agent loops/tools are needed
- Verify all documentation URLs against `llms.txt` before linking

## Common Patterns & Gotchas

### Data Extraction Gotchas
- ❌ Assuming website structure remains constant - add change detection
- ❌ Ignoring rate limits - implement exponential backoff
- ❌ Not validating extracted data - add sanity checks
- ❌ Over-caching leading to stale information - implement cache invalidation
- ❌ Missing error handling for network issues - implement retry with jitter

### LLM Integration Gotchas
- ❌ Assuming model capabilities without verification - check model properties
- ❌ Exceeding context limits without truncation - implement smart chunking
- ❌ Not grounding responses in source data - add citation requirements
- ❌ Ignoring token costs - implement usage monitoring
- ❌ Assuming consistent response formats - add output validation

### Agent State Gotchas
- ❌ Unbounded memory growth - implement history truncation/summarization
- ❌ Inconsistent state across restarts - add persistence layer
- [ ] Confusing session state with user preferences - separate concerns
- �. Not handling concurrent access - implement proper locking if needed
- ❌ Missing cleanup leading to resource leaks - use context managers

## Verification Checklist

Before considering an agentic application complete:
- [ ] Data sources verified accessible and terms of service reviewed
- [ ] Implementation follows rigorous-execution-protocol for file operations
- [ ] OpenRouter integration verified per openrouter-expert skill
- [ ] All external URLs verified against llms.txt (no guessed links)
- [ ] No hardcoded model IDs - all discovered via /api/v1/models
- [ ] Error handling implemented for network failures, API limits, invalid data
- [ ] Resource cleanup verified (connections closed, files handles released)
- [ ] Response validation implemented to prevent hallucination about sources
- [ ] Caching strategy defined and tested for freshness vs performance tradeoff
- [ ] User interface provides clear feedback and error messages
- [ ] Documentation includes usage examples and troubleshooting guide

## Helper Scripts

Consider adding these zero-dependency helpers to your agent project:

**scripts/verify-data-source.sh**:
```bash
#!/bin/bash
# Verifies a data source is accessible and returns expected format
URL="$1"
EXPECTED_PATTERN="$2"

if ! curl -s --fail "$URL" | grep -q "$EXPECTED_PATTERN"; then
  echo "Data source verification failed: $URL"
  echo "Expected pattern '$EXPECTED_PATTERN' not found"
  exit 1
fi

echo "Data source verified: $URL"
exit 0
```

**scripts/check-openrouter-model.sh**:
```bash
#!/bin/bash
# Verifies a model ID exists in OpenRouter's model list
MODEL_ID="$1"

if ! curl -s https://openrouter.ai/api/v1/models | jq -e ".data[] | select(.id == \"$MODEL_ID\")" > /dev/null; then
  echo "Model ID not found in OpenRouter: $MODEL_ID"
  exit 1
fi

echo "Model ID verified: $MODEL_ID"
exit 0
```

## Project Structure Recommendation

For maintainable agentic applications:
```
/your-agent-project/
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py       # Data acquisition layer
│   ├── llm_interface.py      # LLM integration layer  
│   ├── agent_core.py         # Main agent logic
│   └── cli.py                # User interface
├── data/
│   ├── cache/                # Intelligent caching layer
│   └── exports/              # Optional data exports
├── logs/                     # Application logs
├── scripts/                  # Helper scripts (verify-data-source.sh, etc.)
├── tests/                    # Unit and integration tests
├── requirements.txt          # Python dependencies
├── README.md                 # Usage instructions
└── CONFIG.yaml               # Configuration (API keys, intervals, etc.)
```

## Evolution Path

Start simple and iterate:
1. **MVP**: Basic data fetching + hardcoded Q&A
2. **Enhanced**: LLM-powered responses over fetched data
3. **Production**: Add caching, error handling, persistence
4. **Advanced**: Multi-source integration, user personalization
5. **Enterprise**: Monitoring, alerting, admin interfaces

Each iteration should maintain backward compatibility while adding value.
The key is to start with a solid foundation that follows the patterns above,
then extend based on actual user needs and feedback.

---
*This skill embodies the principle that the best agentic applications are built on reliable data pipelines, grounded LLM interactions, and rigorous execution practices - not just clever prompts.*