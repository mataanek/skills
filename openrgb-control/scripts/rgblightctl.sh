#!/usr/bin/env bash
# OpenRGB light control script for the openrgb-control skill
# Provides simple on/off control via the openrgb command

case "$1" in
  off)
    openrgb --setcolor 0 0 0 --mode static
    ;;
  on)
    openrgb --setcolor 255 255 255 --mode static
    ;;
  *)
    echo "Usage: $0 {off|on}"
    exit 1
    ;;
esac