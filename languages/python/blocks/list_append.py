block_id = "list_append"
display_name = "Append to List"
category = "Data Structures"
params = [
    {"name": "list", "type": "string", "default": "my_list"},
    {"name": "item", "type": "string", "default": "item"}
]

def default_params():
    return {"list": "my_list", "item": "item"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        lst = params.get("list", "my_list")
        item = params.get("item", "item")
        return f'{lst}.append({item})\n'
    return ""

block_ui_description = {
    "label": "Append to List",
    "params": params,
    "category": "Data Structures",
    "description": "Adds an item to the end of a list"
}
