# hermes-neutts-voice

A Hermes Agent skill that provides a **local, cloned voice** for TTS using
[NeuTTS Air](https://github.com/neuphonic/neutts), with cached reference
embeddings and fade-in smoothing for natural-sounding speech output.

Fully **profile-agnostic**: switch voices by pointing at a different Hermes
profile directory — no code changes needed.

## Features

- **Voice cloning**: synthesize speech in any voice from a short reference
  WAV (5–10 seconds).
- **Profile-agnostic**: works with any Hermes voice profile; switch via
  `HERMES_ACTIVE_PROFILE`.
- **Cached reference embeddings**: vocal analysis runs once at setup, not
  on every TTS call.
- **Fade-in smoothing**: eliminates harsh or wobbly starts common in
  neural TTS models.
- **Fully local**: no cloud API, no data leaves your machine.
- **Tunable via env vars**: fade time, pad time, device, model repo, etc.

## Requirements

- Hermes Agent (v23+)
- WSL2 / Linux (Ubuntu 22.04 tested)
- Python 3.11 (Hermes venv)
- `ninja-build`, `espeak-ng` system packages
- ~4 GB disk (NeuTTS Air Q4 backbone + NeuCodec)

## Directory structure

```text
~/.hermes/profiles/
├── nix/
│   ├── nix.wav              # reference recording (setup only)
│   └── ref_codes.pt         # cached embedding (generated, do not commit)
├── jarvis/
│   ├── jarvis.wav
│   └── ref_codes.pt
└── ...

~/.hermes/skills/mlops/hermes-neutts-voice/
├── SKILL.md
├── README.md
└── scripts/
    ├── cache_neutts_ref.py  # run once per profile
    └── hermes_neutts_tts.py # called by Hermes per TTS reply
```

## Installation

### 1. Install system dependencies

```bash
sudo apt-get update
sudo apt-get install -y ninja-build espeak-ng
```

### 2. Install NeuTTS into Hermes venv

```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install -U neutts[all]
```

### 3. Place your reference audio

Record a clean mono WAV (16–44 kHz, 5–10 s, no background noise) and
place it at:

```bash
~/.hermes/profiles/<profile_name>/<profile_name>.wav
```


Note the **exact transcript** of what you say in that clip.

### 4. Generate cached reference codes (once per profile)

```bash
HERMES_ACTIVE_PROFILE=nix \
NEUTTS_REF_TEXT="Your exact transcript here." \
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/mlops/hermes-neutts-voice/scripts/cache_neutts_ref.py
```

This produces `~/.hermes/profiles/nix/ref_codes.pt`.
Re-run only if you change the reference audio, transcript, or model.

### 5. Configure Hermes

In `~/.hermes/config.yaml`:

```yaml
tts:
  provider: custom_neutts
  speed: 1.0

  custom_neutts:
    type: command
    command: >
      HERMES_ACTIVE_PROFILE=nix
      /home/you/.hermes/hermes-agent/venv/bin/python
      /home/you/.hermes/skills/mlops/hermes-neutts-voice/scripts/hermes_neutts_tts.py
      {input_path} {output_path}
    output_format: wav
    timeout: 300
    voice_compatible: true

voice:
  auto_tts: true
```

### 6. Restart Hermes

```bash
hermes server
```

## Switching voice profiles

To use a different voice, generate its `ref_codes.pt` first:

```bash
HERMES_ACTIVE_PROFILE=jarvis \
NEUTTS_REF_TEXT="Your jarvis transcript here." \
~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/mlops/hermes-neutts-voice/scripts/cache_neutts_ref.py
```

Then update `HERMES_ACTIVE_PROFILE` in your `config.yaml` command block:

```yaml
command: >
  HERMES_ACTIVE_PROFILE=jarvis
  /home/you/.hermes/hermes-agent/venv/bin/python
  /home/you/.hermes/skills/mlops/hermes-neutts-voice/scripts/hermes_neutts_tts.py
  {input_path} {output_path}
```

## Configuration reference (env vars)

| Variable | Default | Description |
|---|---|---|
| `HERMES_PROFILES_DIR` | `~/.hermes/profiles` | Root profiles directory |
| `HERMES_ACTIVE_PROFILE` | `nix` | Active voice profile name |
| `NEUTTS_CODES_PATH` | `<profiles_dir>/<profile>/ref_codes.pt` | Override codes path |
| `NEUTTS_BACKBONE_REPO` | `neuphonic/neutts-air-q4-gguf` | HuggingFace backbone |
| `NEUTTS_CODEC_REPO` | `neuphonic/neucodec` | HuggingFace codec |
| `NEUTTS_DEVICE` | `cpu` | `cpu` or `cuda` |
| `NEUTTS_SAMPLE_RATE` | `24000` | Output sample rate (Hz) |
| `NEUTTS_FADE_MS` | `150` | Fade-in length (ms) |
| `NEUTTS_PAD_MS` | `100` | Leading silence pad (ms) |
| `NEUTTS_REF_AUDIO` | `<profile_dir>/<profile>.wav` | Override ref WAV path |
| `NEUTTS_REF_TEXT` | *(required for cache script)* | Reference transcript |
| `NEUTTS_SENTENCE_GAP_MS` | `250` | Silence between synthesized sentences (ms) |

## .gitignore

Add these to avoid committing large binary or personal files:
profiles/*/ref_codes.pt
profiles//.wav

## How it works

1. **Setup** (`cache_neutts_ref.py`): loads NeuTTS, encodes your reference
   WAV into a speaker embedding tensor, saves it to the profile dir as
   `ref_codes.pt`.
2. **Per call** (`hermes_neutts_tts.py`): loads the cached embedding (no
   re-encoding), runs NeuTTS inference on the reply text, applies fade-in
   and silence pad, writes a WAV for Hermes to play.

## Credits

- [NeuTTS / Neuphonic](https://github.com/neuphonic/neutts) — voice cloning model
- [Hermes Agent](https://github.com/hermesagent) — AI agent framework

## License

MIT