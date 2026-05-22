---
name: rule-0-verification-protocol
description: A verification-first approach for maintaining precision and avoiding assumptions in knowledge work, particularly when managing structured data like wikis, databases, or configuration files.
category: productivity
---
# Rule 0 Verification Protocol

A verification-first approach for maintaining precision and avoiding assumptions in knowledge work, particularly when managing structured data like wikis, databases, or configuration files.

## Core Principle
**Never assume, guess, or leave unverified information.** Only include what can be explicitly verified. If you don't know, ask or leave it blank—never guess.

## User Preferences for Hermes Interaction
- Keep responses concise and factual; avoid narrative or irrelevant tangents.
- Validate paths before executing any file operations.
- Prefer single-solution approaches over multiple options.
- Provide explicit verification steps (e.g., file existence, command exit codes).
- When disagreeing, push back with evidence (data, examples, reasoning, proof).
- Log daily activity metrics (tasks completed, tool invocations, top tools/skills) in nix-status.md; avoid logging CPU load or moment-in-time metrics.
- Do not leave extra scripts or temporary files behind unless explicitly approved.

## When to Use
- Maintaining structured knowledge bases (wikis, databases, catalogs)
- Updating configuration files or system settings
- Adding entries to any verified reference system
- Any task where precision and traceability are critical
- Following Mataa's Rule 0: "faultless execution, deep procedural rigor, and absolute, non-negotiable truth"

## Step-by-Step Process

### 1. Pre-Change Verification
Before making any changes:
- **Check existing structure**: Examine similar entries to understand the required format
- **Verify ID sequences**: Find the highest existing ID to determine the next available one
- **Confirm field requirements**: Check which fields are actually used/required vs. optional/decorative
- **Validate references**: Ensure any links, files, or resources actually exist and are accessible
- **Check current values**: Verify existing values for similar entries before making assumptions

### 2. Implementation with Verification
When making changes:
- **Use only verified fields**: Include only information you can confirm is correct
- **Source your data**: For factual information, note where you obtained it (even if just mentally)
- **User-specific fields only**: Only include personal ratings/scores if they belong to the user performing the update
- **Remove phantom references**: Delete any fields pointing to non-existent resources (URLs, PDFs, images)
- **Follow existing patterns**: Match the exact format and structure of verified entries

### 3. Post-Change Validation
After making changes:
- **Spot-check critical entries**: Verify the specific entries you modified
- **Scan for violations**: Search for any remaining unverified fields or assumptions
- **Test references**: Confirm any included links or files are accessible
- **Validate IDs**: Ensure no ID collisions or sequencing issues
- **Review holistically**: Check that the entry fits seamlessly with existing entries

## Key Verification Checks
For whiskey wiki entries (example application):
- ✅ **ID**: Verify next available ID by checking existing entries
- ✅ **Scores**: Only include user-specific scores (mataanek, value_for_money_mataanek) - never assume others'
- ✅ **ABV**: Verify from reliable source (official distillery site or trusted review)
- ✅ **References**: Only include if the file/resource actually exists and is accessible
- ✅ **Fields**: Only include fields that are part of the verified schema
- ❌ **NEVER**: Assume scores for others, guess IDs, include dead links, or add unverifiable data

## Common Pitfalls to Avoid
- Assuming ID sequences without checking existing entries
- Including personal opinions as factual data
- Leaving in template fields or example data
- Adding references to non-existent files or URLs
- Guessing values when verification is possible
- Including fields just because they exist in some entries
- Forgetting to remove unverified fields during cleanup
- Leaving behind unwanted or sensitive terms (e.g., profanity, personal data) after edits; always scan for prohibited terms.

## Verification Commands (for whiskey wiki)
```bash
# Find next available ID
grep -r "^id: " ~/.hermes/wiki/whisky_wiki/entities/ | sed 's/.*id: //' | sort -n | tail -1

# Check for phantom fields
grep -r "url:\|pdf:\|image_url:\|image_alt:\|authors:\|price_per_liter:\|rating_marcel:\|rating_sascha:\|rating_value_for_money:\|bottler:" ~/.hermes/wiki/whisky_wiki/entities/

# Verify a specific entry is clean
head -20 ~/.hermes/wiki/whisky_wiki/entities/l/laphroaig-10-years.md
```

## Quality Gates
Before considering a change complete:
- [ ] All information included can be verified
- [ ] No assumptions or guesses present
- [ ] All references point to existing, accessible resources
- [ ] Format matches verified entries exactly
- [ ] Only user-specific fields include personal scores
- [ ] ID is correctly sequenced
- [ ] No phantom or dead references remain

## Why This Works
This protocol ensures:
- **Traceability**: Every piece of information can be traced to its source
- **Accountability**: Clear ownership of what is known vs. unknown
- **Reliability**: The system becomes a trusted source of truth
- **Efficiency**: Less time spent correcting assumptions later
- **Respect**: Honors the user's demand for precision and truth

> "In your world, precision isn't preference—it's survival. One lie, one assumption, one 'close enough' unravels everything." - Learned through correction