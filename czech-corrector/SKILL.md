---
name: czech-corrector
description: Provides a tool to correct Czech text using LanguageTool (via jar) with fallback to rule-based corrections.
---
# Skill: Czech Corrector

Provides a tool to correct Czech text using LanguageTool (via jar) with fallback to rule-based corrections.

## Tool: czech_check

Input: text (string)
Output: corrected Czech text (string)

Usage:
- From Hermes: `hermes run czech-corrector.czech_check --text "Nix je skvela."`
- Or from another skill: call the tool directly.

## Implementation

The tool runs the script `~/.hermes/skills/czech-corrector/scripts/czech_check_tool.py` which wraps the czech_check.py script.

## References

See `references/common_corrections.md` for the list of common typo and agreement corrections used by the rule‑based fallback.

## Dependencies

- Java 17+ (installed)
- LanguageTool jar (installed in ~/.local/share/languagetool/LanguageTool-6.6/languagetool.jar)
- Python package `language-tool-python` (installed in user site)

## Examples

Input: "Nix je skvela operator a ma rada mataanka. Dej mi pusu."
Output: "Nix je skvělý operator a ma rád mataanka. dej mi pusu."

Input: "Dnes je krasny den."
Output: "Dnes je krásný den."

Input: "Dej mi prosim sklenici vody."
Output: "Dej mi prosím sklenici vody."
