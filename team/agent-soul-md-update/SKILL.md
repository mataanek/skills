---
name: agent-soul-md-update
description: Update an agent's SOUL.md file in the Hermes team context.
category: team
version: 0.1.0
author: Hermes Agent
---

# Agent SOUL.md Update Skill

This skill describes how to update an agent's SOUL.md file in the Hermes team context.

## Steps

1. Identify the agent whose SOUL.md needs updating (e.g., hex, wux, nix) based on the goal.
2. Delegate the task to the appropriate agent:
   - If the update is about coding, config, or scripts, delegate to hex.
   - If the update is about precise file operations, wiki maintenance, or path-sensitive tasks, delegate to wux.
   - The nix agent retains oversight and reviews the changes.
3. Provide the delegate_task with:
   - Goal: one-sentence description of the desired change.
   - Context: file path, current content (if needed), and the specific update to make.
   - Toolsets: ["file", "terminal"] for file operations.
4. Wait for the delegate_task to complete and verify the change by reading the file.

## Example

Updating hex SOUL.md to add a bullet point about the 12 CLAUDE.md rules:

Goal: Add a bullet point to the CONTEXT ENGINEERING PRINCIPLES section in hex SOUL.md about the 12 CLAUDE.md rules reducing errors from 41% to 3%.
Context: File path: /home/mataanek/.hermes/profiles/hex/SOUL.md, locate the CONTEXT ENGINEERING PRINCIPLES section and add the bullet after the existing last bullet.
Toolsets: ["file", "terminal"]

## Notes

- Always verify the change by reading the file after the delegate_task completes.
- If the delegate_task fails, check the error and adjust the context or goal.