block_id = "include_cpp"
display_name = "Include Header"
category = "Modules"

params = [
    {"name": "header", "type": "string", "default": "iostream"}
]

def default_params():
    return {"header": "iostream"}

def generate_code(params, children, lang="cpp"):
    header = params.get("header", "iostream")
    return f'#include <{header}>\n'

block_ui_description = {
    "label": "Include Header",
    "params": params,
    "category": "Modules",
    "description": "Includes a C++ header file (e.g., iostream, string, vector)"
}
