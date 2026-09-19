#!/usr/bin/env bash
# Blockliner setup - creates a venv and installs everything needed to run.
# Usage: ./setup_venv.sh
set -e

# tkinter is a separate OS package, not pip-installable - install it first
# if it's missing (only needed once per machine).
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "tkinter not found - installing it (needs sudo)..."
    if command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3-tkinter
    elif command -v apt >/dev/null 2>&1; then
        sudo apt install -y python3-tk
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --noconfirm tk
    else
        echo "Could not detect your package manager - install tkinter manually, then re-run this script."
        exit 1
    fi
fi

python3 -m venv venv
venv/bin/pip install --upgrade pip -q
venv/bin/pip install -r requirements.txt -q

echo ""
echo "Done. Run Blockliner with:"
echo "  venv/bin/python main.py"
