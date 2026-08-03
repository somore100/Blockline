block_id = "type_function"
display_name = "Type (type)"
category = "Functions"
params = [
    {"name": "result", "type": "string", "default": "var_type"},
    {"name": "object", "type": "string", "default": "my_var"}
]

def default_params():
    return {"result": "var_type", "object": "my_var"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        result = params.get("result", "var_type")
        obj = params.get("object", "my_var")
        return f'{result} = type({obj})\n'
    return ""

block_ui_description = {
    "label": "Type",
    "params": params,
    "category": "Functions",
    "description": "Gets the type of an object"
}
