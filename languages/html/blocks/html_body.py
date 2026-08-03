block_id = "html_body"
display_name = "Body"
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
    return "<body>\n" + "\n".join(body_lines) + "\n</body>\n"

block_ui_description = {
    "label": "Body",
    "params": params,
    "category": "Structure",
    "description": "The visible page content. Put headings, paragraphs, and other blocks inside it."
}
