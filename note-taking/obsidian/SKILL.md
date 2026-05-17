---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable. If unset, defaults to `/home/mataanek/.hermes/wiki`.

Note: Vault paths may contain spaces - always quote them.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-/home/mataanek/.hermes/wiki}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-/home/mataanek/.hermes/wiki}"

# All notes
find "$VAULT" -name "*.md" -type f

# In a specific folder
ls "$VAULT/Subfolder/"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-/home/mataanek/.hermes/wiki}"

# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-/home/mataanek/.hermes/wiki}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-/home/mataanek/.hermes/wiki}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## WSL GUI Setup for Obsidian

When running Obsidian via AppImage in WSL, the following prerequisites are required due to missing FUSE 2 and DBus:

1. Install packages: `sudo apt-get update && sudo apt-get install -y libfuse2 dbus-x11`
2. Start DBus service: `sudo service dbus start`
3. Set DISPLAY variable: add `export DISPLAY=:0` to ~/.bashrc or ~/.zshrc and source it.
4. Ensure an X server is running on Windows (e.g., VcXsrv with "Disable access control" checked, or use WSLg on Windows 11 22H2+).
5. Launch Obsidian with: `APPIMAGE_EXTRACT_AND_RUN=1 ./Obsidian.AppImage <vault-path>`

## Managing Personal Notes

To keep the vault focused on domain content (e.g., whisky, band), move personal scratch notes (like status logs) to a dedicated subfolder:

1. Create a personal folder inside the vault: `mkdir -p $VAULT/personal`
2. Move notes: `mv $VAULT/entities/nix-status.md $VAULT/entities/mataanek-profile.md $VAULT/personal/`
3. Wikilinks to these notes remain functional because Obsidian resolves links within the vault; no link updates are required.
4. Optionally, add a daily timestamp script to append logs: see `scripts/update-status.sh`.
5. For automated daily updates, see `references/daily-status-cron.md`.
