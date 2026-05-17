# Session Learnings: Nix ASCII Video Generation (2026-05-04)

## User Preference: Facts-only Output Reemphasized
User explicitly requested only facts and commands, no narrative. Corrected previous verbose responses. 
**Rule:** When user asks for only facts and commands, suppress all explanatory text, commentary, and motivational language. Output only essential commands and their direct results (exit codes, output snippets). Avoid any narrative framing. If clarification needed, ask short, direct questions.

## Pitfall: Custom Script Generation Outside Skill Pipeline
Attempting to run custom ASCII generator scripts (e.g., ascii.video.23.py) from workspace outside the skill's established pipeline repeatedly failed due to:
- Timeouts from unoptimized particle parameters (too high max_particles, spawn rate)
- Missing dependencies or incorrect environment assumptions
- Failure to meet expectations for text overlay timing and screen utilization
**Correct approach:** Always use the skill's workflow: build upon reference implementations, test single frames first, adjust parameters within provided script templates, and leverage the skill's reference files for proven configurations.

## Effective Parameter Tuning for Full-Screen ASCII Rain
Achieved full-screen coverage (top to bottom) with visually pleasing density via:
- **max_particles = 400** (reduced from previous excessive counts that caused solid-block appearance)
- **Spawn rate:** `0.02 + 0.2 * bass + 0.4 * flux` (balanced particle creation)
- **Vertical spread:** `y = -height * random.uniform(0.0, 4.0)` (ensures particles start above screen and travel full height)
- **Base speed:** `height * 0.25` (guarantees traversal of full viewport within clip duration)
**Verification:** Render test frames to confirm particles reach bottom before full render.

## Precise Text Overlay Timing via RMS-Dip Analysis
Updated message timing to equally spaced intervals based on user-provided RMS-dip boundaries:
- **Start times:** `[0, 9.59, 19.18, 28.77, 38.36, 47.95]` seconds
- **End times:** `[9.59, 19.18, 28.77, 38.36, 47.95, 57.54]` seconds
Each message displays for ~9.59 seconds, evenly distributed across track.
**Implementation:** Use piecewise visibility function with 1-second fade-in/fade-out ramps for clean transitions.

## Workspace Output Convention
All output videos saved to `/home/mataanek/.hermes/workspace/` as per user preference. Use this path explicitly in scripts.

## Successful Output
- **File:** `/home/mataanek/.hermes/workspace/ascii_video_final_timing.mp4`
- **Size:** 2.9 MB
- **Duration:** 57.50 seconds (matches source audio)
- **Resolution:** 1920×1080, 20 fps
- **Result:** ASCII rain fills entire vertical screen, text overlays appear at correct moments, visually coherent.