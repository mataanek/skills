# Agentic Systems Foundation (Five Points)

Source: User-provided agentic systems foundation points.

## The Five Points
1. **Tailscale** – private mesh network across all machines; prerequisite for other steps.
2. **Termius** over the tailnet – one SSH client reaching every node, phone included.
3. **tmux** – persistent sessions; survive disconnects; essential for long agentic work.
4. **Private Git repo** – memory layer across agents; pull/work/push; preserves context.
5. **Script everything from day one** – automate repetitive tasks; if done twice, script it.

## The Habit
Ask the AI itself for config, errors, guidance; let the agent do the lifting, then verify.

## Implementation Notes
- Mesh network enables secure zero‑config reachability.
- SSH client should sync hosts and work on mobile.
- Use tmux with resurrect for session persistence.
- Treat Git repo as source of truth; automate pull on start, push on finish.
- Script SSH aliases, setup scripts, and boilerplate.
- Leverage the agent to suggest commands, scripts, fixes; review output.
