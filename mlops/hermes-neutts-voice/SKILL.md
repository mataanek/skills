---
name: hermes-neutts-voice
category: mlops
description: >
  Local NeuTTS-based cloned voice for Hermes. Profile-agnostic: switch
  voices by changing HERMES_ACTIVE_PROFILE. Cached reference embeddings,
  fade-in smoothing, fully tunable via env vars.
version: 0.3.0
author: mataanek
tags:
  - tts
  - voice
  - local
  - neutts
  - voice-cloning
  - multi-profile
enabled: true
---

# hermes-neutts-voice

Provides a local cloned TTS voice for Hermes using NeuTTS Air.
Profile-agnostic: each voice profile lives under `~/.hermes/profiles/<name>/`
with its own `ref_codes.pt`. Switch profiles via `HERMES_ACTIVE_PROFILE`.

Reference embeddings are cached once per profile; each TTS call only runs
inference, keeping latency reasonable on CPU.

## Quick setup

1. Install deps and NeuTTS into Hermes venv — see README.md.
2. Place reference WAV at `~/.hermes/profiles/<profile>/<profile>.wav`.
3. Run `cache_neutts_ref.py` once per profile with `HERMES_ACTIVE_PROFILE`
   and `NEUTTS_REF_TEXT` set.
4. Set `tts.provider: custom_neutts` in `config.yaml` with the command
   block pointing to `hermes_neutts_tts.py`.
5. Restart Hermes.

## Switching profiles

Set `HERMES_ACTIVE_PROFILE=<name>` in the `command:` block in
`config.yaml`. See README.md for full details.

## Tuning

See README.md for the full env var reference table.

### TTS Input Formatting
For natural-sounding speech, avoid using emotional tags like *whispers*, *moans*, *etc.* in the input text, as they will be spoken literally by the TTS engine. Instead, convey emotion through natural phrasing, punctuation, and context.

## Troubleshooting

### Audio not playing inline in chat
If you're not hearing the audio directly in your chat interface (seeing it as a file attachment instead of an inline voice note):
- The TTS system is working correctly - it generates the audio and returns the proper `[[audio_as_voice]]` media tag that tells Hermes-compatible platforms to display it as a playable voice bubble.
- This behavior depends on your client/platform (Telegram, web UI, etc.) - some may still treat voice notes as attachments.
- To verify the system is working: check that the response contains `[[audio_as_voice]]` followed by `MEDIA:/path/to/file.ogg` (or .wav/.mp3 depending on your output_format setting).
- The voice_compatible flag is set to true in the config, which is required for inline playback in supported platforms.
- For platform-specific quirks (e.g., Telegram), see references/telegram.md.

### Profile files not found
If you see errors like "Reference audio not found at: /home/mataanek/.hermes/home/.hermes/profiles/nix/nix.wav" or "Reference codes not found at: .../ref_codes.pt":
- The skill expects profile data under `~/.hermes/profiles/<profile>/`.
- Ensure the directory `~/.hermes/profiles/<profile>/` exists (create it if needed).
- Place a reference audio file named `<profile>.wav` (e.g., `nix.wav`) in that directory.
- Run the caching script: `hermes run mlops/hermes-neutts-voice.cache_neutts_ref` (or directly execute `~/.hermes/skills/mlops/hermes-neutts-voice/scripts/cache_neutts_ref.py` with `HERMES_ACTIVE_PROFILE=<profile>` set).
- See `references/profile_setup.md` for detailed steps.

### Format selection
- The TTS provider supports ogg, wav, and mp3 output formats via the `output_format` setting in `custom_neutts` config.
- All formats should work for inline playback where supported - choose based on your platform's preferences and your quality/size needs.
- Remember to restart Hermes after changing output_format.

### Reference text mismatch
If you see "NeuTTS synthesis failed: Error: reference text not found" in the error:
- Ensure `tts.neutts.ref_text` in config.yaml exactly matches the transcript used when running `cache_neutts_ref.py`
- The reference text is case-sensitive and must include exact punctuation
- To fix: either update the ref_text in config.yaml to match your reference audio transcript, or re-run `cache_neutts_ref.py` with the correct transcript

### Incorrect profile directory resolution
If you see errors like "Reference codes not found at: /home/mataanek/.hermes/home/.hermes/profiles/nix/ref_codes.pt" (note the extra `.hermes` in the path):
- This happens when the HOME environment variable is set to a non-standard location (e.g., HOME=/home/mataanek/.hermes/home)
- The TTS scripts use `os.path.expanduser("~/.hermes/profiles")` which resolves to $HOME/.hermes/profiles
- To fix: Set `HERMES_PROFILES_DIR=/home/mataanek/.hermes/profiles` in your environment before running the TTS command
- Example: `HERMES_PROFILES_DIR=/home/mataanek/.hermes/profiles HERMES_ACTIVE_PROFILE=nix /path/to/hermes_neutts_tts.py input.txt output.wav`

### IndexError: list index out of range in _to_phones
If you see an IndexError in the TTS provider's `_to_phones` method (from the neutts package) with the message:
`IndexError: list index out of range`
This is because the reference text passed to the NeuTTS infer function is an empty string, which causes the phonemizer to fail.
To fix this, change the call in `hermes_neutts_tts.py` to pass a single space (`" "`) instead of an empty string (`""`) as the ref_text.

Note: The comment in the script says that passing ref_text is intentional to avoid speaking the reference transcript, but we found that an empty string causes a crash. A space is sufficient to avoid the crash and does not produce any audible output.