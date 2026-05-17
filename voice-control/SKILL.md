---
name: voice-control
description: "Implements wake word detection, speech-to-text, intent parsing, and text-to-speech for voice-controlled home automation"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [voice, audio, wake-word, speech-to-text, text-to-speech, home-automation]
    related_skills: [hermes-neutts-voice, smart-home, agent-soul-md-update]
---

# Voice Control Skill

Implements a complete voice control pipeline for Hermes agent with wake word detection, speech-to-text, intent processing, and text-to-speech response.

## Overview

This skill provides always-on voice control capability for the Hermes agent, enabling hands-free interaction through:
- Wake word detection (using openWakeWord)
- Speech-to-text transcription (using Whisper)
- Natural language command processing
- Text-to-speech response (using Hermes neuTTS)
- Integration with home automation systems (Hue lights, Daikin AC, Netatmo weather)

## Features

- **Wake Word Detection**: Uses openWakeWord with customizable wake word models
- **Speech Recognition**: Employs Whisper for accurate offline transcription
- **Intent Processing**: Matches commands to home control actions and agent responses
- **Home Automation Integration**: Controls lights, climate, and retrieves weather data
- **Text-to-Speech**: Utilizes Hermes neuTTS for natural-sounding responses
- **Audio Pipeline**: Manages microphone input and audio output via PyAudio

## Implementation

This skill includes executable tools in the `scripts/` directory:
- `scripts/voice_control_main.py`: Main voice control pipeline with wake word detection, STT, intent processing, and TTS
- `scripts/test_components.py`: Component testing script for development and troubleshooting

The tools are automatically registered when the skill is loaded and provide the `/voice-control` command functionality.

## Installation

The skill is installed as part of the Hermes agent skills package. Ensure the following system dependencies are available:

```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get install -y portaudio19-dev python3-pyaudio ffmpeg

# Python dependencies (installed via skill)
pip install openwakeword whisper numpy pyaudio
```

## Usage

The voice control pipeline runs as a continuous background process:

```bash
# Start the voice control pipeline
hermes skill run voice-control
```

Or trigger it manually from within the agent:

```python
# In Hermes agent context
from skills.voice_control.scripts.voice_control_main import VoiceControlPipeline
pipeline = VoiceControlPipeline()
pipeline.run()
```

## Configuration

### Wake Word Models

By default, uses "hey_mycroft_v0.1" model. To change wake words:

1. Edit `voice_control_main.py` line 57:
   ```python
   wakeword_models=[\"hey_jasmine_v0.1\", \"alexa_v0.1\"]  # Available models
   ```

2. Available pre-trained models include:
   - hey_mycroft_v0.1
   - hey_jasmine_v0.1  
   - alexa_v0.1
   - ok_google_v0.1
   - pico_v0.1
   - snowboy variants

### Audio Settings

Adjust in `voice_control_main.py`:
- `CHUNK`: Audio buffer size (default 1024)
- `FORMAT`: Audio format (default paInt16)
- `CHANNELS`: Audio channels (default 1 for mono)
- `RATE`: Sample rate (default 16000 Hz)

### Command Processing

Customize command responses in `process_command()` method:
- Add new `elif` blocks for additional intents
- Modify response strings for personalized interactions
- Extend home control integrations via Hermes registry

## Home Control Integrations

The skill connects to Hermes registry for device control:

### Hue Lights
- `hue_set_light`: Control individual lights
- `hue_get_lights`: Retrieve light status
- Example command: "Turn on the lights"

### Daikin AC
- `daikin_set_temperature`: Set target temperature
- `daikin_get_info`: Retrieve current AC status
- Example command: "Set temperature to 22 degrees"

### Netatmo Weather
- `netatmo_get_formatted_outdoor`: Outdoor conditions
- `netatmo_get_formatted_indoor`: Indoor conditions
- Example command: "What's the outside temperature?"

## Response Generation

Text-to-speech uses Hermes neuTTS system:
- Configured via `HERMES_ACTIVE_PROFILE` environment variable
- Uses reference audio clips for voice cloning
- Falls back to logging if TTS tools unavailable

## Limitations & Considerations

### Audio Quality
- Requires clear microphone input for reliable wake word detection
- Background noise may affect detection accuracy
- Recommended: Use directional microphone or headset in noisy environments

### Latency
- Wake word detection: Near real-time
- Speech-to-text: 1-3 seconds depending on utterance length
- TTS generation: Depends on neuTTS model size
- Total pipeline latency: Typically 2-4 seconds from wake word to response

### Privacy
- All audio processing occurs locally
- No audio leaves the device unless explicitly configured
- Wake word detection uses local onnx models

### Apple Home Integration
**Note**: This skill implements local voice control. For Apple HomePod/HomeKit integration:
- See ideation: `/home/mataanek/.hermes/wiki/ideation/home-speaker.md`
- Requires separate AirPlay streaming solution for speaker output
- Microphone input from HomePods requires workaround due to Apple restrictions
- Consider using this skill as the "brain" with AirPlay for audio I/O

## Troubleshooting

### Common Issues

1. **"No module named 'openwakeword'"**
   ```bash
   pip install openwakeword
   ```

2. **Audio device not found**
   - Check microphone permissions
   - Verify PyAudio installation: `pip install pyaudio`
   - Test with: `python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"`

3. **Whisper model loading slow**
   - First download caches model (~75MB for tiny)
   - Subsequent loads are faster
   - Consider using `base` or `small` models for better accuracy (more RAM)

4. **No TTS output**
   - Verify neuTTS voice skill is installed: `hermes skills list | grep neutts`
   - Check `HERMES_ACTIVE_PROFILE` environment variable
   - Ensure reference audio exists for active profile

### Performance Tuning

- For lower latency: Use smaller Whisper model (`tiny` instead of `base`)
- For better accuracy: Use `small` or `medium` Whisper model (more RAM/CPU)
- Adjust wake word confidence threshold (line 104 in voice_control_main.py)
- Increase `CHUNK size` for more stable audio (increases latency)

## Related Skills

- `hermes-neutts-voice`: Provides the TTS backbone for voice responses
- `smart-home`: Framework for home device integrations
- `agent-soul-md-update`: For updating agent personalities

## Example Interaction

1. User says: "Hey Mycroft" (wake word)
2. System responds with acknowledgment beep (optional)
3. User says: "What's the temperature outside?"
4. System transcribes: "what's the temperature outside?"
5. System queries Netatmo via registry
6. System responds: "Outside it's 22°C with 65% humidity."
7. System speaks response via neuTTS
8. System returns to listening for wake word

## Maintenance

- Periodically update openWakeWord and Whisper models
- Check for Hue/Daikin/Netatmo API changes
- Monitor audio levels in different environments
- Test wake word detection with various accents/noise levels

## Security

- All processing is local - no audio streaming to external services
- Wake word models are locally stored onnx files
- Home control actions go through Hermes registry with proper authentication
- Consider restricting microphone access to trusted users only in shared environments

## Apple HomePod Integration (Speaker Output)

While this skill provides local voice control, integrating with Apple HomePods for speaker output requires additional work due to Apple's restrictions on direct third-party access.

- **Speaker Output via RAOP/AirPlay**: The HomePods expose both RAOP (Remote Audio Output Protocol) and AirPlay services on port 7000. Using a Windows host as a relay avoids mDNS discovery issues in WSL2.
  - **Implementation**: Use the `pyatv` library to discover HomePods and initiate a stream via either RAOP or AirPlay. Audio files (e.g., TTS output) can be sent to the shared folder between the Hermes agent (WSL2) and the Windows host, where a script reads the file and streams it to the selected HomePod.
  - **Key Discoveries from Testing**:
      * `atv.stream.get(Protocol.RAOP)` returns a `RaopStream` object
      * `atv.stream.get(Protocol.AirPlay)` returns an `AirPlayStream` object
      * The stream object has multiple instances: `[AirPlayStream, RaopStream]`
      * Both streamers support `stream_file()` method for WAV files
      * RAOP streamer also supports `write()` method for raw PCM data (after stripping WAV header)
  - **Prerequisites**: 
      * Windows host with Python and `pyatv` installed (version 0.17.0 or later).
      * Shared folder accessible from both WSL2 and Windows (e.g., `/mnt/c/Users/<username>/Shared/NixTTS`).
      * ffmpeg for audio format conversion to PCM WAV (16-bit, 44.1kHz, stereo).
  - **Current State**: Prototype scripts exist to test streaming:
      * `stream_via_raop.py` - Streams via RAOP using PCM WAV conversion
      * `stream_via_main_instance.py` - Streams via the main instance (AirPlay)
      * `test_raop_streamer.py` - Tests RAOP streamer capabilities

- **Microphone Input**: Apple does not allow third‑party access to HomePod microphones. Possible workarounds (not implemented in this skill) include:
  - Using a Siri proxy to capture audio after "Hey Siri" (security and ToS concerns).
  - Routing iPhone/iPad microphone via a Shortcut that sends text to Hermes (loses ambient whole‑house feel).
  - Using a dedicated always‑on mic (e.g., Raspberry Pi with ReSpeaker) placed in the room.

For detailed ideation, assumptions, and prototype logs, see:
  `/home/mataanek/.hermes/wiki/ideation/home-speaker.md`

See also the reference file `references/home-speaker-ideation.md` for a condensed version of the ideation and session-specific notes.

### Audio Streaming Troubleshooting

- **Permission Denied when executing scripts from Windows mount**: 
    When trying to run Python scripts located in the WSL2 filesystem from Windows (e.g., via a shared mount), you may encounter permission errors due to the mount options not granting execute permission.
    **Fix**: Copy the script to the Windows filesystem (e.g., to the shared folder) and run it from there, or adjust the mount options in WSL2 to include the execute flag.

- **Incorrect RAOP service import**: 
    The `pyatv` library uses `RaopService` (not `RAOPService`) for the RAOP service type.
    **Fix**: Import `RaopService` from `pyatv.conf`.

- **Streaming via stream_file() fails with NotSupportedError**: 
    Some streamer objects (like AirPlayStream) may raise NotSupportedError when calling stream_file().
    **Fix**: Try using the main instance (`atv.stream.main_instance`) or the specific streamer obtained via `get()`.

- **Connection timeouts during RTSP SETUP**: 
    Occurs when initializing RAOP stream. Ensure Windows host is on same network as HomePods, no firewall blocks on port 7000 (TCP), and verify discoverability via `pyatv` scan.

- **Streaming raw PCM data**: 
    When using the `write()` method on RAOP streamer, you must strip the WAV header (44 bytes) from PCM WAV files before sending the raw PCM data.

- **Audio format requirements**: 
    HomePods expect PCM audio at 44.1kHz, 16-bit, stereo. Use ffmpeg to convert:
    ```bash
    ffmpeg -y -i input.mp3 -ar 44100 -ac 2 -f wav -acodec pcm_s16le output.wav
    ```
    Or via WSL from Windows:
    ```bash
    wsl /usr/bin/ffmpeg -y -i /mnt/c/path/to/input.mp3 -ar 44100 -ac 2 -f wav -acodec pcm_s16le /mnt/c/path/to/output.wav
    ```

## References

- `references/home-speaker-ideation.md` – Condensed ideation and assumptions for Apple HomePod integration (see full ideation at `/home/mataanek/.hermes/wiki/ideation/home-speaker.md`).