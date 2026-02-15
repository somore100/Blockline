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
