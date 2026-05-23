---
name: educational-wiki-update
description: Standardized process for creating educational content for Mataanek's wiki with proper depth, format, and presentation readiness.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: wiki, educational, content, presentation, learning
    relatedskills: note-taking, research, creative
---

# Educational Wiki Update

## Overview

Standardized process for creating educational content suitable for Mataanek's wiki that follows pedagogical best practices, meets format requirements, and is ready for presentation use. This skill ensures content has sufficient depth for actual teaching (not just summarization) and follows the user's preferred structure: Concept explanation → Visual analogy → Knowledge check.

## When to Use

- User requests educational content creation for the wiki
- Creating learning materials from external sources (threads, articles, videos)
- Developing content that will be used for teaching or presentations
- User specifies format requirements (HTML, knowledge check timing, etc.)
- Building structured courses or lesson series

## Workflow

### Step 1 — Validate Target Location

Before creating any files, validate the target wiki location using Hermes configuration:

```python
# Always check config for wiki path
from hermes_tools import execute_code
import os

result = execute_code("""
import yaml
with open('/home/mataanek/.hermes/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
wiki_path = config.get('skills', {}).get('config', {}).get('wiki', {}).get('path')
print(wiki_path)
""")

if result['output'].strip() != '/home/mataanek/.hermes/wiki':
    raise ValueError(f"Unexpected wiki path: {result['output'].strip()}")
```

Never assume wiki location - always validate from config to prevent saving to wrong folders.

### Step 2 — Assess Content Depth

Evaluate whether source material provides sufficient depth for actual educational use:

✅ **DO**: Extract concepts with explanations suitable for ~2 minutes of teaching each
✅ **DO**: Include concrete examples, analogies, and applications
✅ **DO**: Provide context about why each concept matters
❌ **DON'T**: Just summarize or copy-paste source material
❌ **DON'T**: Create content that's only suitable for reference, not teaching

For each concept, ensure you have:
- One clear, concise core explanation (1-2 sentences)
- One visual analogy that makes the concept intuitive
- One knowledge check question that tests understanding
- Context about scale, application, or significance

### Step 3 — Follow Pedagogical Structure

Each concept unit must follow this exact structure:

1. **Concept Explanation** (What it is)
   - Clear definition in accessible language
   - Key characteristics or mechanics
   - Scale or significance where relevant

2. **Visual Analogy** (How to think about it)
   - Concrete, relatable comparison
   - Should create an "aha" moment
   - Based on user's preferred imagery when available

3. **Knowledge Check** (Validate understanding)
   - Single clear question targeting the core concept
   - Designed for presentation use (reveal on SPACE, not typing)
   - Followed by brief confirmation/correction

### Step 4 — Format for Presentation

Create content in HTML format optimized for presentation:

- Use large, readable fonts (minimum 1.2em for body text)
- Ensure good contrast for projector visibility
- Place images prominently (top 40-60% of slide)
- Keep text concise - audience should be listening, not reading
- Include navigation controls (LEFT/RIGHT arrows or buttons)
- Add progress indicator (Concept X of 20)
- Implement knowledge check with SPACE-to-reveal functionality
- Add reward/confirmation feedback after answer reveal

### Step 5 — Meet Timing Constraints

Respect user-specified timing requirements:

- For 20 concepts in 40 minutes: ~2 minutes per concept
- Allocate time: ~45 sec explanation, ~45 sec analogy, ~30 sec knowledge check
- Content should support this pacing - not too dense, not too sparse
- Practice delivery to ensure timing works

### Step 6 — Use Images Effectively

When source material includes images:

- Select images that directly illustrate the concept
- Place image at beginning of concept (as requested by user)
- Ensure image is properly sized and optimized for web
- Provide meaningful alt text and caption
- Verify image loads correctly from relative path
- Never use images as mere decoration - they must serve an educational purpose

### Step 7 — Validate Before Completion

Before considering the task complete:

✅ Verify all files are in the correct wiki location (validated from config)
✅ Check that each concept has explanation, analogy, and knowledge check
✅ Test that knowledge check reveals answer on SPACE
✅ Confirm images load properly in browser
✅ Ensure navigation works between concepts
✅ Validate timing estimates align with user requirements
✅ Confirm content is suitable for actual teaching (not just reference)

## Common Pitfalls

### ❌ Wrong Wiki Location
**Problem**: Saving to `/home/mataanek/wiki/` instead of `/home/mataanek/.hermes/wiki/`
**Fix**: Always validate path from Hermes config before saving any files
**Prevention**: Make path validation the first step in any wiki content creation

### ❌ Insufficient Depth
**Problem**: Creating content that only summarizes rather than teaches
**Fix**: For each concept, ask: "Could I teach this to someone for 2 minutes?"
**Prevention**: Extract not just what the concept is, but why it matters and how to intuit it

### ❌ Poor Knowledge Check Format
**Problem**: Requiring user to type answers during presentation
**Fix**: Design knowledge checks to reveal answer on SPACE bar only
**Prevention**: Remember: "Knowledge check = presenter asks, audience thinks, SPACE reveals"

### ❌ Misused Images
**Problem**: Using images as decoration rather than visual analogies
**Fix**: Every image must directly support understanding of the concept
**Prevention**: Ask: "Does this image make the concept clearer? Would removing it hurt comprehension?"

### ❌ Ignoring Timing
**Problem**: Creating content that takes too long or too short to present
**Fix**: Time your planned delivery - adjust content density to hit targets
**Prevention**: For 20 concepts in 40 minutes, target ~100-150 words of explanation per concept

## File Structure

Created content should follow this structure:

```
/home/mataanek/.hermes/wiki/
├── educational/
│   ├── course/
│   │   ├── lesson01_concept_name.html
│   │   ├── lesson02_concept_name.html
│   │   └── ... (through lesson20)
│   ├── images/
│   │   ├── (downloaded/source images)
│   │   └── (generated diagrams if needed)
│   ├── index.md          (course index/overview)
│   └── README.md         (course description and usage)
└── News Clippings/       (existing wiki sections)
```

## Reference Implementation

See the AI Foundations 20-concept presentation at:
`/home/mataanek/.hermes/wiki/educational/ai_foundations_40min_final.html`

This implementation demonstrates:
- Correct wiki location (validated from config)
- Sufficient depth for ~2 minutes/concept teaching
- Concept → Visual Analogy → Knowledge check structure
- Image placed at beginning of each concept
- Knowledge check reveals answer on SPACE
- Presentation-optimized formatting
- 40-minute total timing for 20 concepts
- Proper navigation and progress tracking

## Related Skills

- `note-taking`: For structuring and organizing educational content
- `research`: For extracting and verifying information from sources
- `creative`: For visual design and analogy creation
- `freshrss-news-digest`: Example of a well-structured, domain-specific update skill

## Example Usage

When user says: "Create educational wiki content from this AI thread"
1. Validate wiki location from config
2. Extract 20 concepts with sufficient depth for teaching
3. For each concept: create explanation, find/make visual analogy, design knowledge check
4. Format as HTML presentation with proper image placement
5. Test knowledge check (SPACE reveal) and navigation
6. Verify timing meets ~2 minutes/concept requirement
7. Save to correct educational/ directory in wiki
8. Update course index to include new lessons