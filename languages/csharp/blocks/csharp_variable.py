block_id = "csharp_variable"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "type", "type": "choice", "default": "var", "choices": ["var", "int", "double", "string", "bool"]},
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"type": "var", "variable": "x", "value": "0"}

def generate_code(params, children, lang="csharp"):
    var_type = params.get("type", "var")
    var = params.get("variable", "x")
    val = params.get("value", "0")
    if var_type == "string" and not (val.startswith('"') or val.startswith("'")):
        val = f'"{val}"'
    return f"{var_type} {var} = {val};\n"

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Declares and assigns a value to a variable."
}
