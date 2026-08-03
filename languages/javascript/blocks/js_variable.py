block_id = "js_variable"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "kind", "type": "choice", "default": "let", "choices": ["let", "const", "var"]},
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"kind": "let", "variable": "x", "value": "0"}

def generate_code(params, children, lang="javascript"):
    kind = params.get("kind", "let")
    var = params.get("variable", "x")
    val = params.get("value", "0")
    return f"{kind} {var} = {val};\n"

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Declares and assigns a value to a variable. Type the value as valid JS (e.g. \"text\" with quotes, or 5 without)."
}
