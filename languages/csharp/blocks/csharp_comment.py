block_id = "csharp_comment"
display_name = "Comment"
category = "Basic"

params = [
    {"name": "text", "type": "string", "default": "This is a comment"}
]

def default_params():
    return {"text": "This is a comment"}

def generate_code(params, children, lang="csharp"):
    return f"// {params.get('text', '')}\n"

block_ui_description = {
    "label": "Comment",
    "params": params,
    "category": "Basic",
    "description": "Adds a comment to the code."
}
