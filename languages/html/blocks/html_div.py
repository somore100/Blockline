block_id = "html_div"
display_name = "Div"
category = "Structure"
is_container = True

params = [
    {"name": "class_name", "type": "string", "default": ""}
]

def default_params():
    return {"class_name": "", "_children": []}

def generate_code(params, children, lang="html"):
    class_name = params.get("class_name", "").strip()
    open_tag = f'<div class="{class_name}">' if class_name else "<div>"
    body_lines = []
    for child_code in children:
        for line in child_code.rstrip("\n").split("\n"):
            body_lines.append("  " + line if line.strip() else "")
    if not body_lines:
        body_lines = ["  <!-- empty -->"]
    return open_tag + "\n" + "\n".join(body_lines) + "\n</div>\n"

block_ui_description = {
    "label": "Div",
    "params": params,
    "category": "Structure",
    "description": "A generic container for grouping other elements, optionally with a CSS class."
}
