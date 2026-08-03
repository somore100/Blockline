#!/usr/bin/env bash
# Blockline - venv setup (Linux / macOS)
#
# Usage:
#   chmod +x setup_venv.sh
#   ./setup_venv.sh
#
# Then activate with:
#   source venv/bin/activate

set -e

echo "============================================================"
echo " Blockline - Setting up virtual environment (Linux/macOS)"
echo "============================================================"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" &> /dev/null; then
    echo "✗ $PYTHON_BIN not found. Install Python 3.10+ first."
    exit 1
fi

echo "✓ Using $($PYTHON_BIN --version)"

# tkinter ships as a separate system package on most Linux distros -
# pip cannot install it, so check it explicitly and warn instead of
# failing halfway through the venv build.
if ! "$PYTHON_BIN" -c "import tkinter" &> /dev/null; then
    echo "⚠ tkinter is not available for $PYTHON_BIN."
    echo "  Install it via your package manager, e.g.:"
    echo "    Debian/Ubuntu:  sudo apt install python3-tk"
    echo "    Fedora:         sudo dnf install python3-tkinter"
    echo "    Arch:           sudo pacman -S tk"
    echo "  Then re-run this script."
    exit 1
fi
echo "✓ tkinter available"

if [ ! -d "venv" ]; then
    echo "Creating venv/ ..."
    "$PYTHON_BIN" -m venv venv
else
    echo "venv/ already exists, reusing it."
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip > /dev/null

if [ -f "requirements.txt" ]; then
    echo "Installing requirements.txt ..."
    pip install -r requirements.txt
else
    echo "⚠ requirements.txt not found in $(pwd) - skipping."
fi

echo
echo "============================================================"
echo " ✓ Done. Activate the environment with:"
echo "     source venv/bin/activate"
echo " Then run the app with:"
echo "     python main.py"
echo "============================================================"
