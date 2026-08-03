block_id = "html_paragraph"
display_name = "Paragraph"
category = "Basic"

params = [
    {"name": "text", "type": "string", "default": "Some text."}
]

def default_params():
    return {"text": "Some text."}

def generate_code(params, children, lang="html"):
    return f"<p>{params.get('text', '')}</p>\n"

block_ui_description = {
    "label": "Paragraph",
    "params": params,
    "category": "Basic",
    "description": "A paragraph of text."
}
