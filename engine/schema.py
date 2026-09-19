"""
Schema validation for JSON language packs.

A pack that is missing fields, has the wrong types, or is otherwise
corrupt must be rejected with a warning - it must NEVER crash the app
(Phase 2 point 6, Phase 4 point 14). This module only inspects data;
it never executes anything from a pack.
"""

REQUIRED_MANIFEST_FIELDS = {
    "name": str,
    "version": str,
}


def validate_manifest(manifest, pack_name="<unknown>"):
    """Return a list of human-readable error strings (empty = valid)."""
    if not isinstance(manifest, dict):
        return [f"{pack_name}: manifest.json must be a JSON object"]

    errors = []
    for field, expected_type in REQUIRED_MANIFEST_FIELDS.items():
        if field not in manifest:
            errors.append(f"{pack_name}: manifest.json missing required field '{field}'")
        elif not isinstance(manifest[field], expected_type):
            errors.append(
                f"{pack_name}: manifest.json field '{field}' must be a {expected_type.__name__}"
            )
    return errors


def validate_comment_token(manifest, pack_name="<unknown>"):
    """
    Validate the optional 'comment_token' manifest field (Phase A2/A3).
    Returns a list of warning strings (empty = valid/absent). Unlike
    validate_manifest()'s required fields, a bad comment_token must
    NOT take the whole pack down - it's needed only for A3's
    marker-comment export, so callers should warn and strip it,
    leaving the pack (and every other field) intact.
    """
    if "comment_token" not in manifest:
        return []
    token = manifest["comment_token"]
    valid_single = isinstance(token, str)
    valid_pair = isinstance(token, list) and len(token) == 2 and all(isinstance(t, str) for t in token)
    if valid_single or valid_pair:
        return []
    return [f"{pack_name}: manifest.json field 'comment_token' must be a string or a [open, close] pair of strings"]


REQUIRED_NODE_TYPE_FIELDS = {
    "id": str,
    "is_entry_point": bool,
}

OPTIONAL_NODE_TYPE_TYPED_FIELDS = {
    "node_kind": (str, type(None)),
    "header_template": (str, type(None)),
    "required": (bool,),
}


def validate_node_types(node_types, pack_name="<unknown>"):
    """
    Validate a language pack's node_types.json (Phase A2) - a list of
    node-type definitions describing what kinds of Node the node/wire
    hierarchy can create for this language (e.g. "function", "start").

    Returns a list of (index_or_id, error_message) pairs, same shape
    as validate_concepts()'s return - so the loader can drop only the
    specific malformed entries instead of rejecting the whole file.
    node_types.json is optional to begin with (Phase B/E consume it;
    nothing crashes if it's absent), so an empty/missing file is not
    itself an error - only malformed *entries* are.
    """
    if not isinstance(node_types, list):
        return [(None, f"{pack_name}: node_types.json must be a JSON array")]

    errors = []
    for i, entry in enumerate(node_types):
        label = entry.get("id", i) if isinstance(entry, dict) else i
        if not isinstance(entry, dict):
            errors.append((label, f"node_types.json entry {i} must be a JSON object"))
            continue

        for field, expected_type in REQUIRED_NODE_TYPE_FIELDS.items():
            if field not in entry:
                errors.append((label, f"node type '{label}' missing required field '{field}'"))
            elif not isinstance(entry[field], expected_type):
                errors.append((label, f"node type '{label}' field '{field}' must be a {expected_type.__name__}"))

        for field, expected_types in OPTIONAL_NODE_TYPE_TYPED_FIELDS.items():
            if field in entry and not isinstance(entry[field], expected_types):
                names = " or ".join(t.__name__ for t in expected_types)
                errors.append((label, f"node type '{label}' field '{field}' must be {names}"))

    return errors


def validate_block_match(match, block_id, pack_name="<unknown>"):
    """
    Validate a block's optional "match" object (Phase A2) - the
    reverse-recognition rule Phase E/F use to map cold-import/typed
    code back onto this block. Unlike validate_concepts(), a bad
    "match" must NOT take the whole block down: recognition is a
    forward-looking bonus feature, and a block with no working match
    rule simply isn't recognizable yet (falls back to raw, same as
    if "match" were absent entirely) - it must still render code fine.

    Returns a list of warning strings (empty = valid). Callers should
    strip the "match" key and warn on any error, not drop the block.
    """
    if not isinstance(match, dict):
        return [f"block '{block_id}' in pack '{pack_name}': 'match' must be a JSON object"]

    warnings = []
    if "node_kind" not in match:
        warnings.append(f"block '{block_id}' in pack '{pack_name}': 'match' missing 'node_kind'")
    elif not isinstance(match["node_kind"], str):
        warnings.append(f"block '{block_id}' in pack '{pack_name}': 'match.node_kind' must be a string")

    if "slot_map" not in match:
        warnings.append(f"block '{block_id}' in pack '{pack_name}': 'match' missing 'slot_map'")
    elif not isinstance(match["slot_map"], dict):
        warnings.append(f"block '{block_id}' in pack '{pack_name}': 'match.slot_map' must be a JSON object")
    else:
        for slot, source in match["slot_map"].items():
            if not isinstance(slot, str) or not isinstance(source, str):
                warnings.append(
                    f"block '{block_id}' in pack '{pack_name}': 'match.slot_map' keys and values must be strings"
                )
                break

    return warnings


def validate_concepts(blocks, pack_name="<unknown>"):
    """
    Validate a language pack's assembled block set - a dict mapping
    local block id -> block definition (each definition loaded from
    its own languages/<lang>/blocks/<block_id>.json file). Each
    definition needs at least a 'template' string; everything else
    (display_name, category, concept_id, is_container, params...) is
    optional metadata for the UI / translator.

    Returns a list of (block_id, error_message) pairs rather than
    raising or returning a flat error list - this lets the loader
    drop only the specific blocks that failed validation instead of
    rejecting the whole pack over one bad block (Phase 4's "warn and
    skip, never crash" philosophy applied at block granularity, not
    just pack granularity).
    """
    if not isinstance(blocks, dict):
        return [(None, f"{pack_name}: block set must be a dict mapping block id -> definition")]

    errors = []
    for block_id, block_def in blocks.items():
        if not isinstance(block_def, dict):
            errors.append((block_id, f"block '{block_id}' definition must be a JSON object"))
            continue

        if "template" not in block_def:
            errors.append((block_id, f"block '{block_id}' missing required 'template' field"))
        elif not isinstance(block_def["template"], str):
            errors.append((block_id, f"block '{block_id}' 'template' must be a string"))

        if "is_container" in block_def and not isinstance(block_def["is_container"], bool):
            errors.append((block_id, f"block '{block_id}' 'is_container' must be a boolean"))

        if "params" in block_def and not isinstance(block_def["params"], list):
            errors.append((block_id, f"block '{block_id}' 'params' must be a list"))

        if "concept_id" in block_def and not isinstance(block_def["concept_id"], str):
            errors.append((block_id, f"block '{block_id}' 'concept_id' must be a string"))

    return errors
