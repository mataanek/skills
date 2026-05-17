---
name: code-transformation-engineering
description: The definitive, high-stakes protocol for taking a complex, existing source code file and modifying it to meet a demanding set of interconnected functional requirements. This is the surgical strike protocol.
---

# Skill: code-transformation-engineering

## Overview
This skill provides the definitive, high-stakes protocol for taking a complex, existing source code file (e.g., a media processing script, a core agent loop, or a pipeline component) and modifying it to meet a demanding set of interconnected functional requirements. This is the surgical strike protocol for when simple fixes fail.

## When to Use
Use this skill when the user provides a complex script and a list of 3+ specific, often interdependent requirements (e.g., 'Rain must persist during Text phase,' 'Spawning rate must be multiplicative on two features').

## Workflow (The Surgical Strike Protocol)
1.  **Read State:** Use `file:read_file` to capture the current, original state of the source file.
2.  **Analyze Delta:** Deconstruct the user's requirements, identifying all points of change and their dependencies (e.g., Requirement 4 depends on the successful implementation of Requirement 1 and 2).
3.  **Execute Transformation (The Core):**
    *   **Primary Method (Strongly Preferred):** Use a focused `execute_code` block to encapsulate the entire read-modify-write process in one atomic operation. This is significantly more reliable than delegation for code transformation tasks.
    *   **Avoid Delegation Wrapper:** Do not use `delegate_task` for complex code modifications. Experience shows it frequently fails with non-specific errors (e.g., 400) that obscure the real issue.
    *   **Handle Tool Output Formatting:** When using tools that may add metadata (like line numbering), always clean the output before writing. Common patterns to remove:
        - Leading line numbers and pipes (e.g., "    1|import subprocess")
        - Double line numbering from nested tool calls
        - Escaped quotes in docstrings
4.  **Validate/Test (Crucial):** Before declaring success, verify the change. If possible, run unit tests or a deterministic probe. If runtime fails, immediately analyze the traceback for *environmental* issues (like `ModuleNotFoundError`) before assuming a logic error.
5.  **Write State:** If validation passes, use `file:write_file` to atomically overwrite the original script with the perfected, transformed code.

## Pitfalls & Learnings
*   **Delegation Trap:** When dealing with complex code transformation, do not rely solely on the `delegate_task` wrapper. When the wrapper fails (especially with non-specific API errors like 400), the solution is to drop the wrapper and use direct `execute_code` to enforce the change.
*   **Dependency Check:** Always treat `ModuleNotFoundError` as a *workflow* error (missing dependency), not a *logic* error. Fix the environment first.
*   **Interconnectedness:** Requirements are rarely isolated. The transformation must view the script holistically (e.g., Rain persistence is not a single change; it changes the control flow of the entire frame loop).

## Dependencies
*   References: `references/audio_video_transformation_notes.md`
---