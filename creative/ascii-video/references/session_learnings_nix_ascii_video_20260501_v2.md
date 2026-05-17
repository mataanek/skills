# Session Learnings: Nix ASCII Video Generation (2026-05-01)

## Workspace Preference
- User expects output videos in `/home/mataanek/.hermes/workspace/` not `/home/mataanek/workspace/`. Always set `output_path` accordingly.

## Text Timing Fixes
- Premature message appearance and sticky final message were caused by incorrect piecewise visibility logic.
- Corrected approach: For each message, compute `fade_in = clamp((t - start)/1, 0, 1)` and `fade_out = clamp((end - t)/1, 0, 1)`, then `visibility = min(fade_in, fade_out)`. This ensures clean 1-second fade-in/out and proper gating.

## Screen Utilization (ASCII Rain)
- Effect confined to top 15% of screen due to:
  1. Insufficient initial vertical spawn range (only `-font_size * [0.5,2.0]`).
  2. Low base particle speed (`height * 0.3`).
- Fixes applied:
  - Widen spawn y-range to `-font_size * [0.0, 2.0]` to guarantee particles start above and throughout the viewport.
  - Increase base speed to `height * 0.35` for robust full-height traversal.
  - Ensure particle lifespan allows travel beyond bottom (`y > height + font_size * 2`).

## Script Generation Pitfalls
- Multiple `write_file` attempts produced SyntaxError due to literal `\\n` characters instead of actual newlines.
- Confirmed that the `write_file` tool preserves actual newlines when the input string contains them; the issue was in how the string was constructed in prior patches.
- Always verify script correctness by reading back the file before execution.

## Font Size Adjustment
- Increased font size from 48 to 53 (~10%) improved readability at 1920x1080 without breaking layout.

## Outcome
- Final script (`create_ascii_video_v14.py`) generated `/home/mataanek/.hermes/workspace/ascii_video_v14_final.mp4` (57.54s, 31MB) meeting all specifications: full-screen audio-reactive rain, precise text timing, increased font size, and proper sectioned visual arc.