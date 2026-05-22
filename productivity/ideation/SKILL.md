---
name: ideation
description: Generate ideation files from sources (tweets, articles, notes) by expanding points, adding ways to implement, options, high-level plans, alternatives, etc.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: ideation, planning, wiki, documentation
    relatedskills: note-taking, research
---

# Ideation Skill

This skill provides a structured approach to turning raw input (e.g., a tweet, article snippet, or note) into a detailed ideation file suitable for a wiki or knowledge base.

## When to Use

- User shares a tweet, article, or note containing key points or principles.
- User asks to "study this and start new ideation wiki file" or similar.
- User wants to expand brief concepts into actionable plans with implementation ways, options, high-level plans, and alternatives.

## Workflow

### Step 1 — Capture the Source

Record the source URL or text. If it's a tweet, fetch the full thread if needed (use `web_extract` or manual copy).

### Step 2 — Extract Core Points

Identify the numbered or bulleted principles, steps, or facts. Preserve the original wording as blockquotes.

### Step 3 — Create Initial Ideation File

Write a markdown file with:
- Source citation
- Core Insight (if present)
- The extracted points as blockquotes

Save to an appropriate location under `~/.hermes/wiki/ideation/` (or as directed).

### Step 4 — Expand Each Point

For each point, add sections:
- **Ways to Implement**: concrete methods, tools, or practices.
- **Options**: specific products, services, or configurations that realize the ways.
- **High‑level Plan**: timeline or phases (e.g., Month 1, Sprint 1) to adopt the options.
- **Alternatives**: other approaches if the primary options are unsuitable.

Use a consistent template for each point.

### Step 5 — Add Related Notes and Next Steps

Link to existing ideation files or wiki notes that are related.

List concrete next steps (e.g., review with team, draft checklist, propose pilot).

### Step 6 — Validate and Link

Ensure the file is correctly formatted, links work, and it is discoverable (e.g., added to a wiki index if needed).

## Pitfalls

- Do not lose the original source; always cite it.
- Avoid adding fluff; keep each expansion practical and tied to the point.
- If the source already contains expansions, focus on adding missing dimensions (e.g., alternatives, plans) rather than repeating.
- When linking related notes, verify the target exists.
- Do not feel obligated to create only one ideation file per source. If the source contains multiple distinct points that would benefit from separate expansion, create multiple files.
- Do not create an ideation file for a tool or service if the user explicitly states they already have a basic version or implementation, unless they ask for an advanced or alternative approach.

## Templates

See `references/ideation-template.md` for a starter file.

## Example

See the session log for how a tweet about agentic systems foundations was turned into `/home/mataanek/.hermes/wiki/ideation/foundation-five-points.md`.

---
## Reference: Ideation Template

```markdown
# Ideation: [Topic]

**Source:** [URL or description]

**Core Insight:**
[One‑sentence summary of the main takeaway]

## The [Number] Points

> 1. [First point]
> 2. [Second point]
> ...

## Ways to Implement & Options

### 1. [First Point]
- *Ways:* [list of methods]
- *Options:* [specific choices]
- *High‑level Plan:* [timeline or phases]
- *Alternatives:* [other approaches]

# (Repeat for each point)

## Related Notes

- Link to existing ideation/wiki files

## Next Steps

1. [Action]
2. [Action]
3. [Action]

```