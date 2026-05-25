# Verification Commands for Hermes NeuTTS Voice

These commands were successfully used to generate clear TTS audio in a session where the user reported muffled/gibberish output.

## Prerequisites
- Reference audio (`nix.wav`) and reference codes (`ref_codes.pt`) must exist in the profile directory.
- The `hermes-neutts-voice` skill must be loaded/available.

## Environment Variables
When invoking the TTS script directly (not via Hermes' built-in TTS tool), ensure these are set:

```bash
export HERMES_ACTIVE_PROFILE=nix
export HERMES_PROFILES_DIR=/home/mataanek/.hermes/profiles  # Adjust if your profiles are elsewhere
export NEUTTS_OUTPUT_FORMAT=mp3  # or wav/ogg as preferred
```

## Successful Command
```bash
/home/mataanek/.hermes/hermes-agent/venv/bin/python \
  /home/mataanek/.hermes/skills/mlops/hermes-neutts-voice/scripts/hermes_neutts_tts.py \
  input.txt output.mp3
```

Where `input.txt` contains the text to synthesize (normalized by the script) and `output.mp3` is the desired output file.

## Troubleshooting Tips
1. If you see "Reference codes not found", verify:
   - The profile directory exists: `$HERMES_PROFILES_DIR/$HERMES_ACTIVE_PROFILE`
   - `ref_codes.pt` and `<profile>.wav` are present
   - Run `cache_neutts_ref.py` first if missing

2. If audio is muffled or unclear:
   - Check that the reference text in `ref_codes.pt` matches what was used during caching
   - Ensure the input text is not empty or only whitespace
   - Try a different `NEUTTS_OUTPUT_FORMAT` (some platforms handle wav better than mp3)

3. For inline playback in Telegram:
   - The script must return an exit code of 0
   - The output must be in a supported format (ogg often works best for Telegram voice notes)
   - The `voice_compatible: true` flag must be set in config.yaml under `tts.custom_neutts`

## Example Full Session
```bash
# Set environment
export HERMES_ACTIVE_PROFILE=nix
export HERMES_PROFILES_DIR=/home/mataanek/.hermes/profiles
export NEUTTS_OUTPUT_FORMAT=mp3

# Create test file
echo "Bambu Lab, maker of popular 3D printers, ignited a firestorm..." > test.txt

# Generate audio
/home/mataanek/.hermes/hermes-agent/venv/bin/python \
  /home/mataanek/.hermes/skills/mlops/hermes-neutts-voice/scripts/hermes_neutts_tts.py \
  test.txt output.mp3

# Verify output
ls -lh output.mp3  # Should be non-zero size
```