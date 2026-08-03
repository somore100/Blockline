block_id = "java_scanner_create"
display_name = "Create Scanner"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "scanner"}
]

def default_params():
    return {"variable": "scanner"}

def generate_code(params, children, lang="java"):
    variable = params.get("variable", "scanner")
    return f"Scanner {variable} = new Scanner(System.in);\n"

block_ui_description = {
    "label": "Create Scanner",
    "params": params,
    "category": "Basic",
    "description": "Creates a Scanner for reading input. Add an Import block for java.util.Scanner first."
}
