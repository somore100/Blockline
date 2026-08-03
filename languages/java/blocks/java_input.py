block_id = "java_input"
display_name = "Read Line Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "input"},
    {"name": "scanner", "type": "string", "default": "scanner"}
]

def default_params():
    return {"variable": "input", "scanner": "scanner"}

def generate_code(params, children, lang="java"):
    variable = params.get("variable", "input")
    scanner = params.get("scanner", "scanner")
    return f"{variable} = {scanner}.nextLine();\n"

block_ui_description = {
    "label": "Read Line Input",
    "params": params,
    "category": "Basic",
    "description": "Reads a line of input using an already-created Scanner."
}
