"""
Phase A3: marker-comment round-trip.

engine.renderer writes each Node's rendered output wrapped in a pair of
marker-comment lines carrying its node_id (render_node_with_marker /
render_file). This module does the reverse direction: given a file's
text (possibly hand-edited outside Blockliner since it was last
exported) and the in-memory BlocklinerFile Blockliner still remembers,
figure out what changed, per node, without needing tree-sitter or any
understanding of the target language at all - that's Phase E's job for
*unfamiliar* code. This is strictly the "did our own markers survive,
and does what's inside them still match?" check.

Nothing in here ever raises on malformed input. A file with garbled,
missing, duplicated, or mismatched markers still produces a usable
result - see parse_marked_file()'s and reconcile_file()'s docstrings
for exactly what "best effort" means in each case. This mirrors the
same skip-and-warn contract engine.schema/engine.loader already use
for language packs: one bad node's markers must never take down the
rest of the file.
"""

import re

from engine.model import BlocklinerFile, Node
from engine.renderer import render_project

MARKER_LINE_RE = re.compile(r"\$\$\$blockliner:node:(\d+)\$\$\$ (start|end)")


def parse_marked_file(text):
    """
    Scan `text` for Blockliner's marker-comment pairs and split it into
    ordered segments, regardless of what comment syntax (if any) wraps
    each marker line - only the literal tag text is matched, so this
    works even for a language whose comment_token is missing/invalid.

    Returns (segments, errors):
      segments - a list, in file order, of either
          {"kind": "node", "node_id": int, "content": str}
              `content` is exactly the text between the start and end
              marker lines, byte-for-byte (marker lines themselves are
              not included).
          {"kind": "unmarked", "content": str}
              any text outside of a marker pair. Empty for a purely
              Blockliner-generated file; preserved (never dropped) for
              a file that mixes hand-written and Blockliner content.
      errors - human-readable strings describing any malformed marker
          structure encountered (unmatched start/end, mismatched ids,
          an unclosed node at end of file). Always non-fatal: parsing
          still completes and produces its best-effort segments.
    """
    segments = []
    errors = []
    unmarked_buffer = []
    node_lines = []
    open_node_id = None

    def flush_unmarked():
        if unmarked_buffer:
            segments.append({"kind": "unmarked", "content": "".join(unmarked_buffer)})
            unmarked_buffer.clear()

    for line in text.splitlines(keepends=True):
        m = MARKER_LINE_RE.search(line)
        if not m:
            (node_lines if open_node_id is not None else unmarked_buffer).append(line)
            continue

        node_id, kind = int(m.group(1)), m.group(2)

        if kind == "start":
            if open_node_id is not None:
                errors.append(
                    f"node {node_id} 'start' marker found while node {open_node_id} "
                    f"was still open - closing node {open_node_id} early at this point"
                )
                segments.append({"kind": "node", "node_id": open_node_id, "content": "".join(node_lines)})
                node_lines = []
            flush_unmarked()
            open_node_id = node_id
        else:  # "end"
            if open_node_id is None:
                errors.append(f"node {node_id} 'end' marker found with no matching 'start' - ignoring")
                unmarked_buffer.append(line)
                continue
            if open_node_id != node_id:
                errors.append(
                    f"marker mismatch: node {open_node_id} 'start' closed by node {node_id} "
                    f"'end' - trusting the 'end' marker's id"
                )
            segments.append({"kind": "node", "node_id": open_node_id, "content": "".join(node_lines)})
            node_lines = []
            open_node_id = None

    if open_node_id is not None:
        errors.append(f"node {open_node_id} 'start' marker was never closed - keeping its content anyway")
        segments.append({"kind": "node", "node_id": open_node_id, "content": "".join(node_lines)})
    flush_unmarked()

    return segments, errors


def reconcile_file(original_file, text, block_registry):
    """
    Compare a BlocklinerFile Blockliner still has in memory (`original_file`)
    against `text` read back from disk, per node, using its markers.

    For each node found in `text`:
      - Not in `original_file` at all -> kept as an orphaned raw node
        (node_type="raw"). We have no metadata (name/category) to
        recover for it, so it's marked accordingly, not invented.
      - Was already raw before -> stays raw, content refreshed to
        whatever's in the file now (no demotion drama - it was already
        the honest fallback).
      - Was block-backed and its marked content still matches exactly
        what those blocks would render -> the ORIGINAL Node object is
        reattached unchanged, byte-identical, no-op case.
      - Was block-backed but the marked content diverged (hand-edited)
        -> demoted to node_type="raw" with raw_span set to exactly
        what's in the file. Blocks are never guessed back from this -
        that reconstruction is Phase E's job, not this one's.
    A node present in `original_file` whose marker is missing from
    `text` entirely is left unchanged (there's no signal to act on).

    Returns (new_file, diagnostics) - a new BlocklinerFile (original_file
    is never mutated) plus a list of human-readable strings explaining
    every judgment call made, including all parse_marked_file() errors.
    Never raises.
    """
    segments, diagnostics = parse_marked_file(text)
    original_by_id = {n.node_id: n for n in original_file.nodes}
    seen_ids = set()
    new_nodes = []

    for seg in segments:
        if seg["kind"] == "unmarked":
            if seg["content"].strip():
                diagnostics.append(
                    f"{len(seg['content'])} chars of unmarked content found outside any node - "
                    f"preserved as a pass-through raw node, not yet attached to project structure"
                )
                new_nodes.append(Node(node_id=None, node_type="raw", name="unmarked", raw_span=seg["content"]))
            continue

        node_id, content = seg["node_id"], seg["content"]
        seen_ids.add(node_id)
        original = original_by_id.get(node_id)

        if original is None:
            diagnostics.append(f"node {node_id}'s marker found in file but not in the project - kept as orphaned raw")
            new_nodes.append(Node(node_id=node_id, node_type="raw", name=f"orphan_{node_id}", raw_span=content))
            continue

        if original.raw_span is not None:
            new_nodes.append(Node(
                node_id=original.node_id, node_type=original.node_type, name=original.name,
                category=original.category, references=original.references, raw_span=content,
            ))
            continue

        expected = render_project(original, block_registry)
        if content == expected:
            new_nodes.append(original)
        else:
            diagnostics.append(f"node {node_id} ('{original.name}') content diverged from its blocks - demoted to raw")
            new_nodes.append(Node(
                node_id=original.node_id, node_type="raw", name=original.name,
                category=original.category, raw_span=content,
            ))

    for missing_id in set(original_by_id) - seen_ids:
        diagnostics.append(f"node {missing_id} ('{original_by_id[missing_id].name}') marker not found in file - left unchanged")
        new_nodes.append(original_by_id[missing_id])

    new_file = BlocklinerFile(filename=original_file.filename, language=original_file.language, nodes=new_nodes)
    return new_file, diagnostics
