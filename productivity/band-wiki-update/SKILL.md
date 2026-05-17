---
name: band-wiki-update
description: "Standardized process for updating Mataanek's band wiki with new album/single information, lyrics, and metadata from mataanek.eu and raw source files."
version: 1.0.0
author: Nix
category: productivity
---

# Band Wiki Update Process

This skill outlines the steps to keep the band wiki (`/home/mataanek/.hermes/wiki/band/`) up-to-date with information from `mataanek.eu` and raw source files (lyrics, images, etc.). It ensures consistency, proper formatting, and verifiable outputs.

## Prerequisites

- Obsidian vault configured at `/home/mataanek/.hermes/wiki/`
- Band notes stored in `/home/mataanek/.hermes/wiki/band/` (or personal folder for status files)
- Raw assets (images, lyrics) in `/home/mataanek/.hermes/wiki/raw/`
- Access to `mataanek.eu.md` in the raw folder for reference.

## Steps

### 1. Verify Raw Source Files
Ensure the following files exist in `raw/` (examples):
- `Circle.turns.again.final.upscaled.300DPI.jpg`
- `Music.counting.stars.cover.final.JPEG`
- `Therapy.in.despair.upscaled.png`
- `the.weight.that.wakes.me.album.cover.final.jpg`
- Lyrics `.txt` files for each track/album.

```bash
ls -la /home/mataanek/.hermes/wiki/raw/
```

### 2. Move or Ensure Band Notes Are in Correct Location
Band-related markdown notes should reside in `/home/mataanek/.hermes/wiki/band/`. If any are found in `entities/` or elsewhere, move them to `band/` and update links.

```bash
# Example: moving from entities to band
mv /home/mataanek/.hermes/wiki/entities/*.md /home/mataanek/.hermes/wiki/band/ 2>/dev/null || true
```

After moving, update any wikilinks referencing the moved files to include the `band/` prefix (preserving aliases). Use a search-and-replace script or manually edit.

### 3. Add Cover Images to Album Notes
For each album/EP/single that has a cover image in `raw/`, ensure the corresponding markdown file in `band/` includes an image link at the top.

#### Example for Circle Turns Again
Edit `/home/mataanek/.hermes/wiki/band/circle-turns-again.md`:
```markdown
![Circle Turns Again Cover](../raw/Circle.turns.again.final.upscaled.300DPI.jpg)
```

#### Example for The Music That Counts the Stars
Edit `/home/mataanek/.hermes/wiki/band/the-music-that-counts-the-stars.md`:
```markdown
![The Music That Counts the Stars Cover](../raw/Music.counting.stars.cover.final.JPEG)
```

Verify no duplicate image lines exist.

### 4. Enrich the Mataanek Band Page with Info from mataanek.eu
Extract structured information from `raw/mataanek.eu.md` (or fetch from site) and update `/home/mataanek/.hermes/wiki/band/mataanek.md` under the `## Tracks` section (or create if missing).

Include for each release:
- **Release Type** (Album/EP/Single)
- **Release Date**
- **Description** (summary from mataanek.eu)
- **Tracklist** with track numbers, names, and lyric availability (e.g., `01Forest\n  Lyrics`)
- **Listen Links** (Spotify, Apple Music, YouTube Music, Amazon Music, Tidal, Deezer) as bullet list with links.

#### Formatting Template
```markdown
## Tracks

**The Circle Turns Again (Album)**
*
**Release Date:** March 4, 2026
*
**Description:** Circle Turns Again shifts focus from human psychology to nature itself: instead of personal gloom and societal fracture, each song inhabits forests, mountains, fields, and oceans as the real protagonists, using animals and seasons to show how the world endures without us. Compared to The Weight That Wakes Me, which was heavier on existential fatigue and inner turmoil, the album stays melodic and doomy but feels more cinematic and some songs are much more progressive and light - respecting the song itself. Whole album is connected with recurring "circle turns again" motif.
*
**Tracklist:**
* 01Forest
  Lyrics
* 02River
  Lyrics
* 03Mountains
  Lyrics
* 04Fields & Meadows
  Lyrics
* 05Ocean
  Lyrics
* 06Sky
  Lyrics
* 07Forest (Alternate Edit)
  Lyrics
* 08Ocean (Alternate Edit)
  Lyrics
*
**Listen to it here:**
[Spotify](https://open.spotify.com/album/3ByxXrXb7DXLjECI9Etz5B?si=OcQ6EfZIQsCOqPprqRCpJg)
[Apple Music](https://music.apple.com/cz/album/circle-turns-again/1878615876)
[YouTube Music](https://www.youtube.com/watch?v=X7OniWxdod0&list=OLAK5uy_nnlQT4zCiBMSvEdp0trXVTO7gpQ1-oo6c)
[Amazon Music](https://music.amazon.com/albums/B0GPCZXR6W?marketplaceId=ATVPDKIKX0DER&musicTerritory=US&ref=dm_sh_zMzckdUjvUl9fxE5jXxRjJoER)
[Tidal](https://tidal.com/album/500490306)
[Deezer](https://link.deezer.com/s/32DWH5XOWbDaAwkRzRQvx)

**The Music That Counts the Stars (EP)**
*
**Release Date:** February 1, 2026
*
**Description:** Progressive doom metal unfolding me/us/cosmos. From disciplined fatigue through freedom's excuses to starry voids, evoking existential scale, primordial unknowns, and the faint music seeking listeners in the dark.
*
**Tracklist:**
* 01The Weight That Wakes Me
  8:00Lyrics
* 02The Society Fracture
  5:50Lyrics
* 03The Music That Counts the Stars
  7:35Lyrics
* 04The Music That Counts the Stars - Alternate Edit
  6:46Lyrics
*
**Listen to it here:**
[Spotify](https://open.spotify.com/album/4Rmvhq8If2QPY28PxFdrCo?si=YW9pNNxuSaKmaC8dYh84fA)
[Apple Music](https://music.apple.com/cz/album/the-music-that-counts-the-stars-ep/1872516736)
[YouTube Music](https://music.youtube.com/playlist?list=OLAK5uy_k9ggBbaf6FA2a87_hnXKyZXbEcKIXGcNA&si=wRZTRmfWu_l4pbFz)
[Amazon Music](https://music.amazon.com/albums/B0GK7Y1QJ1?marketplaceId=ATVPDKIKX0DER&musicTerritory=US&ref=dm_sh_P1wjRRU1kSCW1wc7Pme34BvHf)
[Tidal](https://tidal.com/album/493711995)
[Deezer](https://www.deezer.com/us/album/907407622)

**The Weight That Wakes Me (Single)**
*
**Release Date:** January 10, 2026
*
**Description:** Doom metal steeped in personal gloom, fatigue, and existential heaviness. It evokes methodical thought, endurance, and cycles of physical-emotional perseverance—weariness veiled in discipline, routine's entropy, control's futility.
*
**Tracklist:**
* 01The Weight That Wakes Me
  8:00Lyrics
*
**Listen to it here:**
[Spotify](https://open.spotify.com/album/40LJezMfSON38lX2mOCA6w)
[Apple Music](https://music.apple.com/cz/album/the-weight-that-wakes-me-single/1869781841)
[YouTube Music](https://www.youtube.com/watch?v=2sm-5IC2euk)
[Amazon Music](https://music.amazon.com/albums/B0GH9T4YJZ?marketplaceId=ATVPDKIKX0DER&musicTerritory=US&ref=dm_sh_LSOYI7IafC3XgeUreVGnlYM6e&trackAsin=B0GHB4DBKH)
[Tidal](https://tidal.com/album/490292005)
[Deezer](https://link.deezer.com/s/32ko4OSJt3MLmq1YCQEgf)
```

### 5. Validate Changes in Obsidian
Launch Obsidian GUI to verify:
- Images display correctly.
- Links (wikilinks and external) are functional.
- Graph view shows expected connections.
- No broken links or missing files.

```bash
# Ensure dependencies installed (if not already)
sudo apt-get update && sudo apt-get install -y libfuse2 dbus-x11
sudo service dbus start
export DISPLAY=:0
# Launch Obsidian (from /home/mataanek)
APPIMAGE_EXTRACT_AND_RUN=1 ./Obsidian.AppImage .hermes/wiki
```

### 6. Commit Changes (Optional)
If using version control, commit the updated files with a descriptive message.

```bash
cd /home/mataanek/.hermes/wiki
git add band/ raw/  # as appropriate
git commit -m "Update band wiki with latest album info and cover images"
```

## Verification Checklist
- [ ] All band markdown files are in `/home/mataanek/.hermes/wiki/band/` (or personal folder for status).
- [ ] Cover images are present in album notes and render in Obsidian.
- [ ] Mataanek band page contains detailed tracklists, release dates, descriptions, and listen links for all major releases.
- [ ] No broken wikilinks (Obsidian shows no unresolved links).
- [ ] Raw source files referenced exist and are accessible.
- [ ] Optional: Changes committed to Git.

## Troubleshooting
- **Missing images**: Verify file paths and that the raw file exists; check for typos in filename or extension.
- **Links not updating**: Ensure you moved the markdown file and updated all references; run a grep for old paths to confirm.
- **Obsidian GUI not launching**: Confirm libfuse2 and dbus-x11 installed, DBus service running, DISPLAY set, and an X server (VcXsrv or WSLg) active on Windows.
- **Information outdated**: Re-check `raw/mataanek.eu.md` for latest details; repeat extraction.
## Notes

- Keep the band wiki focused on music/band content; move personal status notes (e.g., `nix-status.md`, `mataanek-profile.md`) to a `personal/` folder within the vault if they should remain accessible but not clutter the main band namespace. See the obsidian skill for standardized personal notes management (including automated daily updates).
- Always validate paths before executing move or copy commands.
- Prefer single-step, verifiable actions; avoid leaving temporary scripts behind—clean up after use.