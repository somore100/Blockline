block_id = "html_image"
display_name = "Image"
category = "Basic"

params = [
    {"name": "src", "type": "string", "default": "image.png"},
    {"name": "alt", "type": "string", "default": "description"}
]

def default_params():
    return {"src": "image.png", "alt": "description"}

def generate_code(params, children, lang="html"):
    src = params.get("src", "")
    alt = params.get("alt", "")
    return f'<img src="{src}" alt="{alt}">\n'

block_ui_description = {
    "label": "Image",
    "params": params,
    "category": "Basic",
    "description": "An image. Always fill in 'alt' text for accessibility."
}
