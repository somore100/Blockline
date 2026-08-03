block_id = "html_page"
display_name = "HTML Page"
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
    return "<!DOCTYPE html>\n<html>\n" + "\n".join(body_lines) + "\n</html>\n"

block_ui_description = {
    "label": "HTML Page",
    "params": params,
    "category": "Structure",
    "description": "The root of an HTML document. Put a Head block and a Body block inside it."
}
