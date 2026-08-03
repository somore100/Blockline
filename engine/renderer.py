from engine.loader import load_blocks_for_language


def render_project(project, lang="python", languages_root="languages",
                    core_folder=None, block_registry=None):
    """
    Render project blocks into source code for the given language.

    block_registry can be passed in (e.g. the one already loaded at
    startup) to avoid re-scanning disk on every render. If omitted,
    blocks are loaded fresh for `lang`.
    """
    registry = block_registry or load_blocks_for_language(
        lang, languages_root=languages_root, core_folder=core_folder
    )

    output_lines = []
    for block in project.blocks:
        block_def = registry.get(block.block_id)
        if not block_def:
            output_lines.append(f"# ⚠ Unknown block: {block.block_id}\n")
            continue

        code = block_def.generate_code(block.params, block.children, lang)
        output_lines.append(code)

    return "".join(output_lines)
