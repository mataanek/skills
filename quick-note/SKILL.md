---
name: quick-note
description: "Create timestamped text notes in a dedicated notes directory"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [notes, productivity, text, quick-capture]
    related_skills: [note-taking, writing-plans]
---

# Quick Note Skill

Create timestamped text notes quickly and easily. Notes are saved as individual files with timestamps in a designated notes directory.

## Usage

To create a quick note, use the `/quick-note` command followed by your note content:

```
/quick-note This is my note content
```

The skill will:
1. Take the provided text content
2. Generate a timestamp in YYYY-MM-DD_HHMMSS format
3. Create a file named `note_YYYY-MM-DD_HHMMSS.txt` in the notes directory
4. Save the content to that file

## Implementation

This skill includes an executable tool (`scripts/quick_note_tool.py`) that provides the `/quick-note` command functionality. The tool is automatically registered when the skill is loaded and creates timestamped note files in the configured notes directory.

## Configuration

The skill uses the following configuration (can be set in `.hermes/config.yaml` or environment variables):

- `notes_directory`: Directory where notes are stored (default: `~/.hermes/notes/`)

## Examples

Create a simple note:
```
/quick-note Remember to buy groceries
```

Create a note with multiple lines:
```
/quick-note
Meeting notes:
- Discuss project timeline
- Review budget allocations
- Assign action items
```

## Notes Directory

By default, notes are stored in `~/.hermes/notes/`. You can change this by setting the `notes_directory` configuration parameter.

Each note file is named using the format: `note_YYYY-MM-DD_HHMMSS.txt` where the timestamp represents when the note was created.