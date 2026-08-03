block_id = "html_head"
display_name = "Head"
category = "Structure"
is_container = True

params = []

def default_params():
    return {"_children": []}

def generate_code(params, children, lang="html"):
    body_lines = []
    for child_code in children:
        for line in child_code.rstrip("\n").split("\n"):
            body_lines.append("  " + line if line.strip() else "")
    if not body_lines:
        body_lines = ["  <!-- empty -->"]
    return "<head>\n" + "\n".join(body_lines) + "\n</head>\n"

block_ui_description = {
    "label": "Head",
    "params": params,
    "category": "Structure",
    "description": "Page metadata section. Put a Title block inside it."
}
