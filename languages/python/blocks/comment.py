block_id = "comment"
display_name = "Comment"
category = "Basic"
params = [
    {"name": "text", "type": "string", "default": "This is a comment"}
]

def default_params():
    return {"text": "This is a comment"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        text = params.get("text", "")
        return f'# {text}\n'
    elif lang.lower().startswith("c"):
        text = params.get("text", "")
        return f'// {text}\n'
    return ""

block_ui_description = {
    "label": "Comment",
    "params": params,
    "category": "Basic",
    "description": "Adds a comment to the code"
}