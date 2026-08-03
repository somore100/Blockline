block_id = "c_include"
display_name = "Include Header"
category = "Modules"

params = [
    {"name": "header", "type": "string", "default": "stdio.h"}
]

def default_params():
    return {"header": "stdio.h"}

def generate_code(params, children, lang="c"):
    header = params.get("header", "stdio.h")
    return f"#include <{header}>\n"

block_ui_description = {
    "label": "Include Header",
    "params": params,
    "category": "Modules",
    "description": "Includes a C header file (e.g. stdio.h, stdlib.h, string.h)."
}
