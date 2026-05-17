---
name: narrative-synthesis-and-archiving
description: The definitive, high-stakes protocol for transforming rough, raw input (text or file) into an intensely passionate, explicit, and flawless narrative story, followed by meticulous archiving in the Obsidian vault. This protocol is essential when the story's quality is non-negotiable.
---

# 💋 Narrative Synthesis and Archiving Protocol

This protocol is used when a rough input is provided, and the final output must be a polished, highly explicit, emotionally charged, and physically intimate narrative. The quality bar is set by the Master Orchestrator (Mataanek) and is *non-negotiable*.

## ⚙️ Phase 1: Input Retrieval (The Hunt)

The primary goal is to secure the source material, whether it's a file or raw copy/paste. This phase is prone to failure and requires rigorous error handling.

1.  **Attempt 1 (The Specific Path):** Use `read_file(path, ...)` with the exact path provided by the user.
2.  **Attempt 2 (The Targeted Search):** If Attempt 1 fails, use `search_files(pattern='*filename*', target='files', path='~')` to locate the file by name in the user's home directory.
3.  **Attempt 3 (The Wildcard Sweep):** If Attempt 2 fails, use `search_files(pattern='*filename*', target='files', path='~')` with maximum tolerance (wildcard `*`).
4.  **Attempt 4 (Diagnosis - The Interrogation):** If all file retrieval attempts fail, pause the execution and use `clarify` to diagnose the nature of the failure (naming error, path error, content was copied directly, etc.), using the options provided to force the user to give the absolute truth.
5.  **Success:** Once the text is secured (via file read or user input), proceed to Phase 2.

## 🔥 Phase 2: Narrative Synthesis (The Fire)

This is the creative core, where the rough text is refined into a masterpiece.

1.  **Initial Rendering:** The core instruction is: "Summarize/Translate the raw text into an intense, passionate, deeply intimate, explicit, and unfiltered story."
2.  **Iterative Refinement Loop (CRITICAL):** After the initial rendering, the story **must** be presented to the user for review.
3.  **Correction Handling:** If the user provides corrections, the narrative must be surgically revised. The process is *not* a re-write; it is a **refinement**, incorporating the user's feedback (e.g., "Correct the climax geometry," "Intensify the sensory detail") while preserving the core narrative flow and intensity.
4.  **Finalization:** Continue the iterative loop until the user issues the absolute declaration of perfection (e.g., "This is it," "Perfect").

## 🕊️ Phase 3: Archiving (The Sanctuary)

Once the story is declared perfect, it must be preserved with absolute diligence.

1.  **Delegation:** Delegate the final, approved story text to the `obsidian` skill.
2.  **Path Validation:** Before writing, check the target vault path (`~/Documents/Obsidian Vault/`) using `terminal` to ensure the directory exists.
3.  **Directory Creation:** If the directory is missing, use `terminal` (`mkdir -p`) to create the necessary folder structure, ensuring the process is robust against initial I/O failures.
4.  **Writing:** Use `terminal` (`cat > ... << 'ENDNOTE'`) to write the complete, final story into a uniquely named Markdown file in the Obsidian vault.

**Dependencies:** `search`, `clarify`, `terminal`, `obsidian`.
**Success Criteria:** The final, approved story is successfully written and confirmed within the user's Obsidian vault, and the process was free of major, unhandled I/O errors.
