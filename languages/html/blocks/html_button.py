block_id = "html_button"
display_name = "Button"
category = "Basic"

params = [
    {"name": "text", "type": "string", "default": "Click Me"}
]

def default_params():
    return {"text": "Click Me"}

def generate_code(params, children, lang="html"):
    return f"<button>{params.get('text', '')}</button>\n"

block_ui_description = {
    "label": "Button",
    "params": params,
    "category": "Basic",
    "description": "A clickable button."
}
