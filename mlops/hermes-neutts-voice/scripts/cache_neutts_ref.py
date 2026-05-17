#!/usr/bin/env python3
"""
cache_neutts_ref.py — One-time setup: encode reference WAV → ref_codes.pt.
Re-run only when you change your reference audio, transcript, or model.

Usage:
    HERMES_ACTIVE_PROFILE=nix \
    NEUTTS_REF_AUDIO=~/.hermes/profiles/nix/nix.wav \
    NEUTTS_REF_TEXT="Your exact transcript here." \
    ~/.hermes/hermes-agent/venv/bin/python cache_neutts_ref.py
"""
import os
import torch
from neuttsair.neutts import NeuTTSAir

# ─── Profile resolution ────────────────────────────────────────────────────
HERMES_PROFILES_DIR = os.environ.get(
    "HERMES_PROFILES_DIR",
    os.path.expanduser("~/.hermes/profiles")
)
ACTIVE_PROFILE = os.environ.get("HERMES_ACTIVE_PROFILE", "nix")
PROFILE_DIR    = os.path.join(HERMES_PROFILES_DIR, ACTIVE_PROFILE)

# ─── Tunable config ────────────────────────────────────────────────────────
REF_AUDIO  = os.environ.get(
    "NEUTTS_REF_AUDIO",
    os.path.join(PROFILE_DIR, f"{ACTIVE_PROFILE}.wav")
)
REF_TEXT   = os.environ.get(
    "NEUTTS_REF_TEXT",
    "and when it's good, you can't enjoy it too much because it means that when it's bad, you're going to be devastated. So I try not to enjoy it too much, so I take it with a big grain of salt and just live my life and and focus in on my next projects"  # must be provided via env var or edited here
)
CODES_PATH = os.environ.get(
    "NEUTTS_CODES_PATH",
    os.path.join(PROFILE_DIR, "ref_codes.pt")
)
BACKBONE   = os.environ.get("NEUTTS_BACKBONE_REPO", "neuphonic/neutts-air-q4-gguf")
CODEC      = os.environ.get("NEUTTS_CODEC_REPO",    "neuphonic/neucodec")
DEVICE     = os.environ.get("NEUTTS_DEVICE",        "cpu")
# ───────────────────────────────────────────────────────────────────────────

if not REF_TEXT.strip():
    print(
        "ERROR: NEUTTS_REF_TEXT is empty. "
        "Set it via env var to the exact transcript of your reference WAV.",
        file=__import__("sys").stderr,
    )
    __import__("sys").exit(1)

if not os.path.exists(REF_AUDIO):
    print(
        f"ERROR: Reference audio not found at: {REF_AUDIO}",
        file=__import__("sys").stderr,
    )
    __import__("sys").exit(1)

print(f"Profile      : {ACTIVE_PROFILE}")
print(f"Profile dir  : {PROFILE_DIR}")
print(f"Ref audio    : {REF_AUDIO}")
print(f"Codes output : {CODES_PATH}")
print(f"Device       : {DEVICE}")
print()

tts = NeuTTSAir(
    backbone_repo=BACKBONE,
    backbone_device=DEVICE,
    codec_repo=CODEC,
    codec_device=DEVICE,
)

print("Encoding reference audio...")
ref_codes = tts.encode_reference(REF_AUDIO)

torch.save(
    {
        "ref_codes":   ref_codes,
        "ref_text":    REF_TEXT,
        "profile":     ACTIVE_PROFILE,
        "ref_audio":   REF_AUDIO,
        "backbone":    BACKBONE,
    },
    CODES_PATH,
)
print(f"Done. Saved reference codes to: {CODES_PATH}")