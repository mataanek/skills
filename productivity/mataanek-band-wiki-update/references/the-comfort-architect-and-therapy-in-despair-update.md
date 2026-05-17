# Reference: The Comfort Architect and Therapy in Despair Wiki Update Session (2026-05-05)

This reference documents the specific updates made to the Mataanek band wiki during the 2026-05-05 session.

## What Was Updated
1. Entity: `/home/mataanek/.hermes/wiki/entities/the-comfort-architect.md`
   - Source: `/home/mataanek/.hermes/wiki/raw/The Comfort Architect.txt`
   - Updated: Full lyrics for all 6 tracks plus bonus track "Therapy in Despair"

2. Entity: `/home/mataanek/.hermes/wiki/entities/therapy-in-despair.md` (NEW)
   - Source: `/home/mataanek/.hermes/wiki/raw/Therapy in Despair.txt`
   - Source image: `/home/mataanek/.hermes/wiki/raw/Therapy.in.despair.upscaled.png`
   - Created new entity for the single

3. Entity: `/home/mataanek/.hermes/wiki/entities/mataanek.md` (UPDATED)
   - Updated `updated` field to '2026-05-05'
   - Added new releases to Tracks section in reverse chronological order

## Changes Made

### The Comfort Architect Entity Update
1. Updated frontmatter:
   - Added `sources: [- raw/The.Comfort.Architect.txt]`
   - Updated `updated: '2026-05-05'`

2. Complete track listing:
   - 01 Echo Chambers of One
   - 02 Keyboard Hero
   - 03 Left Behind in Real Time
   - 04 Faster Than Thought
   - 05 Thin Line to Walk
   - 06 To Change Again

3. Full lyrics extraction for each track including:
   - Intro, Verse, Pre-Chorus, Chorus, Bridge, Breakdown, Outro sections
   - Proper section header formatting ([Verse], [Chorus], etc.)
   - Asterisk separator lines between tracks preserved from source
   - Bonus track "Therapy in Despair" included

### Therapy in Despair Entity Creation (NEW)
1. Created new entity file with frontmatter:
   - `created: '2026-05-05'`
   - `sources: [- raw/Therapy in Despair.txt, - raw/Therapy.in.despair.upscaled.png]`
   - `tags: [single, music, mataanek]`
   - `title: Therapy in Despair`
   - `type: entity`
   - `updated: '2026-05-05'`

2. Entity body:
   - Heading with release title and type (Single)
   - Description block (from website)
   - Single Overview subsection with release date, genre, concept
   - Tracks subsection (list tracks)
   - Lyrics section with:
     - Track heading and description
     - Full lyrics (copy from raw .txt, cleaning up line numbers and extra spaces)
   - Related Entities section linking to `[[mataanek]]`

### Main Band Entity Update
1. Updated `/home/mataanek/.hermes/wiki/entities/mataanek.md`:
   - Updated `updated: '2026-05-05'`
   - Added new releases to Tracks section:
     - **The Comfort Architect** (Album) - Released May 13, 2026
     - **Therapy in Despair** (Single) - Released May 18, 2026

## Verification
- File size increased for the-comfort-architect.md from 1,099 bytes to 11,335 bytes
- New file created: therapy-in-despair.md (2,064 bytes)
- All lyrics properly formatted with section headers
- Consistent with existing wiki entity format
- Related entity link to [[mataanek]] maintained in all entities
- Release dates match website
- All new releases listed in mataanek.md under Tracks

## Source File Format Notes
The raw source files used:
- Windows line endings (`\\r\\n`)
- Track headers in format: `01 - Track Name`
- Lyrics sections with empty lines between parts
- Asterisk lines (`*******************************************************************`) as track separators (in The Comfort Architect file)
- Bonus track included at end (in The Comfort Architect file)

## Extraction Process Used
1. For The Comfort Architect:
   - Split raw content by asterisk separator lines
   - First section = header/info
   - Subsequent sections = individual tracks
   - For each track:
     - First line = track number and title
     - Remaining lines = lyrics
     - Preserved all original formatting and section headers

2. For Therapy in Despair:
   - Extract track header line: "01 - Therapy in Despair"
   - Remaining lines = lyrics
   - Preserved all original formatting and section headers
   - Cleaned up line numbers and extra whitespace for readability
