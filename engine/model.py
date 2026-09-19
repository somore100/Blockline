class BlockInstance:
    """Runtime representation of a block in the workspace"""

    def __init__(self, block_id: str, params=None, children=None):
        self.block_id = block_id
        self.params = params or {}
        self.children = children or []


class Project:
    """Root project model (JSON-serializable later)"""

    def __init__(self):
        self.blocks = []

    def add_block(self, block_id: str, params=None, children=None):
        self.blocks.append(BlockInstance(block_id, params, children))


class Node:
    """
    One function/class/entry-point in the node/wire hierarchy (Phase A).

    A Node's `.blocks` list is shaped exactly like `Project.blocks` -
    a list of BlockInstance - on purpose, so render_project() and every
    existing block-editing widget in ui.py keep working unchanged when
    simply pointed at `node.blocks` instead of a whole Project. Nothing
    in this class replaces Project; Project stays the shape a single
    node's contents take.

    `references` is always derived (Phase C scans func_call/import_module
    block instances and recomputes it) - never hand-authored, so the
    wire graph can't drift out of sync with the actual block trees.

    `raw_span` is set only for nodes created from unrecognized cold-import
    content (Phase E) or a marker-comment mismatch (Phase A3); when set,
    `blocks` stays empty and the node is text-editable but not
    block-editable, matching the existing raw_code block's philosophy of
    an honest fallback over a wrong guess.
    """

    def __init__(self, node_id, node_type, name, category=None, blocks=None, references=None, raw_span=None):
        self.node_id = node_id
        self.node_type = node_type
        self.name = name
        self.category = category
        self.blocks = blocks or []
        self.references = references or []
        self.raw_span = raw_span


class BlocklinerFile:
    """One source file's worth of nodes, for a single language."""

    def __init__(self, filename, language, nodes=None):
        self.filename = filename
        self.language = language
        self.nodes = nodes or []


class Workspace:
    """Top-level container for all files in a Blockliner project."""

    def __init__(self, files=None):
        self.files = files or []
