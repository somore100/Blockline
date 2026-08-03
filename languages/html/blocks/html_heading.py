block_id = "html_heading"
display_name = "Heading"
category = "Basic"

params = [
    {"name": "level", "type": "choice", "default": "1", "choices": ["1", "2", "3", "4", "5", "6"]},
    {"name": "text", "type": "string", "default": "Heading"}
]

def default_params():
    return {"level": "1", "text": "Heading"}

def generate_code(params, children, lang="html"):
    level = params.get("level", "1")
    text = params.get("text", "")
    return f"<h{level}>{text}</h{level}>\n"

block_ui_description = {
    "label": "Heading",
    "params": params,
    "category": "Basic",
    "description": "A heading, h1 (biggest) through h6 (smallest)."
}
