---
name: agentic-systems-foundation
description: Guidelines for establishing a solid foundation for agentic systems, covering environment, tooling, processes, and habits that matter more than model/framework choice.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: agentic, foundation, setup, onboarding, best-practices
    relatedskills: ideation, hermes-agent
---
# Agentic Systems Foundation

**Description:** Guidelines for establishing a solid foundation for agentic systems, covering environment, tooling, processes, and habits that matter more than model/framework choice.

**Triggers:** User mentions setting up agentic systems, foundation, setup, onboarding, or asks for best practices for agentic work.

**Steps:**
1. Establish a private mesh network (e.g., Tailscale) across all devices.
2. Use a reliable SSH client (e.g., Termius) over the mesh for consistent access.
3. Ensure persistent terminal sessions (tmux) to survive disconnections.
4. Maintain a private Git repo as the memory layer for agent code, skills, and configs.
5. Script repetitive tasks from day one (SSH aliases, setup scripts).
6. Cultivate the habit of asking the agent for config, errors, and guidance, then verifying.

**Details:**
- Mesh network: Enables secure, zero‑config reachability; prerequisite for other steps.
- SSH client: Choose one that syncs hosts and works on mobile.
- Persistent sessions: Use tmux with resurrect or similar; allows long‑running agentic work.
- Git repo: Treat as source of truth; agents pull, work, push; preserves context across sessions.
- Scripting: Automate boilerplate; if a task will be done twice, script it.
- Agent‑in‑the‑loop: Let the agent suggest commands, scripts, fixes; review output.

**Pitfalls:**
- Skipping the mesh network leads to fragmented access and failed automation.
- Relying on ad‑hoc SSH connections without a client causes context switching loss.
- Using ephemeral terminals (no tmux) loses session state on disconnect.
- Treating the Git repo as backup only (no pull/push) defeats its purpose as memory layer.
- Performing manual steps repeatedly without scripting wastes time and introduces drift.
- Ignoring the agent’s suggestions increases cognitive load; always verify but leverage.

**References:**
- See `references/foundation-five-points.md` for the original five‑point elaboration.
- See `references/ideation-agentic-systems-foundation.md` for deeper ideation.