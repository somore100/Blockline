# languages/python/blocks/if_statement.py
#
# Container block: unlike every other block, this one has a nested
# "body" of other blocks inside it, shown indented in the workspace.
# is_container = True tells Blockline to render it that way and to pass
# its rendered children through generate_code's `children` argument
# (a list of already-rendered code strings, one per child block -
# including their own further nesting, if any).

block_id = "if_statement"
display_name = "If"
category = "Control"
is_container = True

params = [
    {"name": "condition", "type": "boolean", "default": "True"}
]

def default_params():
    return {"condition": "True", "_children": []}

def generate_code(params, children, lang="python"):
    condition = params.get("condition", "True")

    body_lines = []
    for child_code in children:
        for line in child_code.rstrip("\n").split("\n"):
            body_lines.append("    " + line if line.strip() else "")

    if not body_lines:
        body_lines = ["    pass"]

    return f"if {condition}:\n" + "\n".join(body_lines) + "\n"

block_ui_description = {
    "label": "If",
    "params": params,
    "category": "Control",
    "description": "Runs the blocks inside its body only when the condition is true. Add blocks to the body with the '+ Add Block' button that appears once this is in your workspace."
}
