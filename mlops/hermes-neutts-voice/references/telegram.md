# Telegram Voice Note Behavior

## Issue
Telegram sometimes displays voice notes as file attachments instead of inline playable bubbles, even when the proper `[[audio_as_voice]]` MEDIA: tag is present.

## Observed Behavior
- Audio files are correctly generated and tagged
- User receives the file as an attachment that must be tapped to play
- Inline playback does not occur automatically

## Workarounds
1. User must tap the attachment to play the audio
2. Alternative: Convert to different format (WAV/MPM) if OGG has issues
3. Send raw file and let user play manually via file manager

## Notes
- This appears to be a Telegram client-side rendering issue
- The TTS system and tagging are functioning correctly
- Same audio works inline in other platforms/web UI
- Consider providing both tagged version and raw file for flexibility

## Verification
To confirm TTS is working: check for `[[audio_as_voice]]\nMEDIA:/path/to/file.ogg` in the response.