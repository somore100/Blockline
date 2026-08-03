block_id = "go_import"
display_name = "Import"
category = "Modules"

params = [
    {"name": "package", "type": "string", "default": "fmt"}
]

def default_params():
    return {"package": "fmt"}

def generate_code(params, children, lang="go"):
    return f'import "{params.get("package", "fmt")}"\n'

block_ui_description = {
    "label": "Import",
    "params": params,
    "category": "Modules",
    "description": "Imports a Go package (e.g. fmt, os, strings)."
}
