block_id = "len_function"
display_name = "Length (len)"
category = "Functions"
params = [
    {"name": "result", "type": "string", "default": "length"},
    {"name": "object", "type": "string", "default": "my_list"}
]

def default_params():
    return {"result": "length", "object": "my_list"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "length")
        obj = params.get("object", "my_list")
        return f'{result} = len({obj})\n'
    return ""

block_ui_description = {
    "label": "Length",
    "params": params,
    "category": "Functions",
    "description": "Gets the length of a list, string, or other object"
}

