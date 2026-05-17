---
name: user-stories-analysis
description: Analyze user stories documentation to extract and prioritize implementation items.
category: research
version: 1.0
---

# User Stories Analysis Skill

## Purpose
Provides a repeatable method to review user stories (e.g., from a product docs page) and identify top 3 priorities for implementation.

## When to Use
- User asks for prioritization from a user stories list or roadmap.
- Need to communicate what to work on next based on documented user needs.

## Steps
1. Retrieve the user stories document (via provided URL or copy-paste).
2. Identify each user story and note its stated goal, user role, and any impact/effort hints.
3. Score each story on:
   - Impact (user value, alignment with product vision) – 1-5
   - Effort (estimated complexity) – 1-5 (lower is easier)
   - Strategic fit (how it advances core agent capabilities) – 1-5
4. Compute a priority score: (Impact * Strategic fit) / Effort (or similar weighting).
5. Rank stories by score, pick top 3.
6. For each, provide a concise rationale referencing the scores.

## Output Format
- List top 3 priorities.
- For each: short description, reasoning (impact/effort/fit), and suggested next step.

## Pitfalls
- Missing explicit impact/effort data: infer from wording; flag assumptions.
- Overlooking non-functional stories (tech debt, refactoring): treat them separately if needed.
- Bias toward recent stories: ensure balanced review.

## Verification
- Cross-check that selected stories address distinct areas (avoid duplication).
- Ensure reasoning is transparent and based on documented cues.

## References
- references/prioritization_framework.md (optional)