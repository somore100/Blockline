block_id = "go_variable"
display_name = "Set Variable"
category = "Basic"

params = [
    {"name": "variable", "type": "string", "default": "x"},
    {"name": "value", "type": "string", "default": "0"}
]

def default_params():
    return {"variable": "x", "value": "0"}

def generate_code(params, children, lang="go"):
    var = params.get("variable", "x")
    val = params.get("value", "0")
    return f"{var} := {val}\n"

block_ui_description = {
    "label": "Set Variable",
    "params": params,
    "category": "Basic",
    "description": "Declares and assigns a variable using Go's short declaration (:=)."
}
