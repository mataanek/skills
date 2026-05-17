# FreshRSS News Digest

This skill turns FreshRSS unread items into a themed digest for Hermes. It separates content collection, digest generation, delivery cadence, and critical alerts so the system stays fresh without becoming noisy.

## Purpose

The digest is designed to read like a short morning brief rather than a ranked list of links. Articles are treated as source material, grouped into themes, and surfaced in a compact editorial format.

## Operating Model

Use separate cadences for ingestion and delivery:

- Poll FreshRSS frequently enough to keep candidate items current, for example every 30 to 60 minutes.
- Generate and deliver the full themed digest twice per day.
- Send an out-of-band alert only when a genuinely critical story appears.

This keeps the digest fresh while avoiding chat spam.

## Recommended Delivery Schedule

A good default is two digest drops per day:

- Morning digest: around the start of the workday.
- Evening digest: later in the day as a second pass.

The exact times should be configured in runtime config, not hardcoded into the skill.

## Critical Alerts

Critical alerts are separate from the normal digest.

Use them only for stories that are both urgent and likely to matter immediately, for example:
- major security incidents or active exploitation,
- major infrastructure outages,
- highly consequential AI or policy developments that need rapid attention.

A critical alert should contain:
- a clear urgent marker,
- one short explanation of what happened,
- one short line on why it matters now,
- the source article reference or link.

Do not wait for the next scheduled digest when the item is clearly urgent.

## Runtime Configuration

Keep environment-specific choices outside the skill itself:

- FreshRSS endpoint and credentials,
- primary and fallback LLM provider settings,
- polling cadence,
- digest delivery times,
- alert transport and routing rules.

The skill defines the workflow. Runtime config defines when and where it runs.

## Suggested Cron Strategy

Example pattern:

- frequent lightweight polling job to refresh unread candidates,
- twice-daily digest job,
- event or rule-based critical alert path.

The implementation can be cron, a scheduler service, or Hermes-native automation. The important part is that collection cadence is faster than digest delivery cadence.

## Model Policy

Use the configured primary model by default. That model may be an API cloud model or a local model.

Recommended policy:
- primary model: best available general summarization model,
- fallback model: secondary configured model if the primary fails,
- parsing fallback: simpler prompt if structured JSON output fails.

Do not hardcode a local endpoint as the only supported path.

## Save Behavior

Saving to wiki should remain explicitly user-triggered.

Recommended commands:
- `save <numbers>` to store selected source items as notes,
- `expand <numbers>` to inspect selected source items without saving.

Saved notes should contain item-specific summaries, not the whole digest.
