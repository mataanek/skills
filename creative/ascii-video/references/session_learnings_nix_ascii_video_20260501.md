# Session Learnings: Nix ASCII Video Generation (2026-05-01)

This document captures key lessons learned from the user's session on 2026-05-01 regarding ASCII video generation with audio-reactive rain and timed text overlay.

## Key Corrections from User Feedback

### 1. Workspace Preference
- The user expects scripts and output to be placed in the Hermes-configured workspace: `/home/mataanek/.hermes/workspace/`.
- Writing to `/home/mataanek/workspace/` (the agent's active workspace) caused confusion and was not preferred.
- **Always verify the output path using `hermes config get` or check the user's explicit instruction.**

### 2. Text Overlay Timing
- In initial attempts, the first text message did not appear until ~8-9 seconds into the video, despite being scheduled for 0-9.5s.
- Root cause: The visibility calculation used `max(fade_in, fade_out)` which delayed the onset of full visibility.
- **Fix:** Use a piecewise visibility function that ramps up from 0 to 1 over the first second, holds at 1, then ramps down to 0 over the last second.
  - For a message active from `t_start` to `t_end`:
    - `t_in = current_time - t_start`
    - `t_out = t_end - current_time`
    - `fade_in = min(1.0, max(0.0, t_in / 1.0))`
    - `fade_out = min(1.0, max(0.0, t_out / 1.0))`
    - `visibility = min(fade_in, fade_out)`  # This yields 0 -> 1 -> 0 profile

### 3. Screen Utilization (Vertical Fill)
- Early versions only populated the top 25% of the screen with ASCII rain, leaving 75% empty.
- Root causes:
  - Insufficient particle spawn rate.
  - Particle lifetime too short to traverse the full screen height.
  - Initial particle Y-position too close to the top (not starting far enough above the screen).
- **Fixes:**
  - Increase spawn rate coefficients (e.g., `spawn_rate = 0.25 + 3.5 * bass + 4.0 * flux`).
  - Increase particle `max_age` to allow longer traversal (e.g., 90-150 frames).
  - Start particles well above the screen: `y = -font_size * random.uniform(0.5, 2.0)`.
  - Ensure particle speed is sufficient to cross the screen within its lifetime.

### 4. Script Generation Pitfall: Escaped Newlines
- When using the `write_file` tool to save long Python scripts, newline characters (`\n`) were sometimes written as literal escape sequences instead of actual line breaks.
- This resulted in `SyntaxError: expected 'except' or 'finally' block` because the entire script was on one line.
- **Mitigation:** After writing a script, verify its integrity with `head -n 5` and `cat -A` to check for escaped newlines (`\\n`). If found, rewrite the script using a method that preserves true newlines (e.g., write line-by-line or use a heredoc).

## Verification Steps for Future Sessions

1. **Path Check:** Confirm output directory matches `/home/mataanek/.hermes/workspace/` unless otherwise instructed.
2. **Frame Sampling:** Render and inspect a few key frames (t=0s, t=10s, t=30s) to verify:
   - Text appears immediately at t=0 for the first message.
   - ASCII particles fill the entire vertical extent of the screen.
   - No visual artifacts from script formatting errors.
3. **Script Health:** Before execution, run `python3 -m py_compile <script.py>` to catch syntax errors early.
