#!/usr/bin/env bash
# OpenRGB installation script for the openrgb-control skill
set -euo pipefail

echo "=== Setting up OpenRGB control from WSL ==="

# Check if we are in WSL
if ! grep -q Microsoft /proc/version 2>/dev/null; then
  echo "Warning: This script is intended for WSL2. Continuing anyway..."
fi

# Common locations for OpenRGB on Windows
WIN_PATHS=(
  "/mnt/c/Program Files/OpenRGB/openrgb.exe"
  "/mnt/c/Program Files (x86)/OpenRGB/openrgb.exe"
  "/mnt/c/OpenRGB/openrgb.exe"
  "/mnt/c/Users/$USERNAME/AppData/Local/OpenRGB/openrgb.exe"
)

# Try to find the binary
FOUND_BINARY=""
for path in "${WIN_PATHS[@]}"; do
  if [[ -x "$path" ]]; then
    FOUND_BINARY="$path"
    break
  fi
done

if [[ -z "$FOUND_BINARY" ]]; then
  echo "Could not find OpenRGB binary automatically."
  echo "Please install OpenRGB on Windows from:"
  echo "  https://github.com/CalcProgrammer1/OpenRGB/releases"
  echo
  echo "Enter the full Windows path to openrgb.exe (e.g., /mnt/c/Program Files/OpenRGB/openrgb.exe):"
  read -r USER_PATH
  if [[ -x "$USER_PATH" ]]; then
    FOUND_BINARY="$USER_PATH"
  else
    echo "Error: '$USER_PATH' is not executable or does not exist."
    exit 1
  fi
fi

echo "Found OpenRGB binary at: $FOUND_BINARY"

# Ask user how they want to access it from WSL
echo
echo "Choose how to access OpenRGB from WSL:"
echo "1) Create a symlink in /usr/local/bin/openrgb (requires sudo)"
echo "2) Add an alias to ~/.bashrc"
echo "3) Just show me the path and I'll handle it myself"
read -p "Enter choice [1-3]: " CHOICE

case "$CHOICE" in
  1)
    # Symlink method
    if [[ -e /usr/local/bin/openrgb ]]; then
      echo "Symlink already exists at /usr/local/bin/openrgb"
      read -p "Overwrite? [y/N]: " OVERWRITE
      if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo "Keeping existing symlink."
      else
        sudo rm /usr/local/bin/openrgb
        sudo ln -s "$FOUND_BINARY" /usr/local/bin/openrgb
        echo "Symlink updated."
      fi
    else
      sudo ln -s "$FOUND_BINARY" /usr/local/bin/openrgb
      echo "Symlink created at /usr/local/bin/openrgb"
    fi
    echo "You can now run: openrgb --listdevices"
    ;;
  2)
    # Alias method
    ALIAS_LINE="alias openrgb='$FOUND_BINARY'"
    if grep -q "alias openrgb=" ~/.bashrc 2>/dev/null; then
      echo "Alias for openrgb already exists in ~/.bashrc"
      read -p "Overwrite? [y/N]: " OVERWRITE
      if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo "Keeping existing alias."
      else
        # Replace the line
        sed -i "s|^alias openrgb=.*|$ALIAS_LINE|" ~/.bashrc
        echo "Alias updated in ~/.bashrc"
      fi
    else
      echo "" >> ~/.bashrc
      echo "# OpenRGB alias" >> ~/.bashrc
      echo "$ALIAS_LINE" >> ~/.bashrc
      echo "Alias added to ~/.bashrc"
    fi
    echo "Run 'source ~/.bashrc' or restart your terminal to use: openrgb --listdevices"
    ;;
  3)
    echo "Remember to use the path: $FOUND_BINARY"
    echo "Example: $FOUND_BINARY --listdevices"
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac

echo
echo "Testing the binary..."
if command -v openrgb >/dev/null 2>&1 || [[ -x "$FOUND_BINARY" ]]; then
  # Use the binary we found
  if "$FOUND_BINARY" --listdevices >/dev/null 2>&1; then
    echo "Success! OpenRGB is working and detected devices."
  else
    echo "Warning: The binary ran but did not list devices. Check your hardware connection."
  fi
else
  echo "Error: Could not run OpenRGB binary. Check permissions and path."
fi

echo
echo "Setup complete. Refer to the skill documentation for usage and cron scheduling."