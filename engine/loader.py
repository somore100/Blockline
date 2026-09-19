"""
JSON language pack loader.

Replaces the old importlib.util / exec_module block loader completely:
packs are pure data now, never executed. Anything malformed is
skipped with a warning - it must never crash the app (Phase 2 point 7,
Phase 4 point 14). This same function serves both bundled/core packs
at startup (Phase 4 point 12) and later, addon packs loaded async
after startup (Phase 4 point 13) - the validate-or-skip contract is
identical either way, only the "Core" vs "Community" tag differs.
"""

import json
import pathlib

from engine.schema import (
    validate_manifest,
    validate_concepts,
    validate_node_types,
    validate_block_match,
    validate_comment_token,
)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_language_pack(pack_dir, verbose=False):
    """
    Load + validate one language pack directory:
        pack_dir/manifest.json      (required)
        pack_dir/blocks/*.json      (required - one block per file, the
                                      filename minus ".json" IS the
                                      block's id; replaces the old
                                      single concepts.json so adding,
                                      removing, or hand-editing one
                                      block never touches the others)
        pack_dir/includes.json      (optional - auto-import rules)
        pack_dir/node_types.json    (optional, Phase A2 - node-hierarchy
                                      kinds like "function"/"start" this
                                      language can create; absence just
                                      means the pack stays forward-only,
                                      no node hierarchy for it yet)

    Returns (manifest, blocks) on success, or (None, None) if the pack
    should be skipped. Callers must treat (None, None) as "skip this
    pack, keep going" - never as fatal.
    """
    pack_dir = pathlib.Path(pack_dir)
    manifest_path = pack_dir / "manifest.json"
    blocks_dir = pack_dir / "blocks"
    includes_path = pack_dir / "includes.json"
    node_types_path = pack_dir / "node_types.json"

    if not manifest_path.exists() or not blocks_dir.is_dir():
        print(f"\u26a0 Skipping language pack '{pack_dir.name}': missing manifest.json or blocks/ folder")
        return None, None

    try:
        manifest = _load_json(manifest_path)
        includes = _load_json(includes_path) if includes_path.exists() else {}
        node_types = _load_json(node_types_path) if node_types_path.exists() else []
    except (OSError, json.JSONDecodeError) as e:
        print(f"\u26a0 Skipping language pack '{pack_dir.name}': could not parse JSON ({e})")
        return None, None

    # Each block is its own file now - a malformed one is skipped
    # individually (same "one bad block never drops its siblings"
    # contract as before, just enforced one file earlier: a syntax
    # error in one block's JSON can't even prevent its sibling files
    # from being read at all).
    blocks = {}
    for block_file in sorted(blocks_dir.glob("*.json")):
        block_id = block_file.stem
        try:
            blocks[block_id] = _load_json(block_file)
        except (OSError, json.JSONDecodeError) as e:
            print(f"\u26a0 Skipping block file '{block_file.name}' in pack '{pack_dir.name}': could not parse JSON ({e})")

    errors = validate_manifest(manifest, pack_dir.name)
    if errors:
        print(f"\u26a0 Skipping language pack '{pack_dir.name}' - failed validation:")
        for err in errors:
            print(f"    - {err}")
        return None, None

    comment_token_warnings = validate_comment_token(manifest, pack_dir.name)
    if comment_token_warnings:
        for w in comment_token_warnings:
            print(f"\u26a0 Ignoring 'comment_token': {w}")
        manifest = dict(manifest)
        del manifest["comment_token"]

    block_errors = validate_concepts(blocks, pack_dir.name)
    if block_errors:
        bad_block_ids = {bid for bid, _ in block_errors if bid is not None}
        for bid, err in block_errors:
            print(f"\u26a0 Skipping block '{bid}' in pack '{pack_dir.name}': {err}")
        blocks = {bid: bdef for bid, bdef in blocks.items() if bid not in bad_block_ids}
        if not blocks:
            print(f"\u26a0 Skipping language pack '{pack_dir.name}': every block failed validation")
            return None, None

    # A bad "match" rule only disables cold-import/slot-parsing
    # recognition for that one block - it must never take the block's
    # normal forward codegen down with it (see validate_block_match's
    # docstring). Strip and warn instead of dropping the block.
    for block_id, block_def in blocks.items():
        if "match" in block_def:
            match_warnings = validate_block_match(block_def["match"], block_id, pack_dir.name)
            if match_warnings:
                for w in match_warnings:
                    print(f"\u26a0 Ignoring 'match' rule: {w}")
                del block_def["match"]

    node_type_errors = validate_node_types(node_types, pack_dir.name)
    if node_type_errors:
        bad_node_type_labels = {label for label, _ in node_type_errors}
        for label, err in node_type_errors:
            print(f"\u26a0 Skipping node type '{label}' in pack '{pack_dir.name}': {err}")
        good_node_types = []
        for i, nt in enumerate(node_types):
            label = nt.get("id", i) if isinstance(nt, dict) else i
            if label not in bad_node_type_labels:
                good_node_types.append(nt)
        node_types = good_node_types

    manifest = dict(manifest)
    manifest["includes"] = includes
    manifest["node_types"] = node_types

    if verbose:
        print(f"\u2713 Loaded language pack '{manifest.get('name', pack_dir.name)}' ({len(blocks)} blocks)")

    return manifest, blocks


def load_all_language_packs(languages_root, verbose=False):
    """
    Discover every subfolder of `languages_root` and load it as a
    language pack. Returns:
        { lang_folder_name: {"manifest": {...}, "blocks": {...}} }
    Packs that fail to load are simply absent from the result (a
    warning was already printed by load_language_pack).
    """
    languages_root = pathlib.Path(languages_root)
    packs = {}

    if not languages_root.exists():
        if verbose:
            print(f"\u26a0 Languages folder does not exist: {languages_root.resolve()}")
        return packs

    for entry in sorted(languages_root.iterdir()):
        if not entry.is_dir():
            continue
        manifest, blocks = load_language_pack(entry, verbose=verbose)
        if manifest is None:
            continue
        packs[entry.name] = {"manifest": manifest, "blocks": blocks}

    return packs


def load_master_concepts(concepts_path, verbose=False):
    """
    Load the root concepts.json (Phase 1 point 1) - the shared
    universal concept-id vocabulary used later for cross-language
    translation (Phase 5). Returns {} on any problem rather than
    raising: the app should still start with language packs' raw/
    non-translatable blocks even if this file is missing or broken.
    """
    concepts_path = pathlib.Path(concepts_path)
    if not concepts_path.exists():
        if verbose:
            print(f"\u26a0 Master concepts.json not found at {concepts_path.resolve()}")
        return {}

    try:
        data = _load_json(concepts_path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"\u26a0 Could not load master concepts.json: {e}")
        return {}

    if not isinstance(data, dict) or not isinstance(data.get("concepts"), list):
        print("\u26a0 Master concepts.json missing a top-level 'concepts' list")
        return {}

    return {c["id"]: c for c in data["concepts"] if isinstance(c, dict) and "id" in c}
