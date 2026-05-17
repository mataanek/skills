# Troubleshooting Guide for hermes-neutts-voice

## Audio not playing inline in chat
If you're not hearing the audio directly in your chat interface (seeing it as a file attachment instead of an inline voice note):
- The TTS system is working correctly - it generates the audio and returns the proper `[[audio_as_voice]]` media tag that tells Hermes-compatible platforms to display it as a playable voice bubble.
- This behavior depends on your client/platform (Telegram, web UI, etc.) - some may still treat voice notes as attachments.
- To verify the system is working: check that the response contains `[[audio_as_voice]]` followed by `MEDIA:/path/to/file.ogg` (or .wav/.mp3 depending on your output_format setting).
- The voice_compatible flag is set to true in the config, which is required for inline playback in supported platforms.

## Format selection
- The TTS provider supports ogg, wav, and mp3 output formats via the `output_format` setting in `custom_neutts` config.
- All formats should work for inline playback where supported - choose based on your platform's preferences and your quality/size needs.
- Remember to restart Hermes after changing output_format.

## Common installation issues
### "NeuTTS synthesis failed: Error: reference text not found"
This error occurs when the reference text in your config doesn't exactly match what was used during reference encoding.
- Ensure `tts.neutts.ref_text` in config.yaml exactly matches the transcript used when running `cache_neutts_ref.py`
- The reference text is case-sensitive and must include exact punctuation
- Example mismatch: "I was traveling..." vs "I was traveling from Tel Aviv to LA for a job, and when I landed they told me I got it."

### ModuleNotFoundError: No module named 'neutts'
- Ensure NeuTTS is installed in the Hermes agent venv: `~/.hermes/hermes-agent/venv/bin/python -m pip install -U neutts[all]`
- Also install system dependencies: `sudo apt-get install -y ninja-build espeak-ng`
- Verify installation: `/home/mataanek/.hermes/hermes-agent/venv/bin/python3 -c "import neutts; print('NeuTTS imported')"` should succeed

### Audio sounds choppy or has harsh starts
- Adjust `NEUTTS_FADE_MS` environment variable (default 150ms) - increase for smoother start
- Adjust `NEUTTS_PAD_MS` environment variable (default 100ms) - increase for more leading silence
- These can be set inline in the command in config.yaml, e.g.:
  `command: > NEUTTS_FADE_MS=200 NEUTTS_PAD_MS=150 /path/to/hermes_neutts_tts.py {input_path} {output_path}`