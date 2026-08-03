block_id = "string_lower"
display_name = "Lowercase String"
category = "String Operations"
params = [
    {"name": "result", "type": "string", "default": "lower_text"},
    {"name": "text", "type": "string", "default": "text"}
]

def default_params():
    return {"result": "lower_text", "text": "text"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "lower_text")
        text = params.get("text", "text")
        return f'{result} = {text}.lower()\n'
    return ""

block_ui_description = {
    "label": "Lowercase",
    "params": params,
    "category": "String Operations",
    "description": "Converts a string to lowercase"
}
