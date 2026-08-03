block_id = "dict_create"
display_name = "Create Dictionary"
category = "Data Structures"
params = [
    {"name": "variable", "type": "string", "default": "my_dict"},
    {"name": "pairs", "type": "string", "default": "'key': 'value'"}
]

def default_params():
    return {"variable": "my_dict", "pairs": "'key': 'value'"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        var = params.get("variable", "my_dict")
        pairs = params.get("pairs", "")
        return f'{var} = {{{pairs}}}\n'
    return ""

block_ui_description = {
    "label": "Create Dictionary",
    "params": params,
    "category": "Data Structures",
    "description": "Creates a new dictionary with key-value pairs"
}
