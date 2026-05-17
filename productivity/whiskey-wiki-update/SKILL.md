---
id: whiskey-wiki-update
name: Whiskey Wiki Update
category: productivity
description: Standardized process for adding new whiskey entries to Mataa's Obsidian-style whiskey wiki, ensuring consistency with existing entries and proper indexing.
---
# Whiskey Wiki Update Skill

## Purpose
Standardized process for adding new whiskey entries to Mataa's Obsidian-style whiskey wiki, ensuring consistency with existing entries and proper indexing.

## When to Use
When adding a new whiskey review or entry to the whiskey wiki located at `/home/mataanek/.hermes/wiki/whisky_wiki/`.

## Prerequisites
- Access to the whiskey wiki directory
- Knowledge of the whiskey being added (name, distillery, region, age, ABV, etc.)
- Mataa's personal scoring for the whiskey (if available)

## Step-by-Step Process

### 1. Verify Wiki Structure
```bash
# Check the entities directory structure
ls -la /home/mataanek/.hermes/wiki/whisky_wiki/entities/
```

### 2. Check for Existing Entry
Verify no entity file already exists for the whiskey:
```bash
# Example for Laphroaig 10 years
ls -la /home/mataanek/.hermes/wiki/whisky_wiki/entities/l/laphroaig-10-years.md
# If file exists, consider updating instead of creating new
```

### 3. Reference Existing Entry for Format
Use an existing similar entry (e.g., Arran 10 years) as template:
```bash
cat /home/mataanek/.hermes/wiki/whisky_wiki/entities/a/arran-10-years.md
```

### 4. Create New Entity File
Create the markdown file with proper frontmatter and content:
- Use lowercase first letter directory (e.g., `l/` for Laphroaig)
- Filename format: `[whiskey-name]-[age]-years.md`
- Include all required frontmatter fields:
  - `id`: sequential number (check existing highest ID)
  - `slug`: url-friendly identifier
  - `name`: full whiskey name
  - `lang`: typically "en"
  - `published_at`: current timestamp in ISO format
  - `image_url`: path to image (if available)
  - `image_alt`: alt text for image
  - `authors`: list of reviewers (typically ["Marcel", "Sascha"] for base entries)
  - `country`, `region`, `age`, `abv`, `distillery`, `bottler`, `type`
  - `flavour`: tasting notes
  - `price_per_liter`: numeric value
  - Ratings: `rating_marcel`, `rating_sascha`, `rating_value_for_money`, `mataanek`, `value_for_money_mataanek`
  - `url`: relative path to wiki entry
  - `pdf`: path to PDF export (if generated)

### 5. Add Mataa's Personal Scores
Ensure to include:
- `mataanek`: Mataa's personal score (0-100)
- `value_for_money_mataanek`: Mataa's value for money score (0-10)

### 6. Update Wiki Index
Increment the total page count in the index file:
```bash
# Update the index.md file to reflect new total count
# Find the line indicating total pages and increment by 1
```

### 7. Verification
Confirm the change was properly recorded:
- Check that the new file exists in the correct location
- Validate frontmatter format matches existing entries
- Verify wiki index shows updated page count
- Ensure Clawmem will detect the change (it monitors the wiki folder)

## Consistency Requirements
- Match exact formatting of existing entries (spacing, indentation, line breaks)
- Use same date format for `published_at`: `YYYY-MM-DDTHH:MM:SS+00:00`
- Follow same structure for metadata sections
- Maintain identical field ordering in frontmatter
- Use same wording style for descriptions

## Common Pitfalls to Avoid
- Incorrect file path (wrong letter directory)
- Missing or malformed frontmatter fields
- Inconsistent formatting compared to existing entries
- Forgetting to update the wiki index
- Using incorrect score formats (should be integers)
- Not including Mataa's personal scores when available

## Verification Checklist
- [] File created at correct path: `/home/mataanek/.hermes/wiki/whisky_wiki/entities/[first-letter]/[slug].md`
- [] Frontmatter includes all required fields with correct data types
- [] Mataa's scores included: `mataanek` and `value_for_money_mataanek`
- [] Format matches existing entries exactly (spacing, indentation)
- [] Wiki index updated to reflect new total page count
- [] File validates as proper markdown with readable content

## Example
See the Laphroaig 10 years entry created at:
`/home/mataanek/.hermes/wiki/whisky_wiki/entities/l/laphroaig-10-years.md`

This follows the exact same structure as the Arran 10 years entry but with Laphroaig-specific details and Mataa's personal scores.