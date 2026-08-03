"""
Blockline - Entry point

Loads the block modules and starts the visual editor UI.
"""

import sys

from ui import start_ui
from engine.loader import load_blocks_from_folder

BLOCKS_PATH = "languages/python/blocks"
LANGUAGES_PATH = "languages"


def main():
    print("Starting Blockline...")

    blocks = load_blocks_from_folder(BLOCKS_PATH)

    if not blocks:
        print(f"⚠ No blocks found under '{BLOCKS_PATH}'.")
        print("  Check that the folder exists and contains block files")
        print("  with a 'block_id' attribute.")
    else:
        print(f"Loaded {len(blocks)} block(s):")
        for block_id, module in blocks.items():
            display_name = getattr(module, "display_name", "Unknown")
            print(f" - {block_id} ({display_name})")

    start_ui(blocks, languages_path=LANGUAGES_PATH)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"✗ Blockline failed to start: {e}", file=sys.stderr)
        sys.exit(1)
