block_id = "string_replace"
display_name = "Replace in String"
category = "String Operations"
params = [
    {"name": "result", "type": "string", "default": "new_text"},
    {"name": "text", "type": "string", "default": "text"},
    {"name": "old", "type": "string", "default": "old"},
    {"name": "new", "type": "string", "default": "new"}
]

def default_params():
    return {"result": "new_text", "text": "text", "old": "old", "new": "new"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "new_text")
        text = params.get("text", "text")
        old = params.get("old", "old")
        new = params.get("new", "new")
        return f'{result} = {text}.replace({repr(old)}, {repr(new)})\n'
    return ""

block_ui_description = {
    "label": "Replace",
    "params": params,
    "category": "String Operations",
    "description": "Replaces occurrences of text in a string"
}