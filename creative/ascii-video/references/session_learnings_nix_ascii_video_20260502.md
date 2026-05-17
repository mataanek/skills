# Session Learnings: Nix ASCII Video Generation (2026-05-02)

## User Preference: Facts-only Output
When the user explicitly requests only facts and commands with no narrative, the agent must:
- Suppress all explanatory text, commentary, and motivational language.
- Output only the essential commands and their direct results (exit codes, output snippets).
- Avoid any narrative framing, even if the task is complex.
- If clarification is needed, ask short, direct questions.

## Pitfall: Custom Script Generation
Attempting to run custom ASCII generator scripts (e.g., ascii.video.23.py) outside the skill's established pipeline often results in:
- Timeouts due to unoptimized particle counts or missing ffmpeg pipe handling.
- Missing dependencies or incorrect environment assumptions.
- Failure to meet user expectations for text overlay timing and screen utilization.
**Correct approach:** Use the skill's workflow: build upon reference implementations, test single frames first, and adjust parameters within the provided script templates.

## Text Overlay Timing Verification
Ensure message visibility functions use correct piecewise logic with fade-in/fade-out ramps (typically 1 second each). Verify against RMS-dip boundaries or user-provided timestamps to prevent premature appearance or lingering text.

## Particle System Screen Utilization
For full-screen ASCII rain:
- Spawn particles with sufficient initial vertical range (cover full height) and base speed to traverse viewport within the clip duration.
- Balance max_particles, spawn_rate, and max_age to avoid timeouts while achieving desired density.
- Test a few frames to confirm particles reach the bottom before adjusting counts.

## Workspace Preference
All output videos should be saved to `/home/mataanek/.hermes/workspace/` unless otherwise specified. Use this path explicitly in scripts to avoid confusion.