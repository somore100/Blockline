block_id = "list_create"
display_name = "Create List"
category = "Data Structures"
params = [
    {"name": "variable", "type": "string", "default": "my_list"},
    {"name": "items", "type": "string", "default": "1, 2, 3"}
]

def default_params():
    return {"variable": "my_list", "items": "1, 2, 3"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        var = params.get("variable", "my_list")
        items = params.get("items", "")
        return f'{var} = [{items}]\n'
    return ""

block_ui_description = {
    "label": "Create List",
    "params": params,
    "category": "Data Structures",
    "description": "Creates a new list with specified items"
}