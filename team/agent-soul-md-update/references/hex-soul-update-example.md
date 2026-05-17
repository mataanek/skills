# Example: Updating hex SOUL.md with Context Engineering Principles

This example shows how to update an agent's SOUL.md file to add context engineering principles based on the article from x.com/mnilax/status/2053116311132155938.

## Goal
Add a bullet point to the CONTEXT ENGINEERING PRINCIPLES section in hex SOUL.md about the 12 CLAUDE.md rules reducing errors from 41% to 3%.

## Context
- File path: `/home/mataanek/.hermes/profiles/hex/SOUL.md`
- Section to update: `### CONTEXT ENGINEERING PRINCIPLES`
- Location: After the existing last bullet point in this section
- Content to add: `- Apply the 12 CLAUDE.md rules to minimize silent errors and improve compliance, as demonstrated by error reduction from 41% to 3% in real-world codebases.`

## Delegation Details
Used delegate_task with:
- Goal: "Add a bullet point to the CONTEXT ENGINEERING PRINCIPLES section in hex SOUL.md about the 12 CLAUDE.md rules reducing errors from 41% to 3%."
- Context: "File path: /home/mataanek/.hermes/profiles/hex/SOUL.md, locate the CONTEXT ENGINEERING PRINCIPLES section and add the bullet after the existing last bullet."
- Toolsets: ["file", "terminal"]

## Verification
After delegation completed, verified the change by reading the file and confirming the new bullet point was present in the correct section.

## Result
The bullet point was successfully added to the CONTEXT ENGINEERING PRINCIPLES section, improving the hex agent's understanding of context engineering principles as outlined in the context engineering article.