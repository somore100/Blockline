block_id = "html_title"
display_name = "Title"
category = "Basic"

params = [
    {"name": "text", "type": "string", "default": "My Page"}
]

def default_params():
    return {"text": "My Page"}

def generate_code(params, children, lang="html"):
    return f"<title>{params.get('text', '')}</title>\n"

block_ui_description = {
    "label": "Title",
    "params": params,
    "category": "Basic",
    "description": "The page's browser tab title. Goes inside a Head block."
}
