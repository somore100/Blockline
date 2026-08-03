block_id = "c_input_number"
display_name = "Read Number Input"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "x"}
]

def default_params():
    return {"variable": "x"}

def generate_code(params, children, lang="c"):
    variable = params.get("variable", "x")
    return f'scanf("%d", &{variable});\n'

block_ui_description = {
    "label": "Read Number Input",
    "params": params,
    "category": "Basic",
    "description": "Reads an integer from the user into an already-declared int variable."
}
