block_id = "import_module"
display_name = "Import Module"
category = "Modules"
params = [
    {"name": "module", "type": "string", "default": "math"},
    {"name": "alias", "type": "string", "default": ""}
]

def default_params():
    return {"module": "math", "alias": ""}

def generate_code(params, children, lang="python"):
    if lang.lower().startswith("py"):
        module = params.get("module", "")
        alias = params.get("alias", "")
        if alias:
            return f'import {module} as {alias}\n'
        return f'import {module}\n'
    return ""

block_ui_description = {
    "label": "Import Module",
    "params": params,
    "category": "Modules",
    "description": "Imports a Python module"
}