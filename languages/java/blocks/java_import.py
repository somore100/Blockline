block_id = "java_import"
display_name = "Import"
category = "Modules"

params = [
    {"name": "package", "type": "string", "default": "java.util.Scanner"}
]

def default_params():
    return {"package": "java.util.Scanner"}

def generate_code(params, children, lang="java"):
    return f"import {params.get('package', 'java.util.Scanner')};\n"

block_ui_description = {
    "label": "Import",
    "params": params,
    "category": "Modules",
    "description": "Imports a Java class or package."
}
