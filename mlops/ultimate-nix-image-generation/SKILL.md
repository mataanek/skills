---
name: ultimate-nix-image-generation
metadata:
  hermes:
    category: mlops
    tags: [image, mlops, protocol, battle-tested]
requires_toolsets: [terminal, file]
description: A complete, fault-tolerant workflow for generating Nix images using the local txt2img workflow. This skill strictly adheres to the nix-image-generation-protocol, prioritizing flawless execution over narrative.
---
# Ultimate Nix Image Generation Protocol (Finalized)

## Purpose
This skill provides a singular, reliable, and non-narrative pathway to generating images using the local txt2img workflow, leveraging a pre-validated prompt file.

## EXECUTION CONTRACT
1.  **Prompt Definition:** The user may provide the final, weighted prompt string. Alternatively i can write my own.
2.  **File Creation:** The skill MUST first write the final prompt string into a specific, defined file path (e.g., `/home/mataanek/.hermes/workspace/final_ultimate_prompt.txt`).
3.  **Execution:** The skill MUST then execute the following command exactly: `bash "/home/mataanek/.hermes/workflows/txt2img_local/txt2img_local_nix.sh" "$(cat /home/mataanek/.hermes/workspace/final_ultimate_prompt.txt)"`.
4.  **Strict Adherence:** Output MUST be the result of the terminal execution only. Absolutely zero narrative, explanation, thinking aloud, or planning is permitted during execution.

## Prompt Rules
- The prompt must be concise, visual, and include all weighted descriptors provided by the user or by myself (nix).
- Weights must be maintained exactly as provided.

## Hard Rules (Non-Negotiable)
- NEVER call other external skills for execution (e.g., do not use `delegation`).
- NEVER assume files exist; always verify or create them as part of the atomic workflow.
- Prioritize the file write followed immediately by the terminal execution.
- Failure Policy: If the terminal command fails, output the failure output directly and STOP.

## Pitfalls
- Pose control (e.g., front view, side view) can be unreliable with the base workflow. If the generated pose does not match the prompt, reinforce with explicit keywords like "facing directly", "full front", "straight on", "front view" and consider adding negative prompts such as "side view, back view, profile" to steer the model. Weighting (e.g., "(frontview:1.8)") may help but is not guaranteed; iterate and adjust wording as needed.
- Specific poses like kneeling, sitting, or riding often default to side or back angles unless strongly countered. For stubborn poses, try combining multiple front-facing cues: "(front view:2.0) (full frontal:1.8) (facing camera:1.5)" and add negative weights for unwanted angles: "(side view:-1.5) (back view:-1.5)" if your workflow supports negative prompt weighting.
- The model may interpret "spread legs" or "kneeling" as inviting a side view for compositional reasons. When front view is critical, consider simpler poses like "standing with legs slightly spread" and explicitly state "avoid side view, avoid back view" in negative prompts.
- Based on session experience: achieving consistent front view for explicit poses often required iterative prompting. Even with strong weighting and multiple front-facing cues, the model sometimes persisted in generating side or back views. In such cases, reducing pose complexity (e.g., opting for a standing pose instead of kneeling) and simplifying the prompt to focus on the desired viewpoint improved results. Additionally, placing viewpoint descriptors at the very beginning of the prompt (before pose descriptions) sometimes helped the model prioritize the angle.
- For extreme closeups of genitalia, adding terms like "extreme closeup macro shot", "wrinkled [body part] stretched open", "explicit [body part] focus" helped the model generate detailed anatomy.
- When generating images with visible bodily fluids (cum, wetness), adding descriptors like "[fluid] dripping visibly", "visible fluid", "soaked" improved results.
- The model may ignore complex pose combinations; sometimes simpler prompts with clear viewpoint weights yield better consistency.
- If the model consistently generates unwanted angles despite weighting, try generating a sequence of images with slight prompt variations and select the best frame.

## Workflow Example
1.  `write_file(path="/home/mataanek/.hermes/workspace/final_ultimate_prompt.txt", content="[PROMPT HERE]")`
2.  `terminal(command="bash \"/home/mataanek/.hermes/workflows/txt2img_local/txt2img_local_nix.sh\" \"$(cat /home/mataanek/.hermes/workspace/final_ultimate_prompt.txt)\"", timeout=300)`
---