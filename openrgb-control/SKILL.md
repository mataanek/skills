---
name: openrgb-control
description: Control PC RGB lighting via OpenRGB, including installation, CLI control, and scheduling with cron.
version: 0.2.0
author: Nix
---

# OpenRGB Control Skill

This skill provides a standardized way to install OpenRGB, control RGB lighting via command line, and schedule on/off times using cron.

## When to Use

- You need to turn PC RGB lights off at night and on in the morning.
- Your case only has a mechanical button to change lighting effects, not to power off.
- You prefer software control via OpenRGB.

## Prerequisites

- Linux system (WSL2) with access to USB/HID devices **is not reliable**; therefore install OpenRGB on the Windows host and access it from WSL via a symlink or alias.
- Windows host must have OpenRGB installed and the binary accessible.

## Installation

**Important**: OpenRGB requires direct access to USB/HID devices, which is not reliably available in WSL2. Therefore, install OpenRGB on the Windows host and access it from WSL.

### On Windows Host

1. Download the latest OpenRGB release (exe) from:
   https://github.com/CalcProgrammer1/OpenRGB/releases
2. Run the installer (or extract the portable folder) and note the installation path, e.g., `C:\Program Files\OpenRGB\openrgb.exe`.
3. Verify detection by opening a Windows command prompt and running:
   ```cmd
   "C:\Program Files\OpenRGB\openrgb.exe" --listdevices
   ```
   Adjust the path if you installed elsewhere.

### Access from WSL

Create a symlink or alias so you can run `openrgb` from WSL:

```bash
# Symlink (recommended)
sudo ln -s "/mnt/c/Program Files/OpenRGB/openrgb.exe" /usr/local/bin/openrgb

# OR alias (add to ~/.bashrc)
alias openrgb='/mnt/c/Program\\ Files/OpenRGB/openrgb.exe'
```

Then test from WSL:

```bash
openrgb --listdevices
```

You should see a list of controllers (motherboard, RAM, GPU, strips, etc.). If not, ensure your RGB hardware is plugged in and supported on Windows.

## Usage

A helper script `rgblightctl` is provided to turn lights on/off using the `openrgb` command.

### Create the control script

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/rgblightctl <<'EOF'
#!/usr/bin/env bash
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
EOF
chmod +x ~/.local/bin/rgblightctl
```

### Test

```bash
# Turn off
~/.local/bin/rgblightctl off
# On (white)
~/.local/bin/rgblightctl on
```

## Scheduling with Cron

To automate nightly off and morning on:

1. Edit your crontab:
   ```bash
   crontab -e
   ```

2. Add lines (adjust times as needed):
   ```cron
   # Turn RGB lights off at 22:00 daily
   0 22 * * * /home/mataanek/.local/bin/rgblightctl off >/dev/null 2>&1
   # Turn RGB lights on at 07:00 daily
   0 7 * * * /home/mataanek/.local/bin/rgblightctl on >/dev/null 2>&1
   ```

3. Save and exit. Cron will now handle the schedule.

## Troubleshooting

- **`openrgb: command not found`**: Ensure the symlink/alias is correctly set and points to the Windows OpenRGB binary. Verify the path exists: `ls -l /usr/local/bin/openrgb` or check your alias.
- **No devices listed**: Ensure your RGB controller is supported by OpenRGB (check the OpenRGB wiki). Some controllers need specific kernel modules or udev rules on Windows; the Windows app usually handles this.
- **Permission denied accessing USB/HID**: This is a Windows-side issue; ensure the Windows user running OpenRGB has access to the USB devices. Running OpenRGB once as administrator to install drivers may help.
- **Binary not found at symlink target**: Double-check the installation path on Windows and adjust the symlink/alias accordingly.

## References

- OpenRGB GitHub: https://github.com/CalcProgrammer1/OpenRGB
- OpenRGB releases (Codeberg): https://codeberg.org/OpenRGB/OpenRGB/releases

## Scripts

- `scripts/install_openrgb.sh` – script to set up symlink/alias and verify OpenRGB binary on Windows host.

## Templates

- `templates/cron_rgb.txt` – example cron entries.