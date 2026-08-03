block_id = "string_upper"
display_name = "Uppercase String"
category = "String Operations"
params = [
    {"name": "result", "type": "string", "default": "upper_text"},
    {"name": "text", "type": "string", "default": "text"}
]

def default_params():
    return {"result": "upper_text", "text": "text"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "upper_text")
        text = params.get("text", "text")
        return f'{result} = {text}.upper()\n'
    return ""

block_ui_description = {
    "label": "Uppercase",
    "params": params,
    "category": "String Operations",
    "description": "Converts a string to uppercase"
}
