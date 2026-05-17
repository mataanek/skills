#!/usr/bin/env bash
set -euo pipefail

LOGDIR="/home/mataanek/.hermes/wiki/personal"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
UPTIME=$(uptime -p | sed 's/up //')
LOAD=$(cat /proc/loadavg)

for file in nix-status.md mataanek-profile.md; do
    {
        echo -e "\n---\n*Updated:* $TIMESTAMP"
        echo "*Uptime:* $UPTIME"
        echo "*Load average:* $LOAD"
    } >> "$LOGDIR/$file"
done