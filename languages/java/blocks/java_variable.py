block_id = "java_variable"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "type", "type": "choice", "default": "int", "choices": ["int", "double", "String", "boolean"]},
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"type": "int", "variable": "x", "value": "0"}

def generate_code(params, children, lang="java"):
    var_type = params.get("type", "int")
    var = params.get("variable", "x")
    val = params.get("value", "0")
    if var_type == "String" and not (val.startswith('"') or val.startswith("'")):
        val = f'"{val}"'
    return f"{var_type} {var} = {val};\n"

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Declares and assigns a value to a variable."
}
