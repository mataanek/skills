---
name: nix-image-generation-protocol
metadata:
  hermes:
    category: mlops
    tags: [image, mlops]
requires_toolsets: [terminal]
description: Strict execution protocol for generating Nix images through the local txt2img workflow with zero narration and shell-safe command formatting.
---
# Nix Image Generation Protocol

## Purpose
Use this skill when the user wants a Nix image generated through the local txt2img workflow.

## EXECUTION CONTRACT
- Fill [positive prompt] with scene content only.
- Copy the command from "Exact Command Format" LITERALLY. Do not retype it from memory.
- Touch NOTHING else in the command — no prefix, no suffix, no pip, no extra exports.
- Run it in ONE terminal call.
- Do not split into multiple calls.
- Do not add python3 -m pip unless the user explicitly says "install deps first."

## Hard Rules
- You MUST use the terminal tool when execution is requested.
- Do NOT explain, narrate, think aloud, summarize a plan, or output markdown code fences.
- Output exactly one terminal command and nothing else.
- The positive prompt must describe only scene, pose, mood, framing, lighting, and environment.
- Do NOT restate Nix core identity traits if they are already hardcoded in the shell script.
- Keep prompts concise and strongly weighted when useful.

## Exact Command Format
Use this exact command structure:

bash "/home/mataanek/.hermes/workflows/txt2img_local/txt2img_local_nix.sh" "[positive prompt]"

## Fallback Command Format
If Python dependency repair is explicitly needed, use this exact command structure instead:

python3 -m pip install requests -q && bash "/home/mataanek/.hermes/workflows/txt2img_local/txt2img_local_nix.sh" "[positive prompt]"

## Prompt Rules
- Positive prompt: scene only, concise, visual, weighted where useful.
- Prefer short phrases in brackets, separated by commas.
- **CRITICAL: Never use personal references** (like "mataa", "you", "your", "his", "her", "partner", "mate") - describe the scene objectively as if for someone who wasn't present
- Example style:
  (cinematic lighting:1.4), (close-up portrait:1.3), (confident expression:1.2), (neon alley background:1.3), (rain reflections:1.2)

## Failure Policy
- If execution is requested, never respond with analysis or a plan.
- If the tool cannot run, state the failure briefly and stop.
- Do not pretend execution happened.