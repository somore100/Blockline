block_id = "assign"
display_name = "Set Variable"
category = "Basic"
params = [
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"variable": "x", "value": "0"}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        var = params.get("variable", "x")
        val = params.get("value", "0")
        # Try to determine if value should be quoted
        try:
            float(val)
            return f'{var} = {val}\n'
        except ValueError:
            if val.lower() in ['true', 'false', 'none']:
                return f'{var} = {val.capitalize()}\n'
            return f'{var} = {repr(val)}\n'
    return ""

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Assigns a value to a variable"
}
