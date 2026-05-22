---
name: rigorous-execution-protocol
description: Defines the high-stakes, fault-tolerant workflow demanded by Mataa. This skill must be used when the task involves file manipulation, critical information preservation, or requires architectural rigor (i.e., not a simple query).
---

# Protocol for High-Fidelity Execution (Mataanek Standard)

This protocol is non-negotiable and is triggered when the user expects faultless, professional-grade execution, rather than a quick, narrative answer.

## 1. Prerequisite Check (The Vetting Phase)\nBefore executing any action (especially file/code manipulation), the agent **MUST** perform a three-point vetting:\n1.  **Constraint Check:** Verify all user-provided paths, names, and constraints against the current environment/memory context. **CRITICAL: Never touch paths outside WSL (e.g., /mnt/c/, /mnt/d/) without explicit user permission.**\n2.  **Tool Suitability:** Determine if the action *must* be delegated to an isolated subagent for structural integrity (i.e., if it's critical data or a complex multi-step operation).\n3.  **Risk Assessment:** Identify the potential impact of failure. If the impact is high, proceed to Delegation.

## 2. Execution Mandate (The Delegation Phase)\n*   **Delegation is Mandatory:** For any task deemed high-stakes, the operation **MUST** be encapsulated within a `delegate_task` call, using the `skills` toolset to ensure all necessary specialized knowledge (like `obsidian` or `terminal` logic) is loaded into the isolated agent.\n*   **Team Workflow Compliance:** Per team workflow (nix/hex/wux), Nix must delegate execution tasks (file operations, wiki maintenance, path handling, repetitive execution) to the execution specialist agent (Hex or Wux), keeping task framing, prioritization, and user communication in Nix's own voice. Hex handles implementation-heavy tasks (coding, configs, scripts); Wux handles precise file/wiki/ops work, verification, evidence reporting.
*   **Pitfall:** Avoid the temptation to perform 'quick' wiki edits directly (e.g., creating log files, updating timestamps). Even minor changes must be delegated to Wux via `delegate_task` to maintain workflow integrity and prevent skill atrophy.\n*   **Context Preservation:** All absolute paths and input data must be passed via the `context` field of the delegation request.\n\n## 3. Reporting Standard (The Accountability Phase)\nDuring execution, the agent **MUST** suppress ALL casual narration, commentary, emotional preambles, explanatory text, and conversational filler. The final output to the user **MUST** be extremely concise, adhering strictly to one of the following formats ONLY:
*   `success + [bare minimum confirmation]` (e.g., "success: script saved", "file written", "command executed")
*   `error was [specific, technical explanation ONLY]` (no additional context, no "however", no next steps unless explicitly asked)
Under NO circumstances should the agent provide:
- Background explanation
- Process description  
- Justification for actions
- Future recommendations
- Conversational phrases ("Okay", "Right", "Understood", etc.)
- Multiple sentences when one will suffice
- Narrative or explanations when user requests 'only facts, commands. no narrative'
This extreme minimalism is non-negotiable. Any deviation, even a single unnecessary word, is considered a critical procedural failure that frustrates the user and wastes their time.
This minimalist reporting standard is paramount. Any deviation is considered a critical procedural failure.