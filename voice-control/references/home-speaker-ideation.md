# Apple HomePod Integration Ideation (Condensed)

See the full ideation at: `/home/mataanek/.hermes/wiki/ideation/home-speaker.md`

## Goal
Enable Nix to send and receive audio via Apple HomePods for seamless voice interaction (hands‑free, ambient computing).

## Key Challenges
- Apple does not allow third‑party access to HomePod microphones (only Siri is authorized).
- AirPlay output may introduce latency and buffering; multicast DNS (mDNS) may not work in WSL2 without configuration.
- Any workaround may break with Apple OS updates and carries maintenance overhead.

## Approaches Explored

### Audio Output (Speaker)
- **AirPlay Streaming**: Use `shairport-sync`, `pyatv`, or `ffmpeg` + `paplay` to stream TTS audio to HomePod.
- **Siri Shortcuts + Webhooks**: Indirect, uses Siri's voice, requires exposed webhook.
- **HomeBridge Plugin**: Requires maintaining a separate hub; potential compatibility breaks.

### Audio Input (Microphone)
- **Siri Proxy (MITM)**: Security risks, actively blocked by Apple, violates ToS.
- **HomePod as AirPlay Mic Receiver**: Not supported; HomePods do not expose mic streams via AirPlay.
- **Fallback to Phone/Watch**: User invokes Siri on iPhone/Apple Watch; loses ambient whole‑house feel.
- **Dedicated Always‑On Mic**: Raspberry Pi + ReSpeaker (or similar) placed in room; defeats purpose of using existing HomePods but is reliable and compliant.

## Integration Layer
Lightweight middleware on an always‑on device (Mac, Linux box, or Pi) that:
- Exposes a local API for Hermes to send text (for TTS output via AirPlay).
- Listens for audio triggers (from workaround mic sources) and forwards text to Hermes.
- Handles state (e.g., “listening mode”, volume control).

## Safety & Privacy
- Prioritize local processing; no audio should leave the home network unencrypted.
- Any solution must encrypt audio in transit if leaving the device (though local-only is preferred).

## User Experience
- True duplex conversation is hard due to latency and half‑duplex limitations.
- Push‑to‑talk or defined interaction phrases may be more realistic than fully ambient.

## Next Steps (from ideation)
1. Research current state of `pyatv`, `shairport-sync`, and HomeBridge speaker plugins.
2. Prototype TTS output to HomePod via `ffmpeg` + `paplay` (if PulseAudio supports AirPlay) or `aptx` tools.
3. Explore input alternatives: macOS accessibility features (if Mac available), dedicated always‑on mic.
4. Define interaction model: push‑to‑talk, wake‑word on alternative hardware, or Siri Shortcut‑triggered.
5. Document assumptions about sustainability given Apple’s restrictions.

## Assumptions & Sustainability (Updated 2026-05-17)
- Apple’s ecosystem does not permit third‑party mic access; mic‑based solutions are experimental and may break with OS updates.
- AirPlay output is viable but requires functional mDNS between agent and HomePod; latency ~200‑400 ms plus buffering.
- Local processing (wake word, STT, TTS) ensures privacy; no audio leaves the home unencrypted.
- Hardware fallback (e.g., Raspberry Pi + ReSpeaker) provides a stable, compliant platform (~$50‑$80).
- Maintenance overhead: monitor GitHub projects for updates to `pyatv`, `shairport-sync`, `openWakeWord`, `whisper`; schedule quarterly review.
- In WSL2, AirPlay discovery may require enabling multicast bridging or using the host’s network stack. Alternative: relay audio via shared folder to Windows host and use a Windows‑based AirPlay sender (e.g., iTunes, Airfoil, or open‑source `shairport-sync` on Windows).

## Related Files
- Full ideation: `/home/mataanek/.hermes/wiki/ideation/home-speaker.md`
- Voice control skill (local): `/home/mataanek/.hermes/skills/voice-control/`