# AI Foundations Lesson - Example Implementation

This document shows how the AI Foundations 20-concept presentation implements the educational-wiki-update skill.

## Location Validation
The lesson correctly validates the wiki location from Hermes config:
- Configured path: `/home/mataanek/.hermes/wiki`
- Content saved to: `/home/mataanek/.hermes/wiki/educational/ai_foundations_40min_final.html`

## Depth of Content
Each concept includes:
1. **Concept Explanation**: 1-2 sentences defining the concept and its significance
   - Example (Neural Networks): "A pipeline of layers (input → hidden → output) where each connection has a trainable weight. Adjusting billions of weights makes the network accurate."
2. **Visual Analogy**: Concrete, relatable comparison
   - Example: "Like specialists on an assembly line - each layer processes and passes information to the next."
3. **Knowledge Check**: Single question designed for SPACE-bar reveal
   - Example: "What do we call the adjustable parameters that determine connection strength between neurons?"

## Presentation Format
- HTML format with large, readable fonts (1.3em+ for explanations)
- Images placed prominently at beginning of each concept (top 40% of slide)
- Navigation controls (LEFT/RIGHT arrows and buttons)
- Progress indicator ("Concept X of 20")
- Knowledge check reveals answer on SPACE bar only
- Reward/confirmation feedback after correct answer

## Timing Compliance
- Designed for ~2 minutes per concept (40 minutes total for 20 concepts)
- Explanation: ~45 seconds
- Analogy: ~45 seconds  
- Knowledge check: ~30 seconds (including SPACE reveal and brief discussion)

## Image Usage
- Uses actual images from the source thread as visual analogies
- Each image directly illustrates the concept being taught
- Images are optimized for web use and properly sized
- No decorative images - each serves an educational purpose

## File Structure
```
educational/
├── ai_foundations_40min_final.html     (main presentation)
├── images/                             (source images from thread)
│   ├── HI5-xP8aIAAL0YM.jpg
│   ├── HI58qtEbUAAyrSy.jpg
│   ├── HI59HOVbkAA2OOE.jpg
│   └── HI59_uXa0AAxbxR.jpg
└── ai_foundations_40min_final_README.md (usage documentation)
```

## Verification Completed
✅ Content validates correct wiki location from config
✅ Each concept has explanation, analogy, and knowledge check
✅ Knowledge check reveals answer on SPACE bar
✅ All images load correctly from relative paths
✅ Navigation works between all 20 concepts
✅ Timing estimates align with 2 minutes/concept requirement
✅ Content is suitable for actual teaching (not just reference)