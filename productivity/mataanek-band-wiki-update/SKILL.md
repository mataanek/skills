---
id: mataanek-band-wiki-update
name: Mataanek Band Wiki Update
category: productivity
description: Standardized process for updating Mataanek's band wiki with new album/single information, lyrics, and metadata from mataanek.eu and raw source files.
---
# Mataanek Band Wiki Update Skill

## Purpose
Standardized process for updating Mataanek's band wiki with new album/single information, lyrics, and metadata from mataanek.eu and raw source files, ensuring consistency with existing wiki structure and formatting.

## When to Use
When updating the Mataanek band wiki located at `/home/mataanek/.hermes/wiki/` with new releases, lyrics, or information from the official website mataanek.eu or raw source files in `/home/mataanek/.hermes/wiki/raw/`.

## Prerequisites
- Access to the band wiki directory (`/home/mataanek/.hermes/wiki/`)
- Access to raw source files (`/home/mataanek/.hermes/wiki/raw/`)
- Knowledge of the release being added/updated (album, single, EP)
- Ability to extract information from mataanek.eu
- Familiarity with the existing wiki entity format

## Step-by-Step Process

### 1. Check for Updates on mataanek.eu
Visit https://mataanek.eu/ to identify new releases, updated information, or newly available lyrics.

### 2. Identify What Needs Updating
Determine which wiki entities need to be created or updated:
- Band entity (`entities/mataanek.md`)
- Album entities (e.g., `entities/the-comfort-architect.md`)
- EP entities (e.g., `entities/the-music-that-counts-the-stars.md`)
- Single entities (e.g., `entities/the-weight-that-wakes-me.md`)

### 3. Extract Information from Raw Sources
For lyrics and detailed information, check the raw source directory:
```bash
ls -la /home/mataanek/.hermes/wiki/raw/
```
Look for `.txt` files containing lyrics or information about the release.

### 4. Update Entity File Format
When creating or updating an entity file, use this format:

```yaml
---
created: 'YYYY-MM-DD'
sources:
- raw/[source-file-name].txt  # if applicable
tags:
- album/ep/single  # appropriate type
- music
- mataanek
title: [Entity Title]
type: entity
updated: 'YYYY-MM-DD'
---

# [Entity Title]

[Description from website or raw sources]

## [Overview/Album Overview/EP Overview/Single Overview]

*   **Release Date:** [Date from website]
*   **Genre:** [Genre from website]
*   **Concept:** [Concept description if available]

## Tracks

[List tracks with proper formatting]

## 🎶 Lyrics (Full)

[For each track with lyrics:]
### [Track Number] - [Track Name]

**Description:** [Brief description if available]

**Lyrics:**
[Full lyrics with section headers like [Verse 1], [Chorus], etc.]

[Repeat for each track]

## Related Entities

*   [[mataanek]]
```

### 5. Handle Lyrics Extraction
When extracting lyrics from raw files:
- Identify track sections (often separated by asterisk lines or clear headers)
- Extract track number and title from lines like "01 - Track Name"
- Preserve original section headers ([Verse], [Chorus], [Bridge], [Outro])
- Keep separator lines (asterisk lines) between tracks if they exist in source
- Format lyrics with proper spacing and section labels

### 6. Update Related Entities
After creating/updating an entity:
- Ensure the band entity (`entities/mataanek.md`) mentions the release
- Update concept entities if needed (e.g., `concepts/forest.md` for track concepts)
- Verify cross-links are correct using double-bracket notation

### 7. Verification Steps
Confirm the update was properly recorded:
- Check that the file exists in the correct location (`entities/[name].md`)
- Validate frontmatter format matches existing entries
- Verify lyrics are properly formatted and complete
- Confirm related entity links work
- Ensure the file validates as proper markdown

## Consistency Requirements
- Match exact formatting of existing entries (spacing, indentation, line breaks)
- Use same date format: `YYYY-MM-DD` for created/updated
- Follow same structure for metadata sections
- Maintain identical field ordering in frontmatter
- Use same wording style for descriptions
- Keep lyrics formatting consistent with existing entries (section headers, spacing)
- Use lowercase first letter directory for whiskey wiki (but NOT for band wiki - band wiki entities go directly in entities/)

## Common Pitfalls to Avoid
- Incorrect file path (band wiki entities go directly in `/home/mataanek/.hermes/wiki/entities/`)
- Missing or malformed frontmatter fields
- Inconsistent formatting compared to existing entries
- Forgetting to update related entities when appropriate
- Using incorrect date formats
- Not preserving original lyric formatting (section headers, spacing)
- Missing track listings in the Tracks section
- Incorrect entity linking (use double brackets: `[[entity-name]]`)

## Verification Checklist
- [] File created at correct path: `/home/mataanek/.hermes/wiki/entities/[name].md`
- [] Frontmatter includes all required fields with correct data types
- [] Format matches existing entries exactly (spacing, indentation)
- [] Lyrics are properly formatted with section headers
- [] All tracks from the release are listed
- [] Related entity links are correct
- [] File validates as proper markdown with readable content

## Example Workflow
For updating The Comfort Architect album with lyrics:

1. Check mataanek.eu for release information and confirm tracklist
2. Look in `/home/mataanek/.hermes/wiki/raw/` for "The Comfort Architect.txt"
3. Extract each track's lyrics from the raw file
4. Create/update `/home/mataanek/.hermes/wiki/entities/the-comfort-architect.md`
5. Format with proper frontmatter, album overview, tracklist, and lyrics sections
6. Verify against existing entries like `the-weight-that-wakes-me.md` for consistency

## References
- [Whiskey Wiki Update](skill://whiskey-wiki-update) – similar process for whiskey wiki
- [The Comfort Architect and Therapy in Despair Update](references/the-comfort-architect-and-therapy-in-despair-update.md) – detailed reference of today's update