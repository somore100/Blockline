from engine.loader import load_blocks


def render_project(project, lang="python"):
    """Render project blocks into source code"""
    registry = load_blocks()
    output_lines = []

    for block in project.blocks:
        block_def = registry.get(block.block_id)
        if not block_def:
            continue

        code = block_def.generate_code(
            block.params,
            block.children,
            lang
        )
        output_lines.append(code)

    return "".join(output_lines)
