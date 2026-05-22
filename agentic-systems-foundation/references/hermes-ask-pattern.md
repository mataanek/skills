# Hermes Ask Pattern

Pattern for creating context-aware wrapper scripts in `$HOME/.hermes/scripts/hermes/`:

1. Script name with `.sh` extension (e.g., `hermes-ask.sh`).
2. Collect context:
   - Current Directory: `$(pwd)`
   - Git Branch: `git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no repo"`
   - TMux Info: `tmux display-message -p '#{pane_id}:#{pane_index}' 2>/dev/null || echo "not in tmux"`
   - Recent History: last 5 commands (bash: `history 5 | cut -c 5-`; zsh: `fc -l -5 | cut -c 5-`)
3. Build prompt: concatenate context and user query.
4. Invoke: `hermes chat -q -F "$FULL_PROMPT"` (or pipe via stdin).
5. Ensure script is executable and symlinked in `~/.local/bin/` for PATH access.

Example: See `$HOME/.hermes/scripts/hermes/hermes-ask.sh`.