block_id = "c_print_number"
display_name = "Print Number"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "x"}
]

def default_params():
    return {"variable": "x"}

def generate_code(params, children, lang="c"):
    variable = params.get("variable", "x")
    return f'printf("%d\\n", {variable});\n'

block_ui_description = {
    "label": "Print Number",
    "params": params,
    "category": "Basic",
    "description": "Prints an integer variable's value to the console."
}
