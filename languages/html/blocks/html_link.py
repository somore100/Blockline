block_id = "html_link"
display_name = "Link"
category = "Basic"

params = [
    {"name": "url", "type": "string", "default": "https://example.com"},
    {"name": "text", "type": "string", "default": "Click here"}
]

def default_params():
    return {"url": "https://example.com", "text": "Click here"}

def generate_code(params, children, lang="html"):
    url = params.get("url", "")
    text = params.get("text", "")
    return f'<a href="{url}">{text}</a>\n'

block_ui_description = {
    "label": "Link",
    "params": params,
    "category": "Basic",
    "description": "A clickable hyperlink."
}
